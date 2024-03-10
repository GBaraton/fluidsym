LIBS    = -lm
CC		= gcc
CFLAGS	=  -O3

DEBUG_CFLAGS	= -Wall -Wextra -g 
OPTI_FLAGS		= -march=native -mavx2 -mfpmath=sse -msse4 -fopt-info-vec-all=gcc.optrpt

SRC		= src
SRCS	= $(wildcard $(SRC)/*.c)

TEST		= test
TESTS		= $(wildcard $(TEST)/*.c)
TESTBINS	= $(patsubst $(TEST)/%.c, $(TEST)/bin/%, $(TESTS))


# fsym_release: $(SRCS) 
# 	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

fsym: $(SRCS)
	$(CC) $(DEBUG_CLFAGS) $(CFLAGS) -o $@ $^ $(LIBS)

valgrind:
	valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose ./fsym

$(TEST)/bin/%: $(TEST)/%.c
	$(CC) $(CFLAGS) $< -o $@ -lcriterion 

test: $(TESTBINS)
	for test in $(TESTBINS) ; do ./$$test ;


.PHONY: fsym
