all: lz11.so
.PHONY: all

lz11.so: lz11.cpp lz11.h
	g++ -shared -O3 -o lz11.so lz11.cpp
	cp lz11.so ..