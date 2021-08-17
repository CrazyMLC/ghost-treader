# ghost-treader
A specialized version of [ghost-tripper](https://github.com/CatTrinket/ghost-tripper) meant to deal with the text files of Capcom's DS release, *Ghost Trick: Phantom Detective*. 

## Text files?
Not counting the multiple languages, there are about 346 ".xml" files in the Ghost Trick ROM.
Approximately half of these ".xml" files contain dialogue, and the other half contain the scripting language for the game.

While presumably they were originally some form of .xml file, they've been encoded into a new format.
For our purposes, we'll refer to this new format by their first 4 bytes in ascii: 1LMG

By using this tool, you'll be able to convert these 1LMG files into human-readable text files, which you can then go on to edit in your favorite text editor.
Afterwards, you'll be able to convert the text files back into 1LMG, and insert them into the game.

### Scripting language? Does that mean you can modify more than just the dialogue?
Most of the filenames are in this format **##.xml.lz** where ## is a two letter language code.
But some of the filenames don't have any language code; these filenames end with only **.xml.lz**. These files contain the scripting language for the game.

Experiments have confirmed this, such as editing the string filepaths in root .xml.lz files, or editing object names in game .xml.lz files.
The scripting language is a bit difficult to parse though, so no progress has been made on it.

For now, **ghost-treader** is primarily capable of dealing with english dialogue 1LMG files. (Some accent characters used by other languages may not be in tables.py)

## File guide
* **decode.py** - This handles the job of decoding Ghost Trick's text files. Drag one into the script and it'll show up in the .\decoded\ folder.
* **encode.py** - Encodes your decoded text files back into a format Ghost Trick can use. Just like decode.py, just drag a decoded file in and check .\encoded\\.
* **tables.py** - The byte-to-text dictionary. This is probably the first place you should look, if you want to contribute.
* **message.py** - Defines the Message class, which holds most of the file information, and does most of the encoding/decoding work.
* **notes.txt** - Some of my personal notes on decoding the 1LMG file format and byte commands.
* **CREDITS** - The people this project wouldn't have gotten this far without.

## How to use (Windows)
1. First, you're going to need some resources.
   1. You'll need Python 3, as well as this repo cloned onto your device.
   1. You'll be needing [tinke](https://github.com/pleonex/tinke)'s binary, or one of its many forks.
   1. Then, you're going to need the Ghost Trick ROM. It's recommended that you dump the cartridge that you bought.
1. Once that's all set up, you'll have to get a **1LMG** file out of the ROM using tinke.
   1. "st01/st01_game000_Expand.en.xml.lz" is recommended for this purpose; it has the english dialogue for the opening scenes of the game.
   1. With your **.en.xml.lz** file selected, click on the **Unpack** button.
   1. A new **.en.xml.lz** file should show up on the list, with **[1LMG]** to the right of it. Select the file, click on the **Extract** button, and save the file somewhere.
1. This is the easy part. Time to edit the file!
   1. Drag your extracted **.en.xml.lz** file into this project's **decode.py**.
   1. Check the "decoded" subfolder, and open the .txt file in your text editor of choice.
   1. Make some changes! Make someone say something funny, and it'll be easy to notice.
   1. You can look at **tables.py** to find more information on the various commands that have been discovered.
1. Now to encode the text file back into a 1LMG file.
   1. Drag the text file into this project's **encode.py**.
   1. Check the "encoded" subfolder. If there weren't any errors, your file should be good to go to be reinserted with tinke.
1. Time to insert the file back into Ghost Trick.
   1. In tinke, navigate back to and select file you originally extracted. (Don't forget to unpack like before!)
   1. Click the **Change file** button and use your encoded file.
   1. Remember the file that you had selected when you clicked Unpack in tinke? You're going to have to select it again, and click **Pack**.
   1. Click **Save ROM** and save your new ROM. (Don't overwrite your original!)
1. Open the new ROM file in an emulator and admire your work.
