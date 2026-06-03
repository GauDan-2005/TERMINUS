#pragma once

#include <stddef.h>

#define MAX_BLOCKS 8
#define MAX_BS 4
#define MAX_NNZ_BLOCKS 64
#define CASE_NAME_LEN 32

typedef struct {
    int rb;
    int cb;
    double vals[MAX_BS * MAX_BS];
} BlockEntry;

typedef struct {
    char name[CASE_NAME_LEN];
    int nblocks;
    int bs;
    int reorder;
    int perm[MAX_BLOCKS];
    int block_count;
    BlockEntry blocks[MAX_NNZ_BLOCKS];
    double rhs[MAX_BLOCKS * MAX_BS];
} CaseSpec;

int case_load(const char *path, CaseSpec *spec);
