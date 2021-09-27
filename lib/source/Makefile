CXX=g++
CXXFLAGS=-shared -O3 -fPIC
OUT=lz11.so
SOURCES=lz11.cpp

all: lz11.so
.PHONY: all

lz11.so: lz11.cpp lz11.h
	${CXX} ${CXXFLAGS} -o ${OUT} ${SOURCES}
	cp ${OUT} ..

clean:
	${RM} ${OUT}
