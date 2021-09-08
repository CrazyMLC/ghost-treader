from io import BytesIO
from struct import pack,unpack

from tables import *

# For encoding, we're gonna want to make some custom tables based on the ones in tables.py, and we don't want to have to redo it every time we encode a new file.
encode_tags = None# We'll have a quick, easy to search list of commands/other []s that don't have any parameters.
encode_commands = None# And then we'll have the more complicated commands with parameters.
encode_text = None# And then the inverted text table
encode_portraits = None# And there's a lot of portraits, so we should do those too just to keep things convenient
def init_encoding():
	global encode_tags, encode_commands, encode_text, encode_portraits
	encode_tags,encode_commands,encode_text,encode_portraits = {},{},{},{}
	
	for key,image in images.items():
		encode_tags[image] = key
	for key,command in commands.items():
		command = command.replace('\n','')
		if command.count(' ') == 0:
			encode_tags[command] = key
		else:
			command = command[1:-1].split(' ')
			k = command[0]
			command[0] = key
			encode_commands[k] = command
	for key,value in text_table.items():
		encode_text[value] = key
	for key,value in portraits.items():
		encode_portraits[value] = key


class Message:
	def __init__(self, offset=None, pointer=None):
		self.label_offset = offset
		self.label = ""
		self.length = 0
		self.pointer = pointer
		self.decoded = ""
	
	def __str__(self):
		namestr = self.label + " Position: " + hex(self.pointer)
		result = "\n"
		result += '=' * len(namestr) + "\n"
		result += namestr + "\n"
		result += '=' * len(namestr) + "\n"
		result += self.decoded + "\n"
		return result
	
	def get_label(self, data, position):
		data.seek(position+self.label_offset)
		bytes = bytearray(b'')
		while True:
			char, = data.read(1)
			if char == 0:
				break
			else:
				bytes.append(char)
		self.label = bytes.decode('ASCII')
	
	def decode(self, data):
		data.seek(self.pointer)
		self.decoded = ""
		i = 0
		while i < self.length>>1:
			char, = unpack('<H', data.read(2))
			if char in commands:
				command = commands[char].split(' ')
				
				# let's count our number of parameters for this function.
				parameters = []
				for j in range(len(command)):
					if '{}' in command[j]:
						parameters.append(j)
				# if getting parameters would go out of bounds, don't do it.
				if i+len(parameters) >= self.length>>1:
					self.decoded += text_table.setdefault(char, byte_string['outside'].format(char))
					i+=1
					continue
				# okay, time to fetch parameters.
				for j in range(len(parameters)):
					i+=1
					parameters[j] = (unpack('<H', data.read(2))[0], parameters[j])
				# if we got any params, time to start inserting them. check tables for replacing numbers with strings.
				for j in range(len(parameters)):
					param = parameters[j][0]#This is the actual parameter
					ind = parameters[j][1]#This is the index within the command the parameter is for
					if j == 0:
						if command[0] == '[COLOR':
							param = colors.setdefault(param, byte_string['inside'].format(param))
						elif command[0] == '[MINI_PORTRAIT':
							param = mini_portraits.setdefault(param, byte_string['inside'].format(param))
						elif command[0] in ['[PORTRAIT','[FADE_PORTRAIT']:
							param = portraits.setdefault(param, byte_string['inside'].format(param))
						elif command[0] in ['[SFX','[CONFIRM_SFX']:
							param = sounds.setdefault(param, byte_string['inside'].format(param))
						elif command[0] in ['[MUSIC','[FADE_MUSIC']:
							param = music.setdefault(param, byte_string['inside'].format(param))
					command[ind] = command[ind].format(param)
				# great, the command should be ready to go.
				self.decoded += ' '.join(command)
			elif char in images:
				self.decoded += images.setdefault(char, byte_string['inside'].format(char))
			else:
				self.decoded += text_table.setdefault(char, byte_string['outside'].format(char))
			i+=1
			
	def encode(self):
		if encode_tags == None:
			init_encoding()
		encoded = BytesIO()
		trimmed = self.decoded.replace("\n","").replace("\t","")
		i = 0
		while i < len(trimmed):
			if trimmed[i] != '[':
				if trimmed[i] in encode_text:
					encoded.write( pack('<H', encode_text[trimmed[i]]) )
				else:
					return f"Unknown character in {self.label}: {trimmed[i]}"
			else:
				ending = trimmed.find(']',i+1)
				if ending == -1:
					return f"Unclosed bracket in {self.label}: {trimmed[i:i+15]}(...)"
				tag = trimmed[i:ending+1]
				i = ending
				if tag in encode_tags:
					encoded.write( pack('<H', encode_tags[tag]) )
				elif tag[1:3] == "0x":
					encoded.write( pack('<H', int(tag[1:-1],16)) )
				else:
					# Maybe there's misplaced spaces in the tag. Let's try to be forgiving about that by filtering empty strings out of the list.
					tag = tag[1:-1]
					tag_backup = tag # Keep the original for error reporting
					tag = list(filter(lambda x: x!='',tag.split(' ')))
					if tag[0] not in encode_commands:
						return f"Unknown command in {self.label}: [{tag_backup}]"
					elif len(tag) != len(encode_commands[tag[0]]):
						print(len(tag), len(encode_commands[tag[0]]))
						return f"Command has incorrect syntax in {self.label}: [{tag_backup}]"
					command = encode_commands[tag[0]]
					params = [command[0]]
					for z in range(1,len(command)):# If the same spot in the original command string is a variable, let's extract it.
						if '{}' in command[z]:
							params.append(tag[z])
					# Now the arduous process of converting the strings into numbers.
					for v in range(len(params)):
						param = params[v]
						if type(param) is int:
							continue
						elif param.isnumeric():
							params[v] = int(param,10)
						elif param[:-1].isnumeric():# Let's allow extra characters like commas or colons after parameters
							params[v] = int(param[:-1],10)
						elif param[:2] == "0x":
							if param[-1] in [',',':',';']:
								param = param[:-1]
							params[v] = int(param,16)
						elif v == 1:
							if tag[0] == "COLOR":
								for key,value in colors.items():
									if param == value:
										params[v] = key
										break
							elif tag[0] == "MINI_PORTRAIT":
								for key,value in mini_portraits.items():
									if param == value:
										params[v] = key
										break
							elif tag[0] in ["PORTRAIT","FADE_PORTRAIT"]:
								params[v] = encode_portraits[param]
							elif tag[0] in ["SFX","CONFIRM_SFX"]:
								for key,value in sounds.items():
									if param == value:
										params[v] = key
										break
							elif tag[0] in ["MUSIC","FADE_MUSIC"]:
								for key,value in music.items():
									if param == value:
										params[v] = key
										break
							else:
								return f"Unknown {tag[0]} input in {self.label}: [{param}]"
						else:
							return f"Unknown {tag[0]} input in {self.label}: [{param}]"
					encoded.write( pack('<'+'H'*len(params),*params) ) 
			i+=1
		encoded.seek(0)
		return encoded.read()
				