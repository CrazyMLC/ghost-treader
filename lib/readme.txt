compress.py - from magical, encodes files. unused, as of this writing.
lzss3.py - also from magical, decodes files. also unused as of writing.

font.py - creates images out of .imb files. puts it all into a .\font\ folder.

message.py - does the job of converting bytes into text, and text into bytes, using tables.py
tables.py - has information on what each byte in 1LMG files mean.

__init__.py - allows scripts in this folder to be accessed externally