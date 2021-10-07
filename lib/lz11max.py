#!/usr/bin/env python3
import os,sys,platform,shutil,argparse,time
from ctypes import *
from struct import unpack
lz11 = None

def lz11max_init(dirpath=os.path.join("lib","lz11maxcompress")):
	global lz11
	if lz11 == None:
		p = os.path.join(dirpath,"lz11maxbin.so")
		"""
		if not os.path.exists(p):
			p = os.path.join(dirpath,f"lz11_{platform.system()}_x64.so")
			"""	
		try:
			lz11 = CDLL(p,winmode=0)
		except:
			if os.path.exists(p):
				sys.stderr.write("Failed to initialize lz11maxbin.so binary. Try rebuilding with the Makefile at .\\lib\\lz11maxcompress\\")
			else:
				sys.stderr.write("Couldn't find lz11maxbin.so binary. Try rebuilding with the Makefile at .\\lib\\lz11maxcompress\\")
			return False
	return True

def lz11max_compress(input, flags=5):
	in_len = len(input)
	output = c_buffer(in_len*2)
	return output[:lz11.compressor(c_buffer(input),in_len,byref(output),flags)]





if __name__ == "__main__":	
	parser = argparse.ArgumentParser(description = "Encrypts files using slow but optimal lz11 compression.\n\nIntended for use as an import; the main function is provided for testing.\nEncodes or decodes one file at a time.")
	parser.add_argument("-i", "--input", help="Input file", required=True)
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
	
	if not lz11max_init("lz11maxcompress"):
		print("Error: lz11 initialization failed.")
		quit()
	
	
	try:
		with open(args.input,'rb') as file:
			data = file.read()
	except:
		print("Error: Failed to read from input file.")
		quit()
	
	
	if not args.silent:
		print("Compressing input...")
		start = time.perf_counter()
	try:
		data = lz11max_compress(data)
	except:
		print("Error: Compression failed.")
		quit()
	if not args.silent:
		print((time.perf_counter()-start)*1000,"ms")
	
	try:
		with open(args.output,'wb') as file:
			file.write(data)
	except:
		print("Error: Failed to write to output file.")
		quit()
	
	if not args.silent:
		print("Operation successful.")
