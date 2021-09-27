CC="g++"
CXXFLAGS="-shared -03 -fPIC"
OUT="lz11.so"
SOURCES="lz11.cpp"

all: lz11.so
.PHONY: all

lz11.so: lz11.cpp lz11.h
	${CC} ${CXXFLAGS} -o ${OUT} ${SOURCES}
	cp ${OUT} ..

clean:
	${RM} ${OUT}
