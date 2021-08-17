from io import BytesIO
from struct import unpack
import sys,os,time

from tables import *
from message import *

def decode_1LMG(filepath):
	"""Open, decode, and print a 1LMG file at the given filepath."""
	with open(filepath, 'rb') as text_file:
		data = text_file.read()
	data = BytesIO(data)
	
	if data.read(4) != b'1LMG':
		return "File isn't 1LMG"

	# Let's find all the important file locations
	mystery, = unpack('<L', data.read(4))# Seems to have something to do with scripts...
	footer_offset, = unpack('<L', data.read(4))
	pointers_offset, = unpack('<L', data.read(4))

	footer_position = 0x34 + footer_offset
	pointers_position = footer_position + pointers_offset

	data.seek(pointers_position)
	message_count, = unpack('<L', data.read(4))

	if message_count == 0:
		return "File has no messages"

	labels_offset = 4+message_count*8
	labels_position = labels_offset + pointers_position
	
	# Alright. Now we know all the locations within the file, so let's start reading data.
	# We're already here, so let's read the footer's pointer table.
	messages = []
	for m in range(message_count):
		messages.append(
			Message( *unpack('<LL', data.read(8)) )
		)
		# Scripts don't use stop codes necessarily, so we'll have to calculate lengths for each message.
		if m > 0:
			messages[m-1].length = messages[m].pointer - messages[m-1].pointer
	messages[-1].length = footer_position - messages[-1].pointer

	# Now, let's get the data from the pointers we found.
	for message in messages:
		# We'll let the message class handle the data.
		message.get_label(data, labels_position)
		message.decode(data)
		
	# Sometimes the last message in a file will have a lingering 0x0000 in order to 4byte-align the pointer table.
	# Can't necessarily tell when it's part of the message or not, but we can easily cut it out for dialogue files.
	if pointers_offset == 4:# Most if not all script files have a higher offset, so we can use this to identify dialogue files.
		if messages[-1].decoded[-(1+len(commands[0xfffe])):] == commands[0xfffe]+'0':
			messages[-1].decoded = messages[-1].decoded[:-1]
	
	# We're done! Let's print each message using the message class's string conversion function.
	print(*messages, sep='')

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
	output = "decoded"
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
			if sys.argv[v-1] != "--view":
				original_stdout = sys.stdout
				new_file = "{}.txt".format(os.path.join(output,os.path.basename(sys.argv[v])))
				f = open(new_file, 'w', encoding="utf8")
				sys.stdout = f
			e = decode_1LMG(sys.argv[v])
			if sys.argv[v-1] != "--view":
				sys.stdout = original_stdout
				f.close()
			if e == None:
				successful += 1
			else:
				errors += f"{e}: {os.path.basename(sys.argv[v])}\n"
			continue
		elif not sys.argv[v] == "--view":
			errors += f"Couldn't process command: {sys.argv[v]}\n"
	printProgressBar(1,1)
	print(errors)
	print("Successfully decoded {0} file{1} in {2:.1f}ms".format(successful,("" if (successful==1) else "s"),(time.perf_counter()-start)*1000))
	input("Press enter to exit")
	