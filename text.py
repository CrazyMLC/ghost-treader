from collections import namedtuple
from io import BytesIO
from struct import unpack
from sys import argv

from tables import *


def decode_message(m):
	data.seek(messages[m].message_pointer)
	message = ''
	i = 0
	
	while i < lengths[m]>>1:
		char, = unpack('<H', data.read(2))
		if char in commands:
			command = commands[char]
			# if getting parameters would go out of bounds, don't do it.
			if i+command.count('{0') >= lengths[m]>>1:
				message += text_table.setdefault(char, r'[0x{0:04x}]'.format(char))
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
			message += command
		else:
			message += text_table.setdefault(char, r'[0x{0:04x}]'.format(char))
		i+=1

	#print(message)
	return message


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


with open(argv[1], 'rb') as text_file:
	data = text_file.read()
data = BytesIO(data)


"""
header format: (length 34)
1LMG (identifier)
4 byes (???)
4 bytes (footer pointer)
4 bytes (pointer table pointer, relative to above)
4 bytes (end of file pointer, relative to above)

data format:
#

footer format:
2 bytes (* )
# string bytes
# data pointer table
	4 bytes table length
	# table
2 bytes (* )
# label bytes
"""


assert data.read(4) == b'1LMG'

# find all the important file locations
data.seek(8)
footer_offset, = unpack('<H', data.read(2))
data.seek(12)
pointers_offset, = unpack('<H', data.read(2))

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
lengths.append(footer_position - messages[message_count-1].message_pointer)


for m in range(message_count):
	# Find the label and print it as a header
	label = get_label(data, labels_position + messages[m].label_offset)

	print(label, messages[m].message_pointer)
	print('=' * len(label))

	# Extract the actual message
	messages[m] = decode_message(m)

	# sometimes the last message in a file will have a lingering 0x00 in order to 4byte-align the pointer table...
	# i don't know how to tell when it's just padding or when it's part of the msg (scripts don't have stop codes)
	# i'll cut the 0x00 out if it's after a [STOP] for the benefit of the localization files.
	if m+1 == message_count:
		if messages[m][-7:] == "[STOP]0":
			messages[m] = messages[m][:-1]

	print(messages[m], end='\n{}\n\n'.format('=' * len(label)))
