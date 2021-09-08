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
	0x72: '_',#0x72 is blank, but since there's no underscore(?), we'll use it as such.
	0x73: '¡',
	0x74: '¿',
	#0x75-0xe0 are blank
	0xe1: '.',
	0xe2: '→',
	0xe3: '「',
	0xe4: '」',
	0xe5: '(',
	0xe6: ')',
	0xe7: '『',
	0xe8: '』',
	0xe9: '“', # Not used?
	0xea: '"',#'”',  # Curly but used for all quotation marks anyway (edited to normal " for easier editing)
	0xeb: '▼',
	0xec: '▲',
	0xed: ':',
	0xee: '、', #??
	0xef: ',',
	0xf0: '+',
	0xf1: '/',
	0xf2: '*',
	0xf3: "'",#'’', # (edited to normal ' for easier editing)
	0xf4: '-',
	0xf5: '〮',#?
	0xf6: '〪',#?
	0xf7: '%',
	0xf8: '…',  # XXX Vertically centered
	0xf9: '~',
	0xfa: '«',  # XXX Bigger
	0xfb: '»',  # XXX Bigger
	0xfc: '&',
	0xfd: '☆',
	0xfe: '♪',
	0xff: ' ',
	0x100: '–',#a raised dash compared to 0xf4
	0x101: '”',#it's a normal quote, but that's in use by 0xea for editing purposes
	#0x102: '[',
	#0x103: ']',#need to reserve these for tags...
	0x104: '$',
	0x105: '#',
	0x106: '>',
	0x107: '<',
	0x108: '=',
	0x109: '◆',
	0x10a: '∈',
	0x10b: '∀',
	0x10c: ';',
	0x10d: '∋',
	0x10e: '⊇',
	0x10f: '⊂',
	0x110: '○',
	0x111: '—',
	0x112: 'χ',
}

images = {
	0x0113: '[COIN]',
	0x0114: '[DPAD]',
	0x0115: '[JOWD]',
	0x0116: '[BACK]',
	0x0117: '[TRICK]',
	0x0118: '[GHOST]',
	0x0119: '[RESET]',
	0x011a: '[JOURNAL]',
	0x011b: '[SWAP]',
	0x011c: '[MISSILE]',
	0x011d: '[SISSEL]',
}

colors = {
	0x0: 'WHITE',#not particularly useful because of the textbox background
	#0x1: 'glitch',
	0x2: 'GREY',#a little glitchy looking
	#0x3: 'glitch2',
	#0x4: 'glitch_red',
	0x5: 'LIGHT_RED',
	0x6: 'RED',
	#0x7: 'glitch_red2',
	#0x8: 'glitch_redblue',#seems like the color data works off of using the actual binary data of the input as flags
	0x9: 'BLUE',
	#0xa: 'glitch_light_bluegreen',
	#0xb: 'glitch_bluegreen',
	0xc: 'GREEN',
	#0xd: 'glitch_light_greygreen',
	#0xe: 'glitch_greygreen',
	0xf: 'BLACK',
	#0x10: 'glitch3',
	#colors up to 32 appear glitched still, but seemed to be developing shadows. could be there's more data further up.
}

portraits = {# Every portrait has a flipped version, except the 'empty' potraits. Flipped portraits are always right after the unflipped portrait.
	# 'empty' portraits serve multiple functions. the main reason they're used is to not obscure the game screen, but there's a reason each character has their own empty sprites.
	# Each 'empty' plays that character's bark sound effect, (masculine or feminine), as well as showing that character's icon in the text log. That's also why some characters have multiple empty sprites.
	
	#0x00: 'Broken',
	0x01: 'Jeego',
	#0x02: 'Jeego_r',
	0x03: 'Lynne_smile',
	0x05: 'Lynne_happy',
	0x07: 'Lynne_sweat',
	0x09: 'Lynne_sad',
	0x0b: 'Lynne_shout',
	0x0d: 'Lynne_think',
	0x0f: 'Lynne_angry',#shout, but with a fist
	0x11: 'Lynne_proud',
	0x13: 'Lynne_serious',
	0x15: 'Lynne_surprise',
	0x17: 'Lynne_fear',
	0x19: 'Lynne_shock',
	0x1b: 'Lynne_pensive',
	0x1d: 'Lynne_empty',
	
	0x1e: 'KidLynne_sad1',#hat,stick
	0x20: 'KidLynne_sad2',#stick
	0x22: 'KidLynne_sad3',#only sadness
	0x24: 'KidLynne_cat',
	0x26: 'KidLynne_empty',
	
	0x27: 'Sissel_smile',
	0x29: 'Sissel_frown',
	0x2b: 'Sissel_think',
	0x2d: 'Sissel_sweat',
	0x2f: 'Sissel_befuddled',
	0x31: 'Sissel_soul',
	0x33: 'Sissel_soul_empty',
	0x34: 'Sissel_shrug',
	0x36: 'Sissel_surprise',
	0x38: 'Sissel_pensive',
	0x3a: 'Sissel_shout',
	0x3c: 'Sissel_cat',
	0x3e: 'Sissel_cat_empty',
	0x3f: 'Yomiel_junk',
	0x41: 'Yomiel_junk_empty',
	0x42: 'Yomiel_evil',
	0x44: 'Sissel_empty',
	0x45: 'Yomiel_smile',
	0x47: 'Yomiel_frown',
	0x49: 'Yomiel_think',
	0x4b: 'Yomiel_sweat',
	0x4d: 'Yomiel_befuddled',
	0x4f: 'Yomiel_shrug',
	0x51: 'Yomiel_surprise',
	0x53: 'Yomiel_pensive',
	0x55: 'Yomiel_shout',
	0x57: 'Yomiel_evil2',
	0x59: 'Yomiel_empty',
	0x5a: 'Sissel_smile2',
	0x5c: 'Sissel_peek',
	
	0x5e: 'Emma_smile',
	0x60: 'Emma_shock',
	0x62: 'Emma_empty',
	
	0x63: 'Kamila_smile',
	0x65: 'Kamila_think',
	0x67: 'Kamila_happy',
	0x69: 'Kamila_possessed',
	0x6b: 'Kamila_cry',
	0x6d: 'Kamila_sad',
	0x6f: 'Kamila_shout',
	0x71: 'Kamila_empty',
	
	0x72: 'Sith',
	0x74: 'Sith_empty',
	
	0x75: 'Missile',
	0x77: 'Missile_old',
	0x79: 'Missile_empty',
	0x7a: 'Missile_old_empty',
	
	0x7b: 'Jeego2',
	0x7d: 'Jeego_empty',
	
	0x7e: 'Tengo',
	
	0x80: 'Ray_on',
	0x82: 'Ray_off',
	0x84: 'Ray_soul',#when ray speaks over a soul
	0x86: 'Ray_empty',#plays ray's portrait noise on text boxes
	
	0x87: 'Robot',
	
	0x89: 'Cabanela_smile',
	0x8b: 'Cabanela_empty',#?
	0x8c: 'Cabanela_happy',
	0x8e: 'Cabanela_sweat',
	0x90: 'Cabanela_pensive',
	0x92: 'Cabanela_shout',
	0x94: 'Cabanela_frown',
	
	0x96: 'Jowd_serious',
	0x98: 'Jowd_frown',
	0x9a: 'Jowd_laugh',
	0x9c: 'Jowd_smile',
	0x9e: 'Jowd_shout',
	0xa0: 'Jowd_serious_past',
	0xa2: 'Jowd_frown_past',
	0xa4: 'Jowd_smile_past',
	0xa6: 'Jowd_serious_jacket',
	0xa8: 'Jowd_frown_jacket',
	0xaa: 'Jowd_smile_jacket',
	0xac: 'Jowd_smug',
	0xae: 'Jowd_pensive',
	0xb0: 'Jowd_laugh_past',
	0xb2: 'Jowd_shout_past',
	0xb4: 'Jowd_smug_past',
	0xb6: 'Jowd_laugh_jacket',
	0xb8: 'Jowd_shout_jacket',
	0xba: 'Jowd_smug_jacket',
	0xbc: 'Jowd_empty',
	
	0xbd: 'Officer_serious',
	0xbf: 'Officer_serious2',#?
	0xc1: 'Officer_devastated',
	0xc3: 'Officer_empty',
	
	0xc4: 'Officer2',#looks unfamiliar?
	
	0xc6: 'GreenDetective',
	0xc8: 'GreenDetective_empty',
	
	0xc9: 'BlueDetective',
	
	0xcb: 'BlueDoctor',
	
	0xcd: 'Rindge',
	0xcf: 'Rindge_empty',
	
	0xd0: 'Memry',
	
	0xd2: 'PidgeonMan',
	0xd4: 'PidgeonMan_empty',
	
	0xd5: 'Dandy',
	0xd7: 'Dandy_empty',
	
	0xd8: 'Beauty',
	0xda: 'Beauty_empty',
	
	0xdb: 'Bartender',
	
	0xdd: 'Amelie_upset',
	0xdf: 'Amelie_smile',
	0xe1: 'Amelie_healthy',
	
	0xe3: 'Minister_tense',
	0xe5: 'Minister_shock',
	0xe7: 'Minister_smile',
	0xe9: 'Minister_empty',
	
	0xea: 'Bailey',
	0xec: 'Bailey_empty',
	
	0xed: 'CardGuard',
	
	0xef: 'ArmedGuard',
	
	0xf1: 'Officer3',
	0xf3: 'Officer3_empty',
	
	0xf4: 'Rocker',
	
	0xf6: 'CurryLover',
	
	0xf8: 'Guardian',
	0xfa: 'Guardian_preach',
	0xfc: 'Guardian_empty',
	
	0xfd: 'Chef',
	0xff: 'Chef_empty',
	
	0x100: 'PoliceChief',
	0x102: 'PoliceChief_empty',
	
	0x103: 'MinisterGuard',
	
	0x105: 'YonoaOfficer',
	
	0x107: 'Alma_smile',
	0x109: 'Alma_happy',

	0x10b: 'Soul',
	0x10d: 'Soul_empty',
	
	#0x10e: 'Message'
	#0x10f: crash
}
def fill_in_portraits():# reversed portraits were not listed above, to keep the list short. let's fix that.
	temp = []
	for key,item in portraits.items():
		if key+1 not in portraits:
			temp.append(key+1)
	for key in temp:
		portraits[key] = portraits[key-1]+"_r"
fill_in_portraits()


mini_portraits = {
	0x0: 'None',
	0x1: 'Sissel',
	0x2: 'Missile',
	0x3: 'Lynne',
	0x4: 'Ray',
	0x5: 'Ray_empty',
	0x6: 'Ray_grey_empty',
	0x7: 'Guardian',
	0x8: 'Cat',
	0x9: 'Jowd',
	0xa: 'Minister',
	0xb: 'Cabanela',
	0xc: 'PidgeonMan',
	0xd: 'Sissel_soul',
	0xe: 'Kamila'# Kamila lacks a mini portrait, but her icon still shows in the text log.
	# Ones after this are glitched data
}

sounds = {
	0x0: 'silence',
	0x1: 'menu_select',
	0x2: 'menu_confirm',
	0x3: 'menu_cancel',
	0x4: 'menu_disabled',
	0x5: 'menu_text',
	0x6: 'male_bark',
	0x7: 'female_bark',
	0x8: 'menu_quit',
	0x9: 'menu_back',#unsure about the menu sfx namings but w/e
	0xa: 'ding',#some kind of musical ding sound?
	0xb: 'time_resume',#used when control returns during 4mbd
	0xc: 'fate_change',
	0xd: 'new_info',
	0xe: 'ghost_world',
	0xf: 'cutscene',
	0x10: 'ghost_move',
	0x11: 'ghost_trick',
	0x12: 'ghost_ping',
	0x13: 'telephone',
	0x14: 'phone_answer',
	#these next ones are the most relevant to dialogue
	0x15: 'surprise',
	0x16: 'intrigue',
	0x17: 'yell',
	0x18: 'slam',
	
	0x19: 'ding2',#another unfamiliar ding type sound?
	0x1a: 'save',
	0x1b: 'flashback',
	0x1c: 'time_travel',
	0x1d: 'ghost_talk',#loops forever until somehow cancelled?
	0x1e: 'ghost_switch',
	0x1f: 'ghost_fail',#don't actually remember what this is...
	0x20: 'fan_loop',#some kind of fan noise? loops forever
	0x21: 'silence2',#?
	0x22: 'door_open',
	0x23: 'door_close',
	0x24: 'water_drop',
	0x25: 'rat_talk',
	0x26: 'rat_hurt',
	0x27: 'shaker',#idk what this is
	#there are many, many sfx in this table, and very few are relevant to dialogue. maybe scripts use these?
	
	#here's some others used in dialogue:
	0x33: 'missile_bark',#have to check, but it's with most of his dialogue
	#0x37:
	#0xaa:#chef?
	#0x13e:#used by lovestruck officer?
	#0x179:#beauty/dandy?
	#0x193:#gunshot?
	
}

music = {
	0x0: 'silence',
	0x1: 'ghost_trick',
	0x2: 'fate_changed',
	0x3: 'fate_changed_variation',
	0x4: '4_minutes',
	0x5: '4_minutes_variation',
	0x6: 'count_down',
	
	0x7: 'beta_jingle1',
	
	0x8: 'suspicion',
	0x9: 'world_of_dead',
	0xa: 'deadline',
	0xb: 'ray_theme',
	0xc: 'lynne_theme',
	0xd: 'reincarnation',
	0xe: 'beauty_and_dandy',
	0xf: 'awakening',
	0x10: 'emma_theme',
	0x11: 'cabanela_theme',
	0x12: 'chicken_paradise',
	0x13: 'imprisoned',
	0x14: 'complication',
	0x15: 'welcome_to_salon',
	0x16: 'minister_theme',
	0x17: 'darkness',
	0x18: 'chase',
	0x19: 'jowd_theme',
	0x1a: 'trauma',
	0x1b: 'saying_goodbye',
	0x1c: 'providence',
	0x1d: 'dead_afterimage',
	0x1e: 'prologue',
	0x1f: 'nothingness',
	0x20: 'dashing_enigma',
	0x21: 'chained_past',
	0x22: 'desperate_struggle',
	0x23: 'epilogue',
	0x24: 'providence_skip_intro',#?
	0x25: 'intermission',
	
	0x26: 'beta_jingle2',
	0x27: 'beta_countdown',
	0x28: 'beta_lynne',
	0x29: 'unused_theme',
	0x2a: 'beta_suspicion',
	
	0x2b: 'missile_theme',
	
	0x2c: 'unused_peaceful',
	0x2d: 'beta_minister',
	0x2e: 'beta_salon',
	0x2f: 'beta_jingle3',
	0x30: 'unused_tifa',
	0x31: 'beta_emma',
	
	0x32: 'jingle'
}

#currently unused by encoder/decoder, just documenting them here
shouts = {
	0x0: 'heeey',
	0x1: 'miss_kamila',
	0x2: 'cant_believe',
	0x3: 'ha_ha_ha',
	0x4: 'it_cant_be',
	0x5: 'dont_listen',
	0x6: 'welcome',
	0x7: 'hate_red_things',
	0x8: 'who_am_i',
	0x9: 'we_did_it',
	0xa: 'didnt_we',
	0xb: 'ill_never_forget_it',
	0xc: 'ill_never_forget_you',
	0xd: 'we_have_to',
	0xe: 'not_fair',
	0xf: 'missile',
	0x10: 'im_missile',
	0x11: 'its_missile',
	0x12: 'ill_try',
	0x13: 'amelie',
	0x14: 'is_that_you',
	0x15: 'blank?_nooo',
	0x16: 'cant_read',
	0x17: 'who_shot_me',
	0x18: 'you_bet_i_did',
	0x19: 'im_very_sorry',
	0x1a: 'of_course',
	0x1b: 'of_course_we_will',
	0x1c: 'naturally',
	0x1d: 'from_terrible_tree',
	0x1e: 'you_bet',
	0x1f: 'you_got_it',
	0x20: 'over_and_over',
	0x21: 'ill_do_it',
	0x22: 'sissel',
	0x23: 'got_it',
	0x24: 'wow',
	0x25: 'hello?',
	0x26: 'miss_lynne',
	0x27: 'i_hope',
	#0x28: 'blank',
	#the table loops after this? shouldn't be exactly the same though, judging off where it's used. most shouts in the game tend to be 40-80? and they don't match up with just looping this over and over as is
}

commands = {
	0xff01: '[BREAK]\n',#moves to a new line
	0xff02: '[WAIT]\n\n',#waits for input, then clears the textbox.
	0xff03: '[CENTER]',#centers text printed afterwards, until a new line. produced undesirable results when used in the middle of a line.
	0xff04: '[SPEED {}]',#text speed, higher seems slower. frames per character?
	0xff05: '[COLOR {}]',#changes text color
	0xff06: '[SHOW]',#shows the textbox
	0xff07: '[HIDE]',#hides the textbox
	0xff08: '[PORTRAIT {}]\n',#portraits have different barks on appearing
	
	0xff0c: '[PAUSE {}]',#pauses text output. measured in frames?
	0xff0d: '[SFX {}]',#sound effects
	0xff0e: '[FUN_0E {}]',#unknown. only used in police chief's office when rindge reports lynne's appearance at point X, with the value 0x86, and seems to have no effect. maybe it's deprecated
	0xff0f: '[FLASH]',#flashes the screen white
	0xff10: '[SHAKE {} FOR {}]',#time measured in frames?
	
	0xff15: '[CLEAR IN {}]\n\n',#clears the textbox after some time. measured in frames?
	0xff16: '[PARAGRAPH]\n\n',#breaks up narrator text. softlocks when used in a text box.
	0xff17: '[BIG]',#makes text after it big. put another one to make text size normal.
	
	0xff19: '[FADE_PORTRAIT {} IN {}]\n',#lower FADE is slower. no portrait barks?
	
	0xff1b: '[MINI_PORTRAIT {}]\n',#mini portraits on the side of dialogue boxes
	0xff1c: '[MUSIC {}]',#changes music track.
	0xff1d: '[FADE_MUSIC {} TO {} IN {}]',#fades a bgm track to the given volume, over the given time. (frames again?)
	0xff1e: '[MUSIC_OFF {}]',#fades music out over the given time (frames again?)
	
	0xff20: '[LOWER {}]',#drops text down, more goes lower.
	0xff21: '[SCRIPTED_PAUSE]',#pauses until a scripted condition is met. not available on all dialogue. does not clear the textbox.
	0xff22: '[APPEAR {}]',#affects fade in speed of narrator text. since it's used to accelerate fade in speed rather than slow it down, i'll just call it 'appear'. could use more testing, effects of the number may not be linear.
	0xff23: '[SKIP]',#attempts to skip the remainder of the current textbox, doesn't allow waiting for input
	0xff24: '[FADE {}]',#fades text in all at once.
	0xff25: '[SHAKE2 {}]',#what's the difference between this and 0xff10?
	0xff27: '[SHAKE3 {} {}]',#what's with all these shakes???
	0xff28: '[VOLUME {} {}]',#changes music volume (X volume in Y frames?)
	
	0xff2b: '[CONFIRM_SFX {}]',#changes the sound effect that plays when confirming the dialogue
	0xff2c: '[FOCUS {}]',#flashes background white and then fades to black. higher number is slower. (number of frames?)
	0xff2d: '[START Event {}, Scene {}]\n',#Event # seems to roughly correlate with story progress. Scene # seems to be sequential within each event, usually. some files contain scenes from multiple events... as of now, unsure how the game uses this information or if it even matters.
	0xff2e: '[SHOUT {}]',#fills the text box with an image, showing a message in a large font. unsure why it's sometimes accompanied by normal text and other tags. needs another table...
	0xff2f: '[RIGHT]',#right aligns text, distorts text if used in the middle of dialogue, just like center
	
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
	'inside': '0x{0:x}'
}