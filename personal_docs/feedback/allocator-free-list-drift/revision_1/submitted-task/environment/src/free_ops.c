#include "../include/arena.h"
#include "../acct_e/acct.h"
#include "../list_b/list.h"
#include "../pool_a/tag.h"

#include <string.h>

int arena_slot_free(Arena *a, int idx) {
    if (idx < 0 || idx >= a->slot_count || !a->slot_live[idx]) {
        return -1;
    }
    Block b;
    b.base = a->mem;
    b.off = (size_t)((unsigned char *)a->slots[idx] - a->mem - HDR_SIZE);
    size_t total = tag_read_size(&b);
    z_set_flag(&b, 0);
    xd3(&a->stats, -(ssize_t)total);
    a->stats.live_blocks--;
    a->slot_live[idx] = 0;
    list_coalesce(a, &b);
    return 0;
}
