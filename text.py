from collections import namedtuple
from io import BytesIO
from struct import unpack
from sys import argv

from tables import *



def decode_message(message_data):
	"""Decode the message from an iterator"""

	message = ''

	for char in message_data:
		if char in commands:
			command = commands[char]
			parameters = []
			for i in range(command.count('{0')):
				parameters.append(next(message_data))
			for param in parameters:
				p = param
				if command.count('COLOR {'):
					p = colors.setdefault(param, r'!!!!!\x{0:04x}'.format(param))
				elif command.count('MINI_PORTRAIT {'):
					p = mini_portraits.setdefault(param, r'!!!!!\x{0:04x}'.format(param))
				elif command.count('PORTRAIT {'):
					p = portraits.setdefault(param, r'!!!!!\x{0:04x}'.format(param))
				elif command.count('SFX {'):
					p = sounds.setdefault(param, r'!!!!!\x{0:04x}'.format(param))
				command = command.format(p)
			message += command
			if command.count('[STOP]'):
				break
		else:
			message += text_table.setdefault(char, r'!!!!!\x{0:04x}'.format(char))

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

def message_iterator(data, pointer):
	"""Yield the message at the given pointer, character by character.

	Each character is two bytes long and little endian.
	"""
	data.seek(pointer)
	while True:
		char, = unpack('<H', data.read(2))

		#if char == 0xfffe:
		#	raise StopIteration
	   # else:
		yield char


with open(argv[1], 'rb') as text_file:
	data = text_file.read()
data = BytesIO(data)


assert data.read(4) == b'1LMG'

# Seek to and read message pointers
data.seek(8)
pointers_offset, = unpack('<H', data.read(2))
data.seek(pointers_offset + 0x38)

#assert data.read(4) == b'\x2a\x00\x00\x00'  # Not sure of the significance

message_count, = unpack('<L', data.read(4))
messages = []
Message = namedtuple('Message', ['label_offset', 'message_pointer'])

for m in range(message_count):
	messages.append(
		Message( *unpack('<LL', data.read(8)) )
	)

labels_pointer = data.tell()  # XXX Can I actually *find* this anywhere?

for message in messages:
	# Find the label and print it as a header
	label = get_label(data, labels_pointer + message.label_offset)

	print(label, message.message_pointer)
	print('=' * len(label))

	# Extract the actual message
	message = message_iterator(data, message.message_pointer)
	message = decode_message(message)

	print(message, end='\n\n')
