CC = gcc
CFLAGS = -g -Wall

TARGETS = simple_crash simple_test

all: $(TARGETS)

$(TARGETS): %: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm $(TARGETS)

