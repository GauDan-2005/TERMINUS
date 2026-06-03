#include "../include/arena.h"
#include "../pool_a/tag.h"

#include <string.h>

static size_t fl_ix(size_t off) {
    return off >> 3;
}

void slot_take_split(Arena *a, Block *fit, size_t req, size_t need);
void slot_take_whole(Arena *a, Block *fit, size_t total);

static Block make_blk(Arena *a, size_t off) {
    Block b;
    b.base = a->mem;
    b.off = off;
    return b;
}

static Block *find_fit(Arena *a, size_t need) {
    size_t cur = a->fl_head.off;
    static Block pick;
    while (cur != FL_END) {
        Block b = make_blk(a, cur);
        size_t total = tag_read_size(&b);
        if (total >= need) {
            pick = b;
            return &pick;
        }
        cur = a->fl_link_next[fl_ix(cur)];
    }
    return NULL;
}

int arena_slot_alloc(Arena *a, size_t req) {
    size_t need = blk_align(req + HDR_SIZE + FTR_SIZE);
    Block *fit = find_fit(a, need);
    size_t total;
    int idx;
    if (!fit) {
        return -1;
    }
    total = tag_read_size(fit);
    if (total >= need + MIN_BLK) {
        slot_take_split(a, fit, req, need);
    } else {
        slot_take_whole(a, fit, total);
    }
    idx = a->slot_count++;
    if (idx >= MAX_SLOTS) {
        return -1;
    }
    a->slots[idx] = fit->base + fit->off + HDR_SIZE;
    a->slot_payload[idx] = req;
    a->slot_live[idx] = 1;
    a->stats.live_blocks++;
    memset(a->slots[idx], (unsigned char)(idx + 1), req < 64 ? req : 64);
    return idx;
}
