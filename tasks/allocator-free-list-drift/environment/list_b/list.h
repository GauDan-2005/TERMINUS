#ifndef LIST_H
#define LIST_H

#include "../include/arena.h"
#include "../include/block.h"

void xb1(Arena *a, Block *b);
void list_remove(Arena *a, Block *b);
void list_coalesce(Arena *a, Block *b);
int q8f_blk(Arena *a, Block *oldb, size_t need, size_t *merged_out);

#endif
