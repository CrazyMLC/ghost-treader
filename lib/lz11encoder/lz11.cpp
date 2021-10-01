#include <cstdint>
#include <cstdio>
#include <cstring>
#include <unordered_map>
#include <vector>
#include "lz11.h"

class LZ11NDSCompressor {
public:
	LZ11NDSCompressor(const uint8_t *input,  size_t input_size, uint8_t *output) : input_(input), input_size_(input_size), output_(output) {
	}

	size_t Compress(int flags, int max_scenarios);

private:
	constexpr static int MAX_BACKREF_OFFSET = 0xFFF;
	constexpr static int MIN_BACKREF_LEN = 1 + 0x2;
	constexpr static int MAX_BACKREF_LEN = 0x10110;
	constexpr static int INDEX_HORIZON_DIST = 0x4000;

	struct Scenario {
		Scenario() {
		}
		explicit Scenario(int w) : waste(w) {
		}

		int waste = 1;
		int backref_offset = 0;
		int backref_len = 0;
		int saved_bytes = 0;
	};

	void CompressReverse(int max_scenarios);
	void CompressForward(int max_scenarios);

	void BuildIndex(uint32_t newHorizon);
	inline bool IndexContains(uint32_t src, int range);
	Scenario TryReverseWaste(uint32_t src, int waste);
	Scenario TryForwardWaste(uint32_t src, int waste);

	const uint8_t *input_;
	const size_t input_size_;
	uint8_t *output_;
	size_t outpos_ = 0;
	std::unordered_map<uint32_t, std::vector<uint32_t>> index_;
	uint32_t indexHorizon_ = 0xFFFFFFFF;
	int flags_ = 0;
};

size_t LZ11NDSCompressor::Compress(int flags, int max_scenarios) {
	outpos_ = 0;

	// Before any compression, validate the size can be supported.
	if (input_size_ > 0x00FFFFFF) {
		fprintf(stderr, "Input data too big to compress via LZ11.\n");
		return outpos_;
	}

	flags_ = flags;
	if (flags & LZ11_REVERSE) {
		CompressReverse(max_scenarios);
	} else {
		CompressForward(max_scenarios);
	}

	return outpos_;
}

void LZ11NDSCompressor::BuildIndex(uint32_t newHorizon) {
	if (input_size_ - newHorizon < 3) {
		return;
	}
	index_.clear();

	uint32_t hash = (input_[newHorizon] << 16) | (input_[newHorizon + 1] << 8);
	uint32_t end = newHorizon + INDEX_HORIZON_DIST + 1;
	if (end > (uint32_t)input_size_)
		end = (uint32_t)input_size_;
	for (uint32_t i = newHorizon + 2; i < end; ++i) {
		hash = (hash | input_[i]) << 8;
		index_[hash].push_back(i);
	}

	indexHorizon_ = newHorizon;
}

bool LZ11NDSCompressor::IndexContains(uint32_t src, int range) {
	uint32_t earliest = src > (uint32_t)MAX_BACKREF_OFFSET - range ? src - MAX_BACKREF_OFFSET - 1 - range : 0;
	if (earliest < indexHorizon_) {
		return false;
	}
	return src < indexHorizon_ + INDEX_HORIZON_DIST - range;
}

LZ11NDSCompressor::Scenario LZ11NDSCompressor::TryReverseWaste(uint32_t src, int waste) {
	Scenario plan{ waste };
	// Start out in debt, our match has to save more.
	plan.saved_bytes = -2 - waste;
	if ((uint32_t)waste + MIN_BACKREF_LEN >= src) {
		return plan;
	}

	// According to this plan, our buffer will END at this position.
	src -= waste;

	// We have at most this many bytes to encode.
	int left = src - MIN_BACKREF_LEN > MAX_BACKREF_LEN ? MAX_BACKREF_LEN : src - MIN_BACKREF_LEN;
	if (left < MIN_BACKREF_LEN) {
		return plan;
	}

	int best_offset = 0;
	int best_len = 0;

	uint32_t hash = (input_[src - 3] << 24) | (input_[src - 2] << 16) | (input_[src - 1] << 8);
	const bool checkVRAM = (flags_ & LZ11_VRAM_SAFE) != 0;
	const auto &matches = index_.at(hash);
	for (size_t i = 0; i < matches.size(); ++i) {
		const uint32_t found_pos = matches[i];
		if (found_pos >= src - 1) {
			break;
		}
		if (found_pos + MAX_BACKREF_OFFSET < src - 1) {
			continue;
		}

		int found_off = src - 1 - found_pos;
		if (checkVRAM && found_off <= 1) {
			continue;
		}

		// How long is this match?  We only looked for three bytes so far.
		int found_len = 3;
		int max_len = found_pos >= (size_t)left ? left : (int)found_pos;
		for (int j = found_len; j < max_len; ++j) {
			if (input_[found_pos - j] != input_[src - j - 1]) {
				break;
			}
			found_len++;
		}

		if (found_len > best_len) {
			// Maybe this is the one?
			best_len = found_len;
			best_offset = found_off;
			if (found_len == MAX_BACKREF_LEN) {
				break;
			}
		}
	}

	if (best_len >= MIN_BACKREF_LEN) {
		// Alright, this is our best shot.
		plan.backref_offset = best_offset - 1;
		plan.backref_len = best_len;
		plan.saved_bytes += best_len;
		if (best_len > 16) {
			plan.saved_bytes--;
		}
		if (best_len > 272) {
			plan.saved_bytes--;
		}
	}
	return plan;
}

void LZ11NDSCompressor::CompressReverse(int max_scenarios) {
	std::vector<std::vector<uint8_t>> chunks;
	// This is the worst case.
	chunks.reserve(input_size_);

	// Start at the END, and build the file backwards.
	// This gives us the smartest backreference decisions.
	std::ptrdiff_t total_saved = 0;
	size_t compressed_size = 0;
	for (uint32_t src = (uint32_t)input_size_; src > 0; ) {
		if (src == 0 || src > input_size_) {
			break;
		}

		if (!IndexContains(src, -max_scenarios)) {
			BuildIndex(src > INDEX_HORIZON_DIST ? src - INDEX_HORIZON_DIST : 0);
		}

		// Default plan is no backref.
		Scenario plan;

		// Play Chess.  Is it smarter to waste a byte now to save one later?
		for (int s = 0; s < max_scenarios; ++s) {
			Scenario option = TryReverseWaste(src, s);
			if (option.saved_bytes > plan.saved_bytes) {
				plan = option;
				// If any plan wasting a byte is better, go with it.
				// We don't need to examine future plans, since we'll do this next byte.
				if (s != 0) {
					break;
				}
				// If this is already ideal, we're done.
				if (plan.backref_len == MAX_BACKREF_LEN) {
					break;
				}
			} else if (s == 0) {
				// Won't save, no sense checking other scenarios.
				break;
			}
		}

		if (plan.waste != 0) {
			for (int i = 0; i < plan.waste; ++i) {
				chunks.push_back({ input_[--src] });
				compressed_size++;
			}
		} else {
			if (plan.backref_len < 17) {
				uint8_t byte1 = ((plan.backref_len - 1) << 4) | (plan.backref_offset >> 8);
				uint8_t byte2 = plan.backref_offset & 0xFF;
				chunks.push_back({ byte1, byte2 });
				compressed_size += 2;
			} else if (plan.backref_len < 273) {
				uint8_t byte1 = 0x00 | ((plan.backref_len - 17) >> 4);
				uint8_t byte2 = (((plan.backref_len - 17) & 0x0F) << 4) | (plan.backref_offset >> 8);
				uint8_t byte3 = plan.backref_offset & 0xFF;
				chunks.push_back({ byte1, byte2, byte3 });
				compressed_size += 3;
			} else {
				uint8_t byte1 = 0x10 | ((plan.backref_len - 273) >> 12);
				uint8_t byte2 = ((plan.backref_len - 273) >> 4) & 0xFF;
				uint8_t byte3 = (((plan.backref_len - 273) & 0x0F) << 4) | (plan.backref_offset >> 8);
				uint8_t byte4 = plan.backref_offset & 0xFF;
				chunks.push_back({ byte1, byte2, byte3, byte4 });
				compressed_size += 4;
			}
			total_saved += plan.saved_bytes;
			src -= plan.backref_len;
		}
	}

	compressed_size += (chunks.size() + 7) / 8;
	// TODO: Not sure.
	//compressed_size += chunks.size() & 7;

	output_[0] = 0x11;
	output_[1] = (input_size_ >> 0) & 0xFF;
	output_[2] = (input_size_ >> 8) & 0xFF;
	output_[3] = (input_size_ >> 16) & 0xFF;

	// Time to reverse the chunks and insert the flags.
	size_t pos = 4;
	for (size_t i = 0; i < chunks.size(); i += 8) {
		uint8_t *quadflags = &output_[pos++];
		uint8_t nowflags = 0;
		for (int j = 0; j < 8 && i + j < chunks.size(); ++j) {
			const auto &chunk = chunks[chunks.size() - i - j - 1];
			if (chunk.size() == 1) {
				output_[pos++] = chunk[0];
			} else {
				nowflags |= 0x80 >> j;
				for (uint8_t k = 0; k < chunk.size(); ++k) {
					output_[pos++] = chunk[k];
				}
			}
		}
		*quadflags = nowflags;
	}

	outpos_ = (compressed_size + 4 + 3) & ~3;
}

LZ11NDSCompressor::Scenario LZ11NDSCompressor::TryForwardWaste(uint32_t src, int waste) {
	Scenario plan{ waste };
	// Start out in debt, our match has to save more.
	plan.saved_bytes = -2 - waste;
	// According to this plan, we'll have this many src bytes to match.
	src += waste;

	if (src == 0 || (size_t)src + waste >= input_size_) {
		return plan;
	}

	// We have at most this many bytes to encode.
	int left = input_size_ - src > MAX_BACKREF_LEN ? MAX_BACKREF_LEN : (int)(input_size_ - src);
	if (left < MIN_BACKREF_LEN) {
		return plan;
	}

	int best_offset = 0;
	int best_len = 0;

	uint32_t hash = (input_[src] << 24) | (input_[src + 1] << 16) | (input_[src + 2] << 8);
	const bool checkVRAM = (flags_ & LZ11_VRAM_SAFE) != 0;
	const auto &matches = index_.at(hash);
	for (size_t i = 0; i < matches.size(); ++i) {
		const uint32_t found_pos = matches[i];
		if (found_pos >= src) {
			break;
		}
		if (found_pos + MAX_BACKREF_OFFSET < src) {
			continue;
		}

		int found_off = src - found_pos;
		if (checkVRAM && found_off <= 1) {
			continue;
		}

		// How long is this match?  We only looked for three bytes so far.
		int found_len = 3;
		for (int j = found_len; j < left; ++j) {
			if (input_[found_pos + j] != input_[src + j]) {
				break;
			}
			found_len++;
		}

		if (found_len > best_len) {
			// Maybe this is the one?
			best_len = found_len;
			best_offset = found_off;
			if (found_len == MAX_BACKREF_LEN) {
				break;
			}
		}
	}

	if (best_len >= MIN_BACKREF_LEN) {
		// Alright, this is our best shot.
		plan.backref_offset = best_offset - 1;
		plan.backref_len = best_len;
		plan.saved_bytes += best_len;
		if (best_len > 16) {
			plan.saved_bytes--;
		}
		if (best_len > 272) {
			plan.saved_bytes--;
		}
	}
	return plan;
}

void LZ11NDSCompressor::CompressForward(int max_scenarios) {
	uint8_t *pos = output_;

	// Now the header, method 0x11 + size << 4, in LE.
	*pos++ = 0x11;
	*pos++ = (input_size_ >> 0) & 0xFF;
	*pos++ = (input_size_ >> 8) & 0xFF;
	*pos++ = (input_size_ >> 16) & 0xFF;

	std::ptrdiff_t total_saved = 0;
	for (uint32_t src = 0; src < (uint32_t)input_size_; ) {
		uint8_t *quadflags = pos++;
		uint8_t nowflags = 0;

		for (int i = 0; i < 8; ++i) {
			if (src >= input_size_) {
				*pos++ = 0;
				continue;
			}

			if (!IndexContains(src, max_scenarios)) {
				BuildIndex(src > MAX_BACKREF_OFFSET - 1 ? src - MAX_BACKREF_OFFSET - 1 : 0);
			}

			// Default plan is no backref.
			Scenario plan;

			// Play Chess.  Is it smarter to waste a byte now to save one later?
			for (int s = 0; s < max_scenarios; ++s) {
				Scenario option = TryForwardWaste(src, s);
				if (option.saved_bytes >= plan.saved_bytes) {
					plan = option;
					// If any plan wasting a byte is better, go with it.
					// We don't need to examine future plans, since we'll do this next byte.
					if (s != 0) {
						break;
					}
					// This is good enough, let's not keep looking.  Might be worse.
					// TO DO: Increase.
					//if (plan.backref_len >= 13) {
					if (plan.backref_len == MAX_BACKREF_LEN) {
						break;
					}
				} else if (s == 0) {
					// Won't save, no sense checking other scenarios.
					break;
				}
			}

			if (plan.waste != 0) {
				for (int j = 0; j < plan.waste && i < 8; ++j) {
					*pos++ = input_[src++];
					i++;
				}
				// We increased this one extra.
				i--;
			} else {
				if (plan.backref_len < 17) {
					*pos++ = ((plan.backref_len - 1) << 4) | (plan.backref_offset >> 8);
					*pos++ = plan.backref_offset & 0xFF;
				} else if (plan.backref_len < 273) {
					*pos++ = 0x00 | ((plan.backref_len - 17) >> 4);
					*pos++ = (((plan.backref_len - 17) & 0x0F) << 4) | (plan.backref_offset >> 8);
					*pos++ = plan.backref_offset & 0xFF;
				} else {
					*pos++ = 0x10 | ((plan.backref_len - 273) >> 12);
					*pos++ = ((plan.backref_len - 273) >> 4) & 0xFF;
					*pos++ = (((plan.backref_len - 273) & 0x0F) << 4) | (plan.backref_offset >> 8);
					*pos++ = plan.backref_offset & 0xFF;
				}
				total_saved += plan.saved_bytes;
				src += plan.backref_len;
				nowflags |= 0x80 >> i;
			}
		}

		*quadflags = nowflags;
		total_saved--;
	}

	size_t len = pos - output_;
	outpos_ = (len + 3) & ~3;
}

extern "C" int compress_nds_lz11(uint8_t * input_buffer, int input_length, uint8_t * output_buffer, int flags) {
	if (flags & LZ11_FAST) {
		LZ11NDSCompressor engine(input_buffer, input_length, output_buffer);
		return engine.Compress(flags, 2);
	}

	// Try to compress as well as possible to fit more in the same space.
	size_t best_size = 0;
	std::vector<uint8_t> buffer;
	buffer.resize(input_length * 2);

	for (int s = 0; s < 4; ++s) {
		LZ11NDSCompressor engine(input_buffer, input_length, buffer.data());

		size_t trial = engine.Compress(flags & ~LZ11_REVERSE, s);
		if (trial < best_size || best_size == 0) {
			if (best_size < (size_t)input_length * 2) {
				best_size = trial;
				memcpy(output_buffer, buffer.data(), best_size);
			}
		}

		trial = engine.Compress(flags | LZ11_REVERSE, s);
		if (trial < best_size || best_size == 0) {
			if (best_size < (size_t)input_length * 2) {
				best_size = trial;
				memcpy(output_buffer, buffer.data(), best_size);
			}
		}
	}

	return best_size;
}

extern "C" void decompress_nds_lz11(uint8_t * input_buffer, int input_length, uint8_t * output_buffer) {
	std::vector<uint8_t> input(input_buffer, input_buffer + input_length);

	if (input.size() < 4 || input[0] != 0x11) {
		fprintf(stderr, "Input data too small to decompress via LZ11 (%d / %02x)\n", (int)input.size(), input[0]);
		return;
	}

	uint32_t sz = input[1] | (input[2] << 8) | (input[3] << 16);

	uint32_t outpos = 0;
	size_t inpos = 4;
	while (outpos < sz && inpos < input.size()) {
		uint8_t quad = input[inpos++];
		if (quad == 0 && outpos + 8 <= sz && inpos + 8 <= (size_t)input_length) {
			memcpy(&output_buffer[outpos], &input[inpos], 8);
			inpos += 8;
			outpos += 8;
			continue;
		}
		for (uint8_t bit = 0x80; bit != 0; bit >>= 1) {
			if ((quad & bit) != 0 && inpos + 1 < (size_t)input_length) {
				uint32_t offset, len;
				if (input[inpos + 0] >= 0x20) {
					offset = ((input[inpos + 0] & 0x0F) << 8) | input[inpos + 1];
					len = 1 + (input[inpos + 0] >> 4);
					inpos += 2;
				} else if ((input[inpos + 0] & 0xF0) == 0x0) {
					if (inpos + 2 >= (size_t)input_length)
						continue;
					offset = ((input[inpos + 1] & 0x0F) << 8) | input[inpos + 2];
					len = 17 + (((input[inpos + 0] & 0x0F) << 4) | (input[inpos + 1] >> 4));
					inpos += 3;
				} else {
					if (inpos + 3 >= (size_t)input_length)
						continue;
					offset = ((input[inpos + 2] & 0x0F) << 8) | input[inpos + 3];
					len = 273 + (((input[inpos + 0] & 0x0F) << 12) | (input[inpos + 1] << 4) | (input[inpos + 2] >> 4));
					inpos += 4;
				}

				if (len > sz - outpos) {
					len = sz - outpos;
				}

				uint32_t srcpos = outpos - 1 - offset;
				for (uint32_t i = 0; i < len; ++i) {
					output_buffer[outpos++] = output_buffer[srcpos + i];
				}
			} else if (outpos < sz && inpos < (size_t)input_length) {
				output_buffer[outpos++] = input[inpos++];
			} else {
				break;
			}
		}
	}
}
