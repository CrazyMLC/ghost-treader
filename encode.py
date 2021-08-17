from io import BytesIO
from struct import pack
import sys,os,time

from tables import *
from message import *

def encode_1LMG(loadpath, savepath):
	"""Open, encode, and save a text file as a 1LMG file."""
	with open(loadpath, 'r', encoding="utf-8") as text_file:
		data = text_file.read()
	# First we have to clean off the '====' lines, and separate the list.
	data = data.split('=\n')[1:]
	if (len(data) % 2) != 0:
		return "Mismatching number of labels and messages"
	for i in range(len(data)):
		line = data[i]
		if line[-1] == "=":
			data[i] = line[:line.rfind('\n')]
	# Then we extract the data and put it into a message list.
	messages = []
	for i in range(0,len(data),2):
		data[i] = data[i].split(" Position")[0]# Take out the position information, it's not relevant to encoding.
		m = Message()
		if data[i].count(' ') > 0:
			return f'Label "{data[i][:20]}" contains a space'
		m.label = data[i]
		m.decoded = data[i+1]
		m.pointer = 0
		messages.append(m)

	# Alright, we have all the input information. Time to start building the file.
	header = BytesIO(b'1LMG')
	header.seek(0,2)
	header.write(bytes(4))# Write the "mystery" bytes as blank, for now.
	
	data = BytesIO()
	
	strings = BytesIO(b'*'+bytes(3))# Placeholder command. Don't actually know how this section works yet; it's used for scripts.
	
	table = BytesIO()
	table.write( pack('<L',len(messages)) )
	
	labels = BytesIO()
	labels.write(b'*'+bytes(1))
	# We're gonna loop through each message, and populate each section of the file as we go.
	for message in messages:
		table.write( pack('<LL', labels.seek(0,2), data.seek(0,2) + 0x34) )
		e = message.encode()
		if type(e) is str:
			print("\n"+e)
			return "File had encoding error"
		data.write(e)
		labels.write(message.label.encode() + bytes(1))
	# Let's make sure that each sections is a multiple of 4 bytes.
	temp = data.seek(0,2) % 4
	data.write(bytes(4-temp))
	
	temp = labels.seek(0,2) % 4
	labels.write(bytes(4-temp))
	# Now we fill in the header...
	header.write( pack('<LLL', data.seek(0,2), strings.seek(0,2), table.seek(0,2)+labels.seek(0,2)) )
	header.write(bytes(0x20))
	# Well, that was easy. Time to save the file.
	with open(savepath, 'wb') as text_file:
		header.seek(0)
		text_file.write(header.read())
		data.seek(0)
		text_file.write(data.read())
		strings.seek(0)
		text_file.write(strings.read())
		table.seek(0)
		text_file.write(table.read())
		labels.seek(0)
		text_file.write(labels.read())
	
	
	
def printProgressBar (iteration, total):
	"""Based on stack overflow 'Text Progress Bar in the Console [closed]'"""
	percent = "{0:.1f}".format(100 * (iteration / float(total)))
	filledLength = int(100 * iteration // total)
	bar = '█' * filledLength + '-' * (100 - filledLength)
	print(f'\r|{bar}| {percent}%', end = "\r")
	if iteration == total: 
		print()
		
if __name__ == "__main__":
	start = time.perf_counter()
	output = "encoded"
	if not os.path.isdir(output):
		os.mkdir(output)
	successful = 0
	errors = ""
	for v in range(1,len(sys.argv)):
		printProgressBar(v-1,len(sys.argv)-1)
		if sys.argv[v] == "--output":
			if os.path.isdir(sys.argv[v+1]):
				output = sys.argv[v+1]
				continue
			errors += f"Invalid output folder: {sys.argv[v+1]}\n"
			break
		elif os.path.isfile(sys.argv[v]):
			new_file = os.path.basename(sys.argv[v])
			new_file = new_file[:new_file.rfind('.')]
			new_file = os.path.join(output,new_file)
			e = encode_1LMG(sys.argv[v],new_file)
			if e == None:
				successful += 1
			else:
				errors += f"{e}: {os.path.basename(sys.argv[v])}\n"
			continue
		else:
			errors += f"Couldn't process command: {sys.argv[v]}\n"
	printProgressBar(1,1)
	print(errors)
	print("Successfully encoded {0} file{1} in {2:.1f}ms".format(successful,("" if (successful==1) else "s"),(time.perf_counter()-start)*1000))
	input("Press enter to exit")