#include "../include/stats.h"

#include <stddef.h>
#include <sys/types.h>

void xd3(Stats *a, ssize_t b) {
    if (b > 0) {
        a->allocated += (size_t)b + 8;
    } else {
        a->allocated -= (size_t)(-b);
    }
    if (a->allocated > a->peak) {
        a->peak = a->allocated;
    }
}
