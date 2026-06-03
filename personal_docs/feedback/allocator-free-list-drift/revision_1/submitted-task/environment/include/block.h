#ifndef BLOCK_H
#define BLOCK_H

#include <stddef.h>

#define HDR_SIZE 16
#define FTR_SIZE 8
#define FL_END ((size_t)-1)
#define MIN_BLK 40
#define ALIGN 8

typedef struct Block {
    unsigned char *base;
    size_t off;
} Block;

static inline size_t blk_align(size_t n) {
    return (n + (ALIGN - 1)) & ~(size_t)(ALIGN - 1);
}

#endif
