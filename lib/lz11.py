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
	parser = argparse.ArgumentParser(description = "Encrypts or decrypts files using lz11 compression.\n\nIntended for use as an import; the main function is provided for testing.\nEncodes or decodes one file at a time. Pass -e or -d to indicate which action to take.")
	parser.add_argument("-i", "--input", help="Input file", required=True)
	parser.add_argument("-d", "--decode", help="Decode input", action='store_true')
	parser.add_argument("-e", "--encode", help="Encode input", action='store_true')
	parser.add_argument("-o", "--output", help="Output file", required=True)
	parser.add_argument("-s", "--silent", help="Skip non-error prints", action='store_true')
	
	if len(sys.argv) < 2:
		parser.print_help()
		input("Press any key to exit.")
		quit()
	
	args = parser.parse_args()
		
	if not os.path.exists(args.input):
		print("Error: Input file doesn't exist.")
		quit()
	
	if args.decode == args.encode:
		print("Error: Invalid decode/encode flags. Run with no arguments or with -h to view help.")
		quit()
	
	if not lz11_init("lz11encoder"):
		print("Error: lz11 initialization failed.")
		quit()
	
	try:
		with open(args.input,'rb') as file:
			data = file.read()
	except:
		print("Error: Failed to read from input file.")
		quit()
	
	
	if args.decode:
		if not args.silent:
			print("Decompressing input...")
		try:
			data = lz11_decompress(data)
		except:
			print("Error: Decompression failed.")
			quit()	
	else:
		if not args.silent:
			print("Compressing input...")
		try:
			data = lz11_compress(data)
		except:
			print("Error: Compression failed.")
			quit()
	
	try:
		with open(args.output,'wb') as file:
			file.write(data)
	except:
		print("Error: Failed to write to output file.")
		quit()
	
	if not args.silent:
		print("Operation successful.")
