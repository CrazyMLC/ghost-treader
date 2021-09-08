from io import BytesIO
from struct import pack
import sys,os,time,argparse

from tables import *
from message import *

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Encodes decoded 1LMG files back into 1LMG.")
	parser.add_argument("-i", "--input", help="Input files or folder, output must be a folder for multiple files", nargs='*')
	parser.add_argument("-o", "--output", help="Output file or folder", default=os.path.join(".","encoded",""))
	parser.add_argument("-e", "--error", help="Error file")
	parser.add_argument("-w", "--wildcard", help="Filters folder contents. separate mandatory name sections with *")
	parser.add_argument("-s", "--silent", help="Skip prints", action='store_true')
	parser.add_argument("-v", "--verbose", help="Wait for confirm", action='store_true')
	parser.add_argument("dragged", help="Catches dragged and dropped files", nargs='*')



def encode_1LMG(loadpath, savepath):
	"""Open, encode, and save a text file as a 1LMG file."""
	with open(loadpath, 'r', encoding="utf-8") as text_file:
		data = text_file.read()
	# First we have to clean off the '====' lines, and separate the list.
	data = data.split('=\n')[1:]
	if (len(data) % 2) != 0:
		sys.stderr.write(f"Mismatching number of labels and messages: {loadpath}\n")
		return -1
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
			sys.stderr.write(f'Label "{data[i][:20]}" contains a space: {loadpath}\n')
			return -2
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
			sys.stderr.write(f"File had encoding error: {loadpath}\n\t{e}\n")
			return -3
		data.write(e)
		labels.write(message.label.encode() + bytes(1))
	# Let's make sure that each sections is a multiple of 4 bytes.
	temp = data.seek(0,2) % 4
	if temp != 0:
		data.write(bytes(4-temp))
	
	temp = labels.seek(0,2) % 4
	if temp != 0:
		labels.write(bytes(4-temp))
	# Now we fill in the header...
	header.write( pack('<LLL', data.seek(0,2), strings.seek(0,2), table.seek(0,2)+labels.seek(0,2)) )
	header.write(bytes(0x20))
	# Well, that was easy. Time to save the file.
	with open(savepath, 'wb') as text_file:
		for part in [header,data,strings,table,labels]:
			part.seek(0)
			text_file.write(part.read())
	
	return 0
	

#Now for the console interface.
if __name__ == "__main__":
	args = parser.parse_args()
	
	def print_progress (iteration, total):
		"""Based on stack overflow 'Text Progress Bar in the Console [closed]'"""
		percent = "{0:.1f}".format(100 * (iteration / float(total)))
		filledLength = int(100 * iteration // total)
		bar = '█' * filledLength + '-' * (100 - filledLength)
		print(f'\r|{bar}| {percent}%', end = "\r")
		if iteration == total: 
			print()
	
	def end_program(message, help=False, wait=-1):
		print(message)
		if help:
			parser.print_help()
		if wait == -1:
			input("Press enter to exit")
		elif wait > 0:
			time.sleep(wait)
		quit()
		
	#Keep track of when the program started.
	if not args.silent:
		start = time.perf_counter()
	
	#First and foremost, let's see if we have any inputs so we can actually run.
	if args.input == None:
		if args.dragged == []:
			if os.path.isdir("decoded"):
				args.input = ["decoded"]
			else:
				end_program("ERROR: No inputs, and decoded folder not found! Printing help text...", help=True)
		else:
			args.input = args.dragged
	#Let's keep track if there are multiple inputs, so we can throw an error if the output isn't a folder.
	multiple = len(args.input) > 1
	if not multiple and os.path.isdir(args.input[0]):
		multiple = True
	
	#Now to check the output.
	output_is_folder = False
	if args.output[-1] == os.sep or os.path.isdir(args.output):
		output_is_folder = True
		if not os.path.exists(args.output):#If the output is a folder and doesn't exist, let's make it for the user.
			try:
				os.mkdir(args.output)
			except:
				end_program("ERROR: Couldn't create output folder.")
	elif multiple:#If we have multiple inputs and the output isn't a folder, we should end execution.
		end_program('ERROR: Input was multiple files, but the output was a single file.')
	
	#Let's set up error reporting for errors that won't stop execution...
	if args.error != None:
		try:
			stderr_temp = sys.stderr
			sys.stderr = open(args.error,'a')
			sys.stderr.write(time.strftime(f'[%Y-%m-%d %H:%M:%S] {os.path.basename(__file__)}\n',time.localtime()))
		except:
			end_program(f"ERROR: Invalid error file.\n{args.error}")
	
	#Alright, let's filter through these inputs to get a list of filenames. Some of them may be folders, which is why we have to do this.
	inputs = []
	for input in args.input:
		if not os.path.exists(input):
			end_program(f"ERROR: Input doesn't exist.\n{input}")
		if not os.path.isdir(input):
			inputs.append(input)
		else:#Time to sort through the folder...
			if args.wildcard != None:
				wildcard = args.wildcard.split('*')
			for root, dirs, files in os.walk(input, topdown=False):
				for name in files:
					if args.wildcard != None:#Check out this lazy wildcard implementation.
						fname = os.path.basename(name)
						if not fname.endswith(wildcard[-1]):
							continue
						for wild in wildcard:
							if wild not in fname:
								fname = None#Just an easy way to save the failure...
								break
						if fname == None:#If we failed the wildcard test, on to the next filename.
							continue
					inputs.append(os.path.join(root, name))
	
	#Good to go! Let's get through these files.
	encoded_files = 0
	for i in range(len(inputs)):
		if not args.silent:
			print_progress(1+i,len(inputs)+1)
			
		if output_is_folder:
			filename = '.'.join(os.path.basename(inputs[i]).split('.')[:-1]) if inputs[i][-4:] == ".txt" else os.path.basename(inputs[i])
			savepath = os.path.join(args.output,filename)
		else:
			savepath = args.output
		
		if encode_1LMG(inputs[i],savepath) >= 0:
			encoded_files += 1

	#Looks like we're done. Let's finish whatever outputs we have, and then exit.
	if not args.silent:
		print_progress(1,1)
	sys.stderr.flush()
	if args.error != None:
		sys.stderr = stderr_temp
	if not args.silent:
		end_program("\nSuccessfully encoded {0} file{1} in {2:.1f}ms".format(encoded_files,("" if (encoded_files==1) else "s"),(time.perf_counter()-start)*1000), wait=(-1 if args.verbose else 5))