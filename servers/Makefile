APPS=single proc_spawn

all: $(APPS)

single: single.o
	gcc single.o -o single

proc_spawn: proc_spawn.o
	gcc proc_spawn.o -o proc_spawn

%.o: %.c
	gcc -std=c99 -c $< -o $@

clean:
	rm -f *~ *.o $(APPS)
