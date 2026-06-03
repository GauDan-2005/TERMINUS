#include "../include/arena.h"
#include "../pool_a/tag.h"

static size_t fl_ix(size_t off) {
    return off >> 3;
}

size_t arena_heap_sig(const Arena *a) {
    size_t sig = 0;
    size_t off = 0;
    while (off < a->used) {
        Block b;
        b.base = (unsigned char *)a->mem;
        b.off = off;
        size_t total = tag_read_size(&b);
        if (total == 0) {
            break;
        }
        if (z_is_flag(&b)) {
            sig += total * 17;
        }
        off += total;
    }
    return sig;
}

size_t arena_fl_sig(const Arena *a) {
    size_t sig = 0;
    size_t cur = a->fl_head.off;
    while (cur != FL_END) {
        Block b = {(unsigned char *)a->mem, cur};
        sig += tag_read_size(&b);
        cur = a->fl_link_next[fl_ix(cur)];
    }
    return sig;
}

int arena_fl_count(const Arena *a) {
    int c = 0;
    size_t cur = a->fl_head.off;
    while (cur != FL_END) {
        c++;
        cur = a->fl_link_next[fl_ix(cur)];
    }
    return c;
}
