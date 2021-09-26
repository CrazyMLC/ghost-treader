CC="g++"
CFLAGS="-shared -03"
OUT="lz11.so"
SOURCES="lz11.cpp"

all: lz11.so

lz11.so: lz11.cpp lz11.h
	${CC} ${CXXFLAGS} -o ${OUT} ${SOURCES}
	cp ${OUT} ..

clean:
	${RM} ${OUT}
