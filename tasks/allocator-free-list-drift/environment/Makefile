CC = gcc
CFLAGS = -std=c17 -Wall -Wextra -O2 -Iinclude

SRCS = src/main.c src/arena_core.c src/init_heap.c src/alloc_ops.c src/slot_take.c \
       src/slot_split.c src/free_ops.c src/reloc_ops.c \
       pool_a/tag.c list_b/list.c split_c/split.c \
       move_d/move.c acct_e/acct.c read_f/parse.c drive_h/run.c flow_g/report.c \
       spill_i/spill.c mirror_j/mirror.c

OBJS = $(SRCS:.c=.o)

all: bin/allocctl

bin/allocctl: $(OBJS)
	mkdir -p bin
	$(CC) $(CFLAGS) -o $@ $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJS) bin/allocctl

.PHONY: all clean
