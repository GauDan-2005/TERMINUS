#include "../include/arena.h"
#include "../acct_e/acct.h"
#include "../list_b/list.h"
#include "../pool_a/tag.h"

void slot_take_whole(Arena *a, Block *fit, size_t total) {
    list_remove(a, fit);
    xa0(fit, total);
    z_set_flag(fit, 1);
    xd3(&a->stats, (ssize_t)total);
}
