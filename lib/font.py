from PIL import Image
from io import BytesIO
import os,sys

def read_font(p):
	"""Takes a font .imb file and outputs images of each character."""
	# Is it actually a font file?
	if p[-4:] != ".imb":
		print("Invalid file.")
		return
	# Get the font data.
	with open(p,'rb') as file:
		data = BytesIO(file.read())
	# Set up the folder structure.
	name = os.path.join("font",os.path.splitext(os.path.basename(p))[0])
	if not os.path.exists("font"):
		os.mkdir("font")
	if not os.path.exists(name):
		os.mkdir(name)
	# Find out the number of characters. (maybe the number is always 256, and it changes the height to match?)
	chars = int(data.seek(0,2)/128)
	data.seek(0)
	# Now read the characters and save the images. Pillow makes this very simple.
	for i in range(chars):
		img = Image.frombytes('L',(8,16),data.read(128))
		fname = os.path.join(name,f"{i}.png")
		img.save(fname)
	print("Success.")

if __name__ == "__main__":
	for p in sys.argv[1:]:
		print(p)
		read_font(p)
		
	input("Press enter to exit")