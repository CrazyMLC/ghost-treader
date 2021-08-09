# ghost-treader
A specialized version of [ghost-tripper](https://github.com/CatTrinket/ghost-tripper) meant to deal with the text files of Capcom's DS release, *Ghost Trick: Phantom Detective*. 

## Text files?
Not counting the multiple languages, there are about 346 ".xml" files in the Ghost Trick ROM.
Approximately half of these ".xml" files contain dialogue, and the other half contain the scripting language for the game.

While presumably they were originally some form of .xml file, they've been encoded into a new format.
For our purposes, we'll refer to this new format by their first 4 bytes in ascii: 1LMG

By using this tool, you'll be able to convert these 1LMG files into human-readable text files, which you can then go on to edit in your favorite text editor.
Afterwards, you'll (eventually) be able to convert the text files back into 1LMG, and insert them into the game.

### Scripting language? Does that mean you can modify more than just the dialogue?
It's certainly possible. All the script files are self-contained, to the point where you can easily move the credits to replace the opening scene of the game.
Because of how modular the game's scenes are, it should be possible to completely rewrite the game however you like, just by editing 1LMG files. That's a ways off, though.

For now, **ghost-treader** is primarily capable of dealing with english dialogue 1LMG files.

## How to use (Windows)
1. First, you're going to need some resources.
   1. You'll need Python 3, as well as this repo cloned onto your device.
   1. You'll be needing [tinke](https://github.com/pleonex/tinke)'s binary, or one of its many forks.
   1. Then, you're going to need the Ghost Trick ROM. It's recommended that you dump the cartridge that you bought.
1. Once that's all set up, you'll have to get a **1LMG** file out of the ROM using tinke.
   1. "st01/st01_game000_Expand.en.xml.lz" is recommended for this purpose; it has the english dialogue for the opening scenes of the game.
   1. With your **.en.xml** file selected, click on the **Unpack** button.
   1. A new **.en.xml** file should show up on the list, with **[1LMG]** to the right of it. Select the file, click on the **Extract** button, and save the file somewhere.
1. This is the easy part. Drag your extracted **.en.xml** file into this project's **text.py**.
1. Check the "decoded" subfolder, and open the .txt file in your text editor of choice.
1. The next of the project's features are still under construction. Hopefully tinke won't be necessary in the future either.
   1. If you know how, you can use the .txt file to help you edit the original **.en.xml** file in a hex editor. It shows you the hex position of each message, and then you can use tables.py to help you navigate from there. After you edit, you follow a similar process to extracting to insert the file back in with tinke. Just, you know, backwards. Don't forget to Pack and Save to ROM after replacing the extracted .en.xml file...
