from PIL import Image
import os,sys
"""
balloon_palette = [# colors extracted from editing balloon_font_en.imb and viewing the "So long, sister." in chp1
	(247,247,247),#	0	0000
	(178,178,178),#	1	0001
	(146,146,146),#	2	0010
	(0,0,0),#		3	0011
	(247,247,247),#	4	0100
	(255,105,4),#	5	0101
	(255,186,146),#	6	0110
	(247,247,247),#	7	0111
	(113,40,20),#	8	1000
	(186,56,20),#	9	1001
	(247,113,56),#	a	1010
	(4,48,146),#	b	1011
	(56,121,186),#	c	1100
	(105,195,247),#	d	1101
	(0,89,0),#		e	1110
	(0,154,0)#		f	1111
]
db_palette = [# colors extracted from editing font_db.imb and observing the People/Phone Book
	(12,0,0),#		0	0000
	(12,0,0),#		1	0001
	(48,0,0),#		2	0010
	(65,0,0),#		3	0011
	(73,4,4),#		4	0100
	(121,4,4),#		5	0101
	(162,4,0),#		6	0110
	(48,12,0),#		7	0111
	(81,32,0),#		8	1000
	(105,40,0),#	9	1001
	(121,56,0),#	a	1010
	(138,65,0),#	b	1011
	(170,73,0),#	c	1100
	(195,97,0),#	d	1101
	(211,105,0),#	e	1110
	(255,130,0)#		f	1111
]
"""
palette = [0xf7,0xb2,0x92,0,0xff,0xff,0x1,0xf7,0xd7,0xc2,0xb2,0x92,0x72,0x52,0x32,0]#made this up
palette2 = [0xff,0xcb,0x79,0]# color picked from dialogue box


def read_font(p):
	"""Takes a font .imb file and outputs images of each character."""
	# Is it actually a font file?
	if p[-4:] != ".imb":
		print("Invalid file.")
		return
	# Get the font data.
	with open(p,'rb') as file:
		data = file.read()
	# Set up the folder structure.
	output = os.path.join("font",os.path.splitext(os.path.basename(p))[0])
	if not os.path.exists("font"):
		os.mkdir("font")
	if not os.path.exists(output):
		os.mkdir(output)
	
	# Now we have to figure out if we should run the 2bpp version or the 4bpp version.
	# This is a difficult problem, so let's just trust the filename.
	if "2bpp" in os.path.basename(p):
		font_2bpp(output,data)
	else:
		font_4bpp(output,data)
	
	print("Success.")


def font_4bpp(output,data):
	# Find out the number of characters.
	chars = int(len(data)/128)
	
	for i in range(chars):
		# This bytearray will hold the image data for us until we pass it to PIL.
		char_img = bytearray()
		
		for k in range(128):
			byte = data[i*128 + k]
			# It reads the nibbles in little endian format...
			char_img.append(palette[byte&15])# First the right nibble
			char_img.append(palette[byte>>4])# Then the left nibble
		
		fname = os.path.join(output,f"{i}.png")
		# Now we let PIL make and save the image for us.
		img = Image.frombytes('L',(16,16),bytes(char_img))
		img.save(fname)


def font_2bpp(output,data):
	# Find out the number of characters.
	chars = int(len(data)/96)
	
	for i in range(chars):
		# This bytearray will hold the image data for us until we pass it to PIL.
		char_img = bytearray()
		
		for k in range(96):
			byte = data[i*96 + k]
			# This is 2bpp, so there are four pixels in a byte. Apparently a term for 2 bits is a "crumb"
			crumbs = [(byte>>4)&3, byte>>6, byte&3, (byte>>2)&3]
			# So basically, if we visualize the order that each crumb in the byte is rendered...
			# 0b00000000
			#   B A D C
			# Why is it ordered this way??? ...Okay, fine. Whatever. It's not like it was frustrating or anything, no sir.
			
			# At least now we can write them to the byte array.
			for crumb in crumbs:
				char_img.append(palette2[crumb])
		
		fname = os.path.join(output,f"{i}.png")
		# Now we let PIL make and save the image for us.
		img = Image.frombytes('L',(16,24),bytes(char_img))
		img.save(fname)


if __name__ == "__main__":
	for p in sys.argv[1:]:
		print(p)
		try:
			read_font(p)
		except:
			print("Encountered an error while reading the file.")
		
	input("Press enter to exit")