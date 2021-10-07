#include "compressor.h"

#include <cassert>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <unordered_map>

using namespace std;

#define DEBUG_PRINTS 0
#define PROGRESS_PRINTS 0

#define TRIGRAM_BLOCK_SHIFT 12
#define TRIGRAM_BLOCK_SIZE (1 << TRIGRAM_BLOCK_SHIFT)
#define MAX_OFFSET (0xFFF+1)
#define MIN_OFFSET 1
#define MATCH_MAX 65808

#if DEBUG_PRINTS || PROGRESS_PRINTS
#include <cstdio>
#endif

// Key format: 0xFFSSTT00 (F = first byte, S = second byte, T = third byte)
inline constexpr uint32_t makeTrigramKey(uint8_t first, uint8_t second, uint8_t third) {
    return ((uint32_t)first << 24) | ((uint32_t)second << 16) | ((uint32_t)third << 8);
}

// Represents a backreference or else a literal byte
struct Match {
private:
    uint32_t start;   // byte index relative to start of uncompressed file, ignored when length=1
    uint32_t length;  // number of uncompressed bytes consumed by the match 
    uint32_t cost;    // how many bytes until the end of the file (not including flag bytes)
    uint8_t byte;     // literal byte, ignored unless length=1

public:
    Match(uint32_t start, uint32_t length, uint32_t cost, uint8_t byte) {
        setStart(start);
        setLength(length);
        setCost(cost);
        setByte(byte);
    }

    inline uint32_t getStart() const {
        return start;
    }

    inline void setStart(uint32_t start) {
        this->start = start;
    }

    inline uint8_t getByte() const {
        return byte;
    }

    inline void setByte(uint8_t byte) {
        this->byte = byte;
    }

    inline uint32_t getLength() const {
        return length;
    }

    inline void setLength(uint32_t length) {
        this->length = length;
    }

    inline uint32_t getCost() const {
        return cost;
    }

    inline void setCost(uint32_t cost) {
        this->cost = cost;
    }

    // Output this match in the form of compressed bytes. Returns number of bytes written.
    // destination: where to start writing
    // referenceIdx: the offset within the uncompressed file that Match.start should be made relative to
    inline uint32_t encode(uint8_t *destination, uint32_t referenceIdx) const {
        const uint32_t o = referenceIdx - getStart() - 1;
        uint32_t l = getLength();
        if (l > MATCH_MAX) {
            assert(false && "length too long");
        } else if (length >= 273) {
            l -= 273;
            destination[0] = 0x10 | (l >> 12);
            destination[1] = l >> 4;
            destination[2] = ((l & 0xF) << 4) | (o >> 8);
            destination[3] = o;
            return 4;
        } else if (l >= 17) {
            l -= 17;
            destination[0] = l >> 4;
            destination[1] = ((l & 0xF) << 4) | (o >> 8);
            destination[2] = o;
            return 3;
        } else if (l >= 3) {
            l -= 1;
            destination[0] = (l << 4) | (o >> 8);
            destination[1] = o;
            return 2;
        } else if (l == 2) {
            assert(false && "cannot encode a length of 2");
        } else if (l == 1) {
            destination[0] = getByte();
            return 1;
        } else {
            assert(false && "cannot encode a length of zero");
        }
		return 0;
    }

    // Calculate a cost for a single match (not counting any other matches that would follow after it)
    // length: the number of uncompressed bytes consumed by this match
    inline static constexpr uint32_t getCost(uint32_t length) {
        if (length > MATCH_MAX) {
            assert(false && "length too long");
        } else if (length >= 273) {
            return 4;
        } else if (length >= 17) {
            return 3;
        } else if (length >= 3) {
            return 2;
        } else if (length == 2) {
            assert(false && "cannot encode a length of 2");
        } else if (length == 1) {
            return 1;
        } else {
            assert(false && "cannot encode a length of zero");
        }
		return 0;
    }
};

// Accepts matches and buffers them to be written in groups of 8
struct BufferedMatchWriter {
    uint8_t *compressed;       // where compressed bytes will be written
    uint32_t outIdx;           // offset into "compressed" whee the next write will occur
    uint32_t uncompressedIdx;  // number of uncompressed bytes now represented in "compressed" (updated during flush)
    uint32_t allMatchesEver;   // count of all matches ever passed into this instance
    const Match *matches[8];   // buffer of up to 8 matches waiting to be written
    uint32_t length;           // number of matches waiting in "matches"
    bool outputAll8;           // output 8 matches, even if flushing fewer than 8

    BufferedMatchWriter(uint8_t *compressed, uint32_t outIdx, bool outputAll8) {
        this->compressed = compressed;
        this->outIdx = outIdx;
        this->outputAll8 = outputAll8;
        uncompressedIdx = 0;
        length = 0;
        allMatchesEver = 0;
    }

    void flush() {
        if (length == 0) {
            return;  // nothing to flush
        }

        // Calculate the flags prefix byte for this group of 8
        uint_fast8_t flags = 0;
        for (uint32_t i = 0; i < length; ++i) {
            flags |= (matches[i]->getLength() > 1) << (7 - i);
        }

        // Write the flags
        compressed[outIdx++] = flags;

        // Write the matches
        for (uint32_t i = 0; i < length; ++i) {
            const auto &match = *matches[i];
            outIdx += match.encode(compressed + outIdx, uncompressedIdx);
            uncompressedIdx += match.getLength();
        }

        if (outputAll8) {
            // Write dummy matches (if needed to add up to 8)
            for (uint32_t i = length; i < 8; ++i) {
                compressed[outIdx++] = 0;
            }
        }

        // Reset for next time
        length = 0;
    }

    // Add a match to the buffer
    // match: the Match (must not be deallocated, because this only stores a pointer to it not a copy)
    inline void write(const Match &match) {
        // If the buffer is full, flush it
        if (length >= 8) {
            flush();
        }

#if DEBUG_PRINTS
        printf("    encoding length=%u\n", match.length);
#endif

        matches[length++] = &match;
        ++allMatchesEver;
    }
};

// Caches locations of trigrams to find matches
struct TrigramFinder {
    const uint8_t *haystack;  // all uncompressed bytes
    uint32_t haystackSize;    // length of "haystack"
    bool vramSafe;

    // kaystack is split into groups of TRIGRAM_BLOCK_SIZE
    // then each group maps a trigram to a vector of locations within that block
    vector<unordered_map<uint32_t, vector<uint32_t>>> internal;

    TrigramFinder(const uint8_t *haystack, uint32_t haystackSize, bool vramSafe) {
        this->haystack = haystack;
        this->haystackSize = haystackSize;
        this->vramSafe = vramSafe;

        const uint32_t totalPages = (haystackSize >> TRIGRAM_BLOCK_SHIFT) + 1;
        internal.resize(totalPages);
        if (haystackSize < 3) {
            return;  // give up on finding any trigrams, too small
        }

        //#pragma omp parallel for
        for (uint32_t blockIdx = 0; blockIdx < totalPages; ++blockIdx) {
            uint32_t byteIdx = blockIdx << TRIGRAM_BLOCK_SHIFT;
            uint32_t trigram = (haystack[byteIdx] << 16) | (haystack[byteIdx + 1] << 8);
            auto &thisBlock = internal[blockIdx];
            const uint32_t max = byteIdx + TRIGRAM_BLOCK_SIZE < haystackSize - 2 ? byteIdx + TRIGRAM_BLOCK_SIZE : haystackSize - 2;
            for (; byteIdx < max; ++byteIdx) {
                trigram = (trigram | haystack[byteIdx + 2]) << 8;
                thisBlock[trigram].push_back(byteIdx);
            }
        }
    }

private:
    // Find the length of the greatest common prefix between first and second
    static size_t GetMatchLen(const void *first, const void *second, size_t maxLen) {
        size_t matchedSoFar = 0;
        size_t remaining = maxLen;

        // Compare 8 bytes at a time for speed
        while (remaining >= 8 && *(uint64_t*)first == *(uint64_t*)second) {
            remaining -= 8;
            matchedSoFar += 8;
            first = ((uint64_t*)first) + 1;
            second = ((uint64_t*)second) + 1;
        }

        // Compare byte-by-byte
        while (remaining > 0 && *(uint8_t*)first == *(uint8_t*)second) {
            --remaining;
            ++matchedSoFar;
            first = ((uint8_t*)first) + 1;
            second = ((uint8_t*)second) + 1;
        }

        return matchedSoFar;
    }

public:
    // Given the offset a needle, returns its longest Match
    inline Match operator[] (uint32_t referenceIdx) const {
        // Create the Match we'll be returning
        Match match(0, 1, UINT32_MAX, haystack[referenceIdx]);

        if (referenceIdx >= MIN_OFFSET && referenceIdx <= haystackSize - 3) {
            const uint32_t minOffset = (!vramSafe || !(referenceIdx & 1)) ? 1 : 2;
            const uint32_t minPossibleByteIdx = referenceIdx > MAX_OFFSET ? referenceIdx - MAX_OFFSET : 0;
            const uint32_t maxPossibleByteIdx = referenceIdx > minOffset ? referenceIdx - minOffset : 0;

            const uint32_t minPossibleBlockIdx = minPossibleByteIdx >> TRIGRAM_BLOCK_SHIFT;
            const uint32_t maxPossibleBlockIdx = maxPossibleByteIdx >> TRIGRAM_BLOCK_SHIFT;

            const auto key = makeTrigramKey(
                haystack[referenceIdx],
                haystack[referenceIdx + 1],
                haystack[referenceIdx + 2]
            );

            for (uint32_t blockIdx = minPossibleBlockIdx; blockIdx <= maxPossibleBlockIdx; ++blockIdx) {
                const auto &m = internal[blockIdx];  // get the map for this block
                const auto it = m.find(key);         // get an iterator hopefully pointing to a vector
                // If this block contains our trigram
                if (it != m.end()) {
                    // Loop over locations where the trigram is found
                    for (uint32_t byteIdx : it->second) {
                        if (byteIdx >= minPossibleByteIdx && byteIdx <= maxPossibleByteIdx) {
                            uint32_t matchLen = 3;  // having found the trigram makes this at least a match of 3 bytes
                            ptrdiff_t maxLen = (ptrdiff_t)haystackSize - (ptrdiff_t)referenceIdx - 3;
                            if (maxLen > 0) {
                                if (maxLen > MATCH_MAX - 3) maxLen = MATCH_MAX - 3;
                                matchLen += GetMatchLen(haystack + referenceIdx + 3, haystack + byteIdx + 3, maxLen);
                            }
/*#if DEBUG_PRINTS
                            if (referenceIdx < 3) {
                                printf("    at %u considering match.length=%u from %u (needle.len=%d)\n", referenceIdx, matchLen, byteIdx, (int)maxLen+3);
                            }
#endif*/
                            // If this match is the best so far, record it
                            if (match.getLength() < matchLen) {
                                /*if (memcmp(haystack + referenceIdx, haystack + byteIdx, matchLen)) {
                                    printf("    BAD GetMatchLen!!!\n");
                                    continue;
                                }*/

                                match.setLength(matchLen);
                                match.setStart(byteIdx);

                                // Possible opportunistic optimization:
                                if (matchLen == maxLen + 3) {
                                    return match;
                                }
                            }
                        }
                    }  // Loop over locations where the trigram is found
                }  // If this block contains our trigram
            }  // loop over blocks
        }

        return match;
    }
};

extern "C" int compressor(const uint8_t *uncompressed, unsigned uncompressedLength, uint8_t *compressed, unsigned flags) {
    Match *matches = (Match *)malloc(sizeof(Match) * uncompressedLength);

#if PROGRESS_PRINTS
    puts("Finding trigrams... ");
#endif
    // Cache the locations of all trigrams
    const TrigramFinder finder(uncompressed, uncompressedLength, (flags & COMPRESS_VRAM_SAFE) != 0);
#if PROGRESS_PRINTS
    puts("done.\n");
#endif

#if PROGRESS_PRINTS
    int lastPercent = -1;

    printf("Initializing %u matches to longest...\n", uncompressedLength);
#endif

    // Initialize all matches to their longest values
    #pragma omp parallel for
    for (uint32_t i = 0; i < uncompressedLength; ++i) {
#if PROGRESS_PRINTS
        int percent = (100 * (int)i) / (int)uncompressedLength;
        if (lastPercent != percent) {
            lastPercent = percent;
            printf("\r%d%% (%u)", percent, i);
            fflush(stdout);
        }
#endif

        matches[i] = finder[i];
    }

#if PROGRESS_PRINTS
    puts("\r100%\n");
#endif

#if PROGRESS_PRINTS
    puts("Adjusting matches...");
    lastPercent = -1;
#endif

    // Adjust matches in case it's somehow better to use a shorter match
    for (int i = (int)uncompressedLength - 1; i >= 0; --i) {
#if PROGRESS_PRINTS
        int percent = (100 * (uncompressedLength - 1 - i)) / uncompressedLength;
        if (lastPercent != percent) {
            lastPercent = percent;
            printf("\r%d%%", percent);
            fflush(stdout);
        }
#endif

        auto &match = matches[i];
        if (i + match.getLength() >= uncompressedLength) {
            match.setCost(Match::getCost(match.getLength()));
            continue;
        }
        uint32_t bestLength = 1;
        uint32_t bestCost = matches[i + 1].getCost() + Match::getCost(1);
        for (uint32_t length = 3; length <= match.getLength(); ++length) {
            uint32_t cost = matches[i + length].getCost() + Match::getCost(length);
            if (bestCost > cost) {
                bestCost = cost;
                bestLength = length;
            }
        }
        match.setCost(bestCost);
        match.setLength(bestLength);
    }
#if PROGRESS_PRINTS
    puts("\r100%\n");
#endif

#if DEBUG_PRINTS
    printf("About to encode header with: %u\n", uncompressedLength);
#endif

    // Ouput the header
    compressed[0] = 0x11;
    compressed[1] = uncompressedLength;
    compressed[2] = uncompressedLength >> 8;
    compressed[3] = uncompressedLength >> 16;

#if DEBUG_PRINTS
    printf("    %02x %02x %02x %02x\n", compressed[0], compressed[1], compressed[2], compressed[3]);
#endif

    // Encode the compressed bytes
    BufferedMatchWriter writer(compressed, 4, (flags & COMPRESS_ALL_8) != 0);
    for (uint32_t byteIdx = 0; byteIdx < uncompressedLength; ) {
        const Match &match = matches[byteIdx];
        writer.write(match);
        byteIdx += match.getLength();
    }
    writer.flush();

    if (flags & COMPRESS_ROUND_TO_4) {
        while (writer.outIdx & 0x3) {
            compressed[writer.outIdx++] = '\0';
        }
    }

    free(matches);
    return writer.outIdx;
}

/*if (backrefByte0 >= 0x20) {
    // Range 3-16 backref length.
    len = 1 + (backrefByte0 >> 4);
    // All share the same offset range (0 - 0xFFF), unclear if VRAM safety required.
    offset = ((backrefByte0 & 0x0F) << 8) | backrefByte1;
    consumed = 2;
} else if (backrefByte0 < 0x10) {
    // Range 17-272 backref length.
    len = 17 + ((backrefByte0 & 0xF) << 4) + (backrefByte1 >> 4);
    offset = ((backrefByte1 & 0x0F) << 8) | backrefByte2;
    consumed = 3;
} else { // 0x10 to 0x1F
    // Range 273-65808 backref length.
    len = 273 + ((backrefByte0 & 0xF) << 12) + (backrefByte1 << 4) + (backrefByte2 >> 4);
    offset = ((backrefByte2 & 0x0F) << 8) | backrefByte3;
    consumed = 4;
}*/

/*
4 byte header:
    0x10 = GBA, 0x11 = DS
    3 byte little endian size of uncompressed file
1 byte flags:
    MSB: 1=next bytes are back reference, 0=literal byte
    secondn't most sig bit: next byte
backref:
    variable size length
    offset

0x20 or higher -> 4 bits of match, range 3-16
0x00 to 0x0F -> 8 bits of match, range 17 to 272
0x10 to ox1F -> 16 bits of match, range 273 to 65808
distance is always 0 to 0xFFF
*/


