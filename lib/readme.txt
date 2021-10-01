Unlike decode.py and encode.py, the scripts in this folder are not intended to be user-facing.
Comparatively, their interfaces are either limited or nonexistant.
======================================================

source\lz11_*_x64.so - Binary of a modified version of unknownbrackets' lz77 compression. Provided for ease of use, but may not work on all platforms. Try running the makefile in source\ if needed.
lz11.py - A wrapper for lz11_*_x64.so

font.py - Creates images out of .imb files. puts it all into a .\font\ folder. May be used in the future to create a text previewer.

message.py - Describes the Message class, which does the job of converting bytes into text, and text into bytes, using tables.py.
tables.py - The Byte-to-Text dictionary for Ghost Trick's 1LMG files.

__init__.py - Allows scripts in this folder to be accessed externally.
