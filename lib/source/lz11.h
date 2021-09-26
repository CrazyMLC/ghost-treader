#pragma once

#include <vector>

enum LZ11Flags {
	LZ11_NORMAL = 0x0000,
	LZ11_FAST = 0x0001,
	LZ11_VRAM_SAFE = 0x0002,
	LZ11_REVERSE = 0x0004,
};

extern "C" int compress_nds_lz11(uint8_t * input_buffer, int input_length, uint8_t * output_buffer, int flags);
extern "C" void decompress_nds_lz11(uint8_t * input_buffer, int input_length, uint8_t * output_buffer);