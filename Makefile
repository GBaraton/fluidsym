LIBS    = -lm
CC		= gcc

CFLAGS =  -O3
DEBUG_CFLAGS = -Wall -Wextra -g 
# OPTI_FLAGS = -march=native -mavx2 -mfpmath=sse -msse4 -fopt-info-vec-all=gcc.optrpt

REQ = main.c fsym.c

# fsym_deb: $(REQ) 
# 	$(CC) $(DEBUG_CFLAGS) -o $@ $^ $(LIBS)

fsym: $(REQ)
	$(CC) $(DEBUG_CLFAGS) $(CFLAGS) -o $@ $^ $(LIBS)

valgrind:
	valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose ./fsym
