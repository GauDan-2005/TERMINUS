#include "../include/arena.h"
#include "../acct_e/acct.h"
#include "../list_b/list.h"
#include "../pool_a/tag.h"
#include "../split_c/split.h"

int split_realloc_inplace(Arena *a, Block *oldb, int idx, size_t req) {
    size_t old_total = tag_read_size(oldb);
    size_t need = blk_align(req + HDR_SIZE + FTR_SIZE);
    if (old_total < need + MIN_BLK) {
        a->slot_payload[idx] = req;
        return idx;
    }
    z_set_flag(oldb, 0);
    xd3(&a->stats, -(ssize_t)old_total);
    mark_c(a, oldb, req);
    xd3(&a->stats, (ssize_t)need);
    a->slot_payload[idx] = req;
    return idx;
}

int split_grow_inplace(Arena *a, Block *oldb, int idx, size_t req, size_t need) {
    size_t merged;
    size_t old_total = tag_read_size(oldb);
    size_t ntotal;
    Block nb;
    nb.base = oldb->base;
    nb.off = oldb->off + old_total;
    ntotal = tag_read_size(&nb);
    if (q8f_blk(a, oldb, need, &merged) != 0) {
        return -1;
    }
    xd3(&a->stats, (ssize_t)ntotal);
    if (merged >= need + MIN_BLK) {
        z_set_flag(oldb, 0);
        xd3(&a->stats, -(ssize_t)merged);
        mark_c(a, oldb, req);
        xd3(&a->stats, (ssize_t)need);
    }
    a->slot_payload[idx] = req;
    return idx;
}

void slot_take_split(Arena *a, Block *fit, size_t req, size_t need) {
    mark_c(a, fit, req);
    xd3(&a->stats, (ssize_t)need);
}
