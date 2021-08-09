from collections import namedtuple
from io import BytesIO
from struct import unpack
import sys
import os

from tables import *

def decode_message(data, pointer, length):
	data.seek(pointer)
	decoded = ''
	i = 0
	
	while i < length>>1:
		char, = unpack('<H', data.read(2))
		if char in commands:
			command = commands[char]
			# if getting parameters would go out of bounds, don't do it.
			if i+command.count('{0') >= length>>1:
				decoded += text_table.setdefault(char, r'[0x{0:04x}]'.format(char))
				i+=1
				continue
			# okay, time to fetch parameters.
			parameters = []
			for j in range(command.count('{0')):
				i+=1
				parameters.append(unpack('<H', data.read(2))[0])
			# if we got any params, time to start inserting them. check tables for replacing numbers with strings.
			for param in parameters:
				p = param
				if command.count('COLOR {'):
					p = colors.setdefault(param, r'!!!\x{0:04x}'.format(param))
				elif command.count('MINI_PORTRAIT {'):
					p = mini_portraits.setdefault(param, r'!!!\x{0:04x}'.format(param))
				elif command.count('PORTRAIT {'):
					p = portraits.setdefault(param, r'!!!\x{0:04x}'.format(param))
				elif command.count('SFX {'):
					p = sounds.setdefault(param, r'!!!\x{0:04x}'.format(param))
				command = command.format(p)
			decoded += command
		else:
			decoded += text_table.setdefault(char, r'[0x{0:04x}]'.format(char))
		i+=1
	return decoded


def get_label(data, pointer):
	"""Get and return the label at the given pointer."""
	data.seek(pointer)
	label = bytearray(b'')

	while True:
		char, = data.read(1)
		if char == 0:
			break
		else:
			label.append(char)

	return label.decode('ASCII')

def decode_1LMG(filepath):
	with open(filepath, 'rb') as text_file:
		data = text_file.read()
	data = BytesIO(data)
	
	try:
		assert data.read(4) == b'1LMG'
	except:
		print("Not a 1LMG file.")
		return "not 1LMG"

	# find all the important file locations
	mystery, = unpack('<L', data.read(4))
	footer_offset, = unpack('<L', data.read(4))
	pointers_offset, = unpack('<L', data.read(4))

	is_dialogue_file = pointers_offset == 4
	footer_position = 0x34 + footer_offset
	pointers_position = footer_position + pointers_offset

	data.seek(pointers_position)
	message_count, = unpack('<L', data.read(4))

	labels_offset = 4+message_count*8
	labels_position = labels_offset + pointers_position

	Message = namedtuple('Message', ['label_offset', 'message_pointer'])
	messages = []
	lengths = []
	# instead of looking for stop codes, let's find the lengths. this way, we can attempt to decode scripts without crashing.

	for m in range(message_count):
		messages.append(
			Message( *unpack('<LL', data.read(8)) )
		)
		if m > 0:# filling in the lengths
			lengths.append(messages[m].message_pointer - messages[m-1].message_pointer)
	try:# if the message count is 0, the script will crash. better catch that gracefully.
		lengths.append(footer_position - messages[message_count-1].message_pointer)
	except:
		print("File contains no data.")
		return "no data"


	for m in range(message_count):
		# Find the label and print it as a header
		label = get_label(data, labels_position + messages[m].label_offset)

		print(label, "Position:", hex(messages[m].message_pointer))
		print('=' * len(label))

		# Extract the actual message
		messages[m] = decode_message(data, messages[m].message_pointer, lengths[m])

		# sometimes the last message in a file will have a lingering 0x0000 in order to 4byte-align the pointer table...
		# i don't know how to tell when it's just padding or when it's part of the msg (scripts don't have stop codes)
		# i'll cut the 0x0000 out if it's after a [STOP] for the benefit of the dialogue files.
		if is_dialogue_file and m+1 == message_count:
			if messages[m][-7:] == "[STOP]0":
				messages[m] = messages[m][:-1]

		print(messages[m], end='\n{}\n\n'.format('=' * len(label)))
	return "ok"

def decode_and_save_1LMG(loadpath, savepath):
	original_stdout = sys.stdout
	with open(savepath, 'w+', encoding="utf8") as f:
		sys.stdout = f # Change the standard output to the file we created.
		decode_1LMG(loadpath)
	sys.stdout = original_stdout # Reset the standard output to its original value

if __name__ == "__main__":
	output = "decoded"
	if not os.path.isdir(output):
		os.mkdir(output)
	for v in range(1,len(sys.argv)):
		if sys.argv[v] == "--output":
			if os.path.isdir(sys.argv[v+1]):
				output = sys.argv[v+1]
				continue
			print("invalid output path:",sys.argv[v+1])
			break
		if os.path.isfile(sys.argv[v]):
			if sys.argv[v-1] == "--view":
				decode_1LMG(sys.argv[1])
				continue
			new_file = "{}.txt".format(os.path.join(output,os.path.basename(sys.argv[v])))
			decode_and_save_1LMG(sys.argv[v],new_file)
			continue
		print("couldn't process command:",sys.argv[v])