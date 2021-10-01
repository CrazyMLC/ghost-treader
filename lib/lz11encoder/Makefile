CXX=g++
CXXFLAGS=-shared -O3 -fPIC
OUT=lz11bin.so
SOURCES=lz11.cpp

all: lz11bin.so
.PHONY: all

lz11bin.so: lz11.cpp lz11.h
	${CXX} ${CXXFLAGS} -o ${OUT} ${SOURCES}

clean:
	${RM} ${OUT}
