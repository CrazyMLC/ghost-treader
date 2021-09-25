Unlike decode.py and encode.py, the scripts in this folder are not intended to be user-facing.
Comparatively, their interfaces are either limited or nonexistant.
======================================================

compress.py - From magical, encodes files. Unused, as of this writing.
lzss3.py - Also from magical, decodes files. Also unused as of writing.

font.py - Creates images out of .imb files. puts it all into a .\font\ folder. May be used in the future to create a text previewer.

message.py - Describes the Message class, which does the job of converting bytes into text, and text into bytes, using tables.py.
tables.py - The Byte-to-Text dictionary for Ghost Trick's 1LMG files.

__init__.py - Allows scripts in this folder to be accessed externally.
