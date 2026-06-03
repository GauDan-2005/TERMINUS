#ifndef ARENA_H
#define ARENA_H

#include "block.h"
#include "stats.h"

#include <stddef.h>

#define HEAP_BYTES 65536
#define MAX_SLOTS 64
#define FL_MAP_SZ (HEAP_BYTES / 8)

typedef struct Arena {
    unsigned char mem[HEAP_BYTES];
    size_t used;
    Block head;
    Block fl_head;
    size_t fl_link_next[FL_MAP_SZ];
    size_t fl_link_prev[FL_MAP_SZ];
    void *slots[MAX_SLOTS];
    size_t slot_payload[MAX_SLOTS];
    int slot_live[MAX_SLOTS];
    int slot_count;
    Stats stats;
} Arena;

void arena_init(Arena *a);
int arena_slot_alloc(Arena *a, size_t req);
int arena_slot_free(Arena *a, int idx);
int arena_slot_realloc(Arena *a, int idx, size_t req);
size_t arena_heap_sig(const Arena *a);
size_t arena_fl_sig(const Arena *a);
int arena_fl_count(const Arena *a);

#endif
