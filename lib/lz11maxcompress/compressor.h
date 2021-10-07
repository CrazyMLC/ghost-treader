
#include <cstdint>

#define COMPRESS_VRAM_SAFE 1
#define COMPRESS_ALL_8 2
#define COMPRESS_ROUND_TO_4 4

extern "C" int compressor(const uint8_t *uncompressed, unsigned uncompressedLength, uint8_t *compressed, unsigned flags);