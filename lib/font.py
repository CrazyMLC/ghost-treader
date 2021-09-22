from PIL import Image
import os,sys
"""
palette = [# colors extracted from editing balloon_font_en.imb, but doesn't seem to match font_db.imb
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
"""
palette = [0xf7,0xb2,0x92,0,0,0,0,0xf7,0xe7,0xd2,0xc2,0xa2,0x92,0x62,0x42,0]#made this up

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
	# Find out the number of characters. (maybe the number is always 256, and it changes the height to match?)
	chars = int(len(data)/128)
	# Now read the characters and save the images. Pillow makes this very simple.
	for i in range(chars):
		#This bytearray will hold the image data for us until we pass it to PIL.
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
	print("Success.")

if __name__ == "__main__":
	for p in sys.argv[1:]:
		print(p)
		read_font(p)
		
	input("Press enter to exit")