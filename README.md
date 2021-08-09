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

For now, **ghost-treader** is primarily capable of dealing with dialogue 1LMG files.

## How to use (Windows)
1. First, you're going to need [tinke](https://github.com/pleonex/tinke) or one of its many forks.
1. Then, you're going to need the Ghost Trick ROM. It's recommended that you get it by copying the cartridge that you own.
1. You'll have to open the ROM in tinke, and locate a file with ".xml" in its filename.
   1. Opening the "st01" folder and locating "st01_game000_Expand.en.xml.lz" is recommended for this purpose; it has the dialogue for the opening scenes of the game.
1. With your ".xml" file located, click on the "Unpack" button.
1. A new file should be visible underneath, with "[1LMG]" to the right of it. Select the file, and click on the "Extract" button.
1. After you've saved this file on your computer using tinke, drag it into "text.py" from **ghost-treader**.
1. Check the "decoded" subfolder, and open the .txt file in your text editor of choice.

(re-insertion coming soon)
