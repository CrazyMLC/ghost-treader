Unlike decode.py and encode.py, the scripts in this folder are not intended to be user-facing.
Comparatively, their interfaces are either limited or nonexistant.
======================================================

lz11encoder\ - Source of a modified version of unknownbrackets' lz77 compression. Binaries are provided for ease of use, but may not work on all platforms. Try running the makefile if needed.
lz11.py - A wrapper for lz11encoder

font.py - Creates images out of .imb files. puts it all into a .\font\ folder. May be used in the future to create a text previewer.

message.py - Describes the Message class, which does the job of converting bytes into text, and text into bytes, using tables.py.
tables.py - The Byte-to-Text dictionary for Ghost Trick's 1LMG files.

__init__.py - Allows scripts in this folder to be accessed externally.
