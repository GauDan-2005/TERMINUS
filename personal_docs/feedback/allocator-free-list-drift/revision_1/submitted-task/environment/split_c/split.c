#include "../include/arena.h"
#include "../list_b/list.h"
#include "../pool_a/tag.h"

#include <stddef.h>

static int on_fl(Arena *a, size_t off) {
    size_t ix = off >> 3;
    return a->fl_head.off == off || a->fl_link_prev[ix] != FL_END || a->fl_link_next[ix] != FL_END;
}

Block *mark_c(Arena *a, Block *b, size_t c) {
    size_t total = tag_read_size(b);
    size_t need = blk_align(c + HDR_SIZE + FTR_SIZE);
    if (total < need + MIN_BLK) {
        return NULL;
    }
    size_t rem = total - need;
    if (on_fl(a, b->off)) {
        list_remove(a, b);
    }
    xa0(b, need);
    z_set_flag(b, 1);
    Block tail;
    tail.base = b->base;
    tail.off = b->off + need;
    xa0(&tail, rem);
    z_set_flag(&tail, 0);
    xb1(a, &tail);
    return NULL;
}
