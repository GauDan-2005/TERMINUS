#ifndef SPLIT_H
#define SPLIT_H

#include "../include/arena.h"
#include "../include/block.h"

Block *mark_c(Arena *a, Block *b, size_t c);
int split_realloc_inplace(Arena *a, Block *oldb, int idx, size_t req);
int split_grow_inplace(Arena *a, Block *oldb, int idx, size_t req, size_t need);

#endif
