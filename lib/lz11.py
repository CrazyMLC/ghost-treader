#!/usr/bin/env python3
import os,sys,platform,shutil,argparse
from ctypes import *
from struct import unpack
lz11 = None

def lz11_init(dirpath=os.path.join("lib","lz11encoder")):
	global lz11
	if lz11 == None:
		p = os.path.join(dirpath,"lz11bin.so")
		if not os.path.exists(p):
			p = os.path.join(dirpath,f"lz11_{platform.system()}_x64.so")
				
		try:
			lz11 = CDLL(p,winmode=0)
		except:
			if os.path.exists(p):
				sys.stderr.write("Failed to initialize lz11bin.so binary. Try rebuilding with the Makefile at .\\lib\\lz11encoder\\")
			else:
				sys.stderr.write("Couldn't find lz11bin.so binary. Try rebuilding with the Makefile at .\\lib\\lz11encoder\\")
			return False
	return True

def lz11_compress(input, flags=0b111):
	in_len = len(input)
	output = c_buffer(in_len*2)
	out_len = lz11.compress_nds_lz11(byref(c_buffer(input)),in_len,byref(output),flags)
	return output[:out_len]
	
def lz11_decompress(input):
	in_len = len(input)
	out_len = unpack('<L', input[:4])[0] >> 8
	output = c_buffer(out_len)
	lz11.decompress_nds_lz11(byref(c_buffer(input)),in_len,byref(output))
	return output





if __name__ == "__main__":	
	parser = argparse.ArgumentParser(description = "Encrypts or decrypts files using lz11 compression.")
	parser.add_argument("-i", "--input", help="Input file")
	parser.add_argument("-o", "--output", help="Output file")
	parser.add_argument("-d", "--decode", help="Decode input", action='store_true')
	parser.add_argument("-e", "--encode", help="Encode input", action='store_true')
	
	if len(sys.argv) <= 1:
		parser.print_help()
		input("Press any key to exit.")
		quit()
	
	args = parser.parse_args()
	
	if not os.path.exists(args.input):
		input("==============\nInput file doesn't exist.\n==============\nPress any key to exit.")
		quit()
	
	if args.decode == args.encode:
		print("==============\nInvalid decode/encode flags.\n==============\n")
		parser.print_help()
		input("Press any key to exit.")
		quit()
	
	if not lz11_init("lz11encoder"):
		input("==============\nlz11 initialization failed.\n==============\nPress any key to exit.")
		quit()
	
	try:
		with open(args.input,'rb') as file:
			data = file.read()
	except:
		input("==============\nFailed to read from input file.\n==============\nPress any key to exit.")
		quit()
	
	try:
		if args.decode:
			data = lz11_decompress(data)
		else:
			data = lz11_compress(data)
	except:
		input("==============\nEncoding failed.\n==============\nPress any key to exit.")
		quit()
	
	try:
		with open(args.output,'wb') as file:
			file.write(data)
	except:
		input("==============\nFailed to write to output file.\n==============\nPress any key to exit.")
		quit()
	
	input("Operation successful.\nPress any key to exit.")
