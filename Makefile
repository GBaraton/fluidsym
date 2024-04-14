LIBS    = -lm
CC		= gcc

CFLAGS			= 
DEBUG_CFLAGS	= -Wall -Wextra -g -DDEBUG
OPTI_FLAGS		= -march=native -mavx2 -mfpmath=sse -msse4 -fopt-info-vec-all=gcc.optrpt -O3

SRC		= src
SRCS	= $(wildcard $(SRC)/*.c)
SRCS_MINUS_MAIN = $(SRC)/fsym.c

TEST		= tests
TESTS		= $(wildcard $(TEST)/*.c)
TESTBINS	= $(patsubst $(TEST)/%.c, $(TEST)/bin/%, $(TESTS))

EXEFILE     = fsym

# fsym_release: $(SRCS) 
# 	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

all: fsym

fsym: $(SRCS)
	$(CC) $(DEBUG_CFLAGS) $(CFLAGS) -o $(EXEFILE) $^ $(LIBS)

release: $(SRCS)
	$(CC) $(OPTI_FLAGS) $(CFLAGS) -o $(EXEFILE) $^ $(LIBS)

valgrind:
	valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose ./fsym

# Compiles tests
$(TEST)/bin/%: $(TEST)/%.c 
	$(CC) $(DEBUG_CFLAGS) $< $(SRCS_MINUS_MAIN) -o $@ -lcriterion  $(LIBS)

# Runs tests, 
test: clean_tests $(TESTBINS)
	for test in $(TESTBINS) ; do ./$$test ; done

clean_tests: 
	rm -f $(TEST)/bin/* 2>/dev/null

clean: clean_tests
	rm -f fsym 

.PHONY: fsym release clean test $(TEST)/bin/%
