#include "../include/arena.h"
#include "../list_b/list.h"
#include "../move_d/move.h"
#include "../pool_a/tag.h"
#include "../split_c/split.h"

int arena_slot_alloc(Arena *a, size_t req);
int arena_slot_free(Arena *a, int idx);

int arena_slot_realloc(Arena *a, int idx, size_t req) {
    if (idx < 0 || idx >= a->slot_count || !a->slot_live[idx]) {
        return -1;
    }
    Block oldb;
    size_t old_pay;
    size_t need;
    oldb.base = a->mem;
    oldb.off = (size_t)((unsigned char *)a->slots[idx] - a->mem - HDR_SIZE);
    old_pay = a->slot_payload[idx];
    need = blk_align(req + HDR_SIZE + FTR_SIZE);
    if (need <= tag_read_size(&oldb)) {
        return split_realloc_inplace(a, &oldb, idx, req);
    }
    if (split_grow_inplace(a, &oldb, idx, req, need) >= 0) {
        return idx;
    }
    {
        int nidx = arena_slot_alloc(a, req);
        if (nidx < 0) {
            return -1;
        }
        xc2(a->slots[nidx], a->slots[idx], old_pay);
        arena_slot_free(a, idx);
        return nidx;
    }
}
