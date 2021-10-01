import os,sys,platform,shutil
from ctypes import *
from struct import unpack
lz11 = None

def lz11_init(dirpath):
	global lz11
	if lz11 == None:
		p = os.path.join(dirpath,'lz11bin.so')
		if not os.path.exists(p):
			if platform.system() == 'Windows':
				s = os.path.join(dirpath,"source","lz11_win_x64.so")
			elif platform.system() == 'Linux':
				s = os.path.join(dirpath,"source","lz11_linux_x64.so")
			else:
				s = os.path.join(dirpath,"source","lz11bin.so")
			if os.path.exists(s):
				shutil.copy2(s,p)
				
		try:
			lz11 = CDLL(p,winmode=0)
		except:
			if os.path.exists(p):
				sys.stderr.write("Failed to initialize lz11bin.so binary. Try rebuilding with the Makefile at .\\lib\\source\\")
			else:
				sys.stderr.write("Couldn't find lz11bin.so binary. Try rebuilding with the Makefile at .\\lib\\source\\")
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