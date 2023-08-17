LIBS    = -lm
CC		= gcc

CFLAGS =  -O3
DEBUG_CFLAGS = -Wall -Wextra -g 
# OPTI_FLAGS = -march=native -mavx2 -mfpmath=sse -msse4 -fopt-info-vec-all=gcc.optrpt

REQ = ./src/main.c ./src/fsym.c

# fsym_release: $(REQ) 
# 	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

fsym: $(REQ)
	$(CC) $(DEBUG_CLFAGS) $(CFLAGS) -o $@ $^ $(LIBS)

valgrind:
	valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose ./fsym

.PHONY: fsym
