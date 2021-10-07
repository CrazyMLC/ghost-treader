CXX=g++
CXXFLAGS=-shared -O3 -fPIC -fopenmp -fno-rtti -fno-exceptions
OUT=lz11maxbin.so
SOURCES=compressor.cpp

all: lz11maxbin.so
.PHONY: all

lz11maxbin.so: compressor.cpp compressor.h
	${CXX} ${CXXFLAGS} -o ${OUT} ${SOURCES}

clean:
	${RM} ${OUT}
