APPS=single

all: $(APPS)

single: single.o
	gcc single.o -o single

%.o: %.c
	gcc -std=c99 -c $< -o $@

clean:
	rm -f *~ *.o $(APPS)
