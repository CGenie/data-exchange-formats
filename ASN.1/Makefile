C_SOURCE := c-codec
INCLUDES_OLD := -I/home/przemek/asn1c-bin/share/asn1c -I${C_SOURCE}
LIBS := /home/przemek/asn1c-bin/share/lib/asn1c.o
INCLUDES := -I${C_SOURCE}

all:
	gcc test-client.c -ggdb ${C_SOURCE}/*.c ${INCLUDES} -o test-client

clean:
	rm -f *.o
	rm -f test-client
