#ifndef STATS_H
#define STATS_H

#include <stddef.h>

typedef struct Stats {
    size_t allocated;
    size_t peak;
    size_t live_blocks;
} Stats;

#endif
