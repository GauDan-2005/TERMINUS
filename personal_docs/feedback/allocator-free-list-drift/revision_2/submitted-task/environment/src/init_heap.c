#include "../include/arena.h"
#include "../list_b/list.h"
#include "../pool_a/tag.h"

#include <string.h>

void arena_init(Arena *a) {
    Block h;
    size_t i;
    memset(a, 0, sizeof(*a));
    for (i = 0; i < FL_MAP_SZ; i++) {
        a->fl_link_next[i] = FL_END;
        a->fl_link_prev[i] = FL_END;
    }
    a->used = HEAP_BYTES;
    h.base = a->mem;
    h.off = 0;
    xa0(&h, HEAP_BYTES);
    z_set_flag(&h, 0);
    a->head = h;
    a->fl_head.base = h.base;
    a->fl_head.off = FL_END;
    xb1(a, &h);
}
