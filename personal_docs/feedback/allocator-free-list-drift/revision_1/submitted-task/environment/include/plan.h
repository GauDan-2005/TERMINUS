#ifndef PLAN_H
#define PLAN_H

#include <stddef.h>

#define MAX_OPS 128

typedef enum {
    OP_ALLOC = 1,
    OP_FREE = 2,
    OP_REALLOC = 3
} OpKind;

typedef struct PlanOp {
    OpKind kind;
    size_t size;
    int index;
    int new_index;
} PlanOp;

typedef struct Plan {
    char name[32];
    PlanOp ops[MAX_OPS];
    int op_count;
} Plan;

int plan_load(const char *path, Plan *out);

#endif
