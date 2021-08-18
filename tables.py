text_table = {
	0x00: '0',
	0x01: '1',
	0x02: '2',
	0x03: '3',
	0x04: '4',
	0x05: '5',
	0x06: '6',
	0x07: '7',
	0x08: '8',
	0x09: '9',
	0x0a: 'A',
	0x0b: 'B',
	0x0c: 'C',
	0x0d: 'D',
	0x0e: 'E',
	0x0f: 'F',
	0x10: 'G',
	0x11: 'H',
	0x12: 'I',
	0x13: 'J',
	0x14: 'K',
	0x15: 'L',
	0x16: 'M',
	0x17: 'N',
	0x18: 'O',
	0x19: 'P',
	0x1a: 'Q',
	0x1b: 'R',
	0x1c: 'S',
	0x1d: 'T',
	0x1e: 'U',
	0x1f: 'V',
	0x20: 'W',
	0x21: 'X',
	0x22: 'Y',
	0x23: 'Z',
	0x24: 'a',
	0x25: 'b',
	0x26: 'c',
	0x27: 'd',
	0x28: 'e',
	0x29: 'f',
	0x2a: 'g',
	0x2b: 'h',
	0x2c: 'i',
	0x2d: 'j',
	0x2e: 'k',
	0x2f: 'l',
	0x30: 'm',
	0x31: 'n',
	0x32: 'o',
	0x33: 'p',
	0x34: 'q',
	0x35: 'r',
	0x36: 's',
	0x37: 't',
	0x38: 'u',
	0x39: 'v',
	0x3a: 'w',
	0x3b: 'x',
	0x3c: 'y',
	0x3d: 'z',
	0x3e: '!',
	0x3f: '?',
	0x40: 'À',
	0x41: 'Á',
	0x42: 'Â',
	0x43: 'Ä',
	0x44: 'Æ',
	0x45: 'Ç',
	0x46: 'È',
	0x47: 'É',
	0x48: 'Ê',
	0x49: 'Ë',
	0x4a: 'Ì',
	0x4b: 'Í',
	0x4c: 'Î',
	0x4d: 'Ï',
	0x4e: 'Ñ',
	0x4f: 'Ò',
	0x50: 'Ó',
	0x51: 'Ô',
	0x52: 'Ö',
	0x53: 'Œ',
	# 0x54: Character looks blank, but isn't used as a space?
	0x55: 'Ù',
	0x56: 'Ú',
	0x57: 'Û',
	0x58: 'Ü',
	0x59: 'à',
	0x5a: 'á',
	0x5b: 'â',
	0x5c: 'ä',
	0x5d: 'æ',
	0x5e: 'ç',
	0x5f: 'è',
	0x60: 'é',
	0x61: 'ê',
	0x62: 'ë',
	0x63: 'ì',
	0x64: 'í',
	0x65: 'î',
	0x66: 'ï',
	0x67: 'ñ',
	0x68: 'ò',
	0x69: 'ó',
	0x6a: 'ô',
	0x6b: 'ö',
	0x6c: 'œ',
	0x6d: 'ß',
	0x6e: 'ù',
	0x6f: 'ú',
	0x70: 'û',
	0x71: 'ü',

	0x73: '¡',
	0x74: '¿',

	0xe1: '.',

	0xe5: '(',
	0xe6: ')',

	0xe9: '“', # Not used?
	0xea: '"',#'”',  # Curly but used for all quotation marks anyway (edited to normal " for easier editing)

	0xed: ':',

	0xef: ',',

	0xf2: '*',
	0xf3: "'",#'’', # (edited to normal ' for easier editing)
	0xf4: '-',

	0xf7: '%',
	0xf8: '…',  # XXX Vertically centered
	0xf9: '~',
	0xfa: '«',  # XXX Bigger
	0xfb: '»',  # XXX Bigger
	0xfc: '&',
	0xfd: '☆',
	0xfe: '♪',
	0xff: ' ',

}

images = {
	0x0116: '[BACK]',
	0x0117: '[TRICK]',
	0x0118: '[GHOST]',
}

colors = {
	0x6: 'RED',
	0x9: 'BLUE',
	0xf: 'BLACK',
}

portraits = {
	0x01: 'Jeego',

	0x04: 'Lynne_smile',
	0x07: 'Lynne_sweat',
	0x0d: 'Lynne_pensive',
	0x0e: 'Lynne_think',
	0x13: 'Lynne_frown',
	0x14: 'Lynne_serious',
	0x16: 'Lynne_surprise',
	0x1c: 'Lynne_pensive',

	0x27: 'Sissel_smile',
	0x29: 'Sissel_frown',
	0x2b: 'Sissel_pensive',
	0x2d: 'Sissel_sweat',
	0x2f: 'Sissel_befuddled',
	0x34: 'Sissel_shrug',
	0x36: 'Sissel_surprise',
	0x3a: 'Sissel_angry',
	0x44: 'Sissel_empty',#plays sissel's portrait noise on text boxes

	0x72: 'Sith_left',

	0x7b: 'Jeego_left',
	0x7c: 'Jeego_right',
	
	0x7f: 'Tengo_right',

	0x80: 'Ray_on_left',
	0x81: 'Ray_on_right',
	0x83: 'Ray_off_right',
	0x85: 'Ray_soul',
	0x86: 'Ray_empty',#plays ray's portrait noise on text boxes
	
	0x88: 'Robot_right',
	
	0x8a: 'Cabanela_',
	
	0xc6: 'Green_Detective',
	
	0xca: 'Blue_Detective',
	
	0xcc: 'Blue_Doctor',
	
	0xee: 'Card_Guard',
	
	0xea: 'Bailey',
	0xec: 'Bailey_empty',

	0x10c: 'Floating-soul',
}

mini_portraits = {
	0x1: 'Sissel',
	0x2: 'Missile',
	0x3: 'Lynne',
	0x4: 'Ray',
	0x5: 'None',
	0x6: 'None2',#??
	0x7: 'Guardian',
	0x8: 'Cat'
}

sounds = {
	0x00: 'silence',
	
	0x15: 'surprise',
	0x16: 'intrigue',
	0x17: 'yell',
	0x18: 'slam'
}

commands = {
	0xff01: '[NEW]\n',#making this into a [] code, so that \n characters can be ignored by the encoder and used solely to make text files easier to read. hard choice, but i think this makes everything less finnicky overall. should also help the whole newline changing with OS problem?
	0xff02: '[CLEAR]\n\n',#waits for input, then clears the textbox.
	0xff03: '[CENTER]',#centers text printed afterwards, until a new line. produced undesirable results when used in the middle of a line.
	0xff04: '[SPEED {0}]',#text speed, higher seems slower. frames per character?
	0xff05: '[COLOR {0}]',#changes text color
	0xff06: '[SHOW]',#shows the textbox
	0xff07: '[HIDE]',#hides the textbox
	0xff08: '[PORTRAIT {0}]\n',#portraits have different barks on appearing
	
	0xff0c: '[PAUSE {0}]',#pauses text output. measured in frames?
	0xff0d: '[SFX {0}]',#sound effects
	
	0xff0f: '[FLASH]',#flashes the screen white
	0xff10: '[SHAKE {0} FOR {{0}}]',#time measured in frames?
	
	0xff15: '[CLEAR IN {0}]\n\n',#clears the textbox after some time. measured in frames?
	0xff16: '[BREAK]\n\n',#breaks up narrator text. softlocks when used in a text box.
	
	0xff19: '[FADE_PORTRAIT {0} IN {{0}}]\n',#lower FADE is slower. no portrait barks?
	
	0xff1b: '[MINI_PORTRAIT {0}]\n',#mini portraits on the side of dialogue boxes
	0xff1c: '[MUSIC {0}]',#changes music. could use another table.
	
	0xff20: '[LOWER {0}]',#drops text down, more goes lower.
	0xff21: '[SCRIPTED_PAUSE]',#pauses until a scripted condition is met. not available on all dialogue. does not clear the textbox.
	0xff22: '[APPEAR {0}]',#affects fade in speed of narrator text. since it's used to accelerate fade in speed rather than slow it down, i'll just call it 'appear'. could use more testing, effects of the number may not be linear.
	0xff23: '[SKIP]',#attempts to skip the remainder of the current textbox, doesn't allow waiting for input
	0xff24: '[FADE {0}]',#fades text in all at once.
	
	0xff28: '[VOLUME {0}]',#changes music volume
	
	0xff2d: '[START Event {0}, Scene {{0}}]\n',#Event # seems to roughly correlate with story progress. Scene # seems to be sequential within each event, usually. some files contain scenes from multiple events... as of now, unsure how the game uses this information or if it even matters.
	
	0xfffe: '[STOP]',#waits for input, then ends a scene
}

stages = {#where is the park???? where is yomiel's death puzzle??
	'st01': "Junkyard",
	'st02': "Super's Office",
	'st03': "Guard Room",#Is everything in the prison in this folder? Is the Moonlit Courtyard here??
	'st04': "Kitchen",
	'st05': "Novelist's Apt.",
	'st06': "Lynne's Apartment",
	'st07': "Kamila's Old House",
	'st09': "Minister's Office",
	'st11': "Special Investigation",
	'st13': "The Chicken Kitchen",#is this merged with the park because of the chicken kitchen puzzle?
	'st14': "Luxurious Parlor",
	'st15': "Epilogue"
}

byte_string = {
	'outside': '[0x{0:04x}]',
	'inside': '0x{0:04x}'
}