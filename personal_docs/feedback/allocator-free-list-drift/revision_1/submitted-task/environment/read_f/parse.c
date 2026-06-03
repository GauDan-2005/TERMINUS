#include "../include/plan.h"

#include <stdio.h>
#include <string.h>

int plan_load(const char *path, Plan *out) {
    FILE *fp = fopen(path, "r");
    char line[256];
    if (!fp) {
        return -1;
    }
    memset(out, 0, sizeof(*out));
    {
        const char *slash = strrchr(path, '/');
        const char *base = slash ? slash + 1 : path;
        strncpy(out->name, base, sizeof(out->name) - 1);
        char *dot = strchr(out->name, '.');
        if (dot) {
            *dot = '\0';
        }
    }
    while (fgets(line, sizeof(line), fp)) {
        char op[32];
        size_t sz = 0;
        int idx = 0;
        int nidx = 0;
        if (line[0] == '#' || line[0] == '\n') {
            continue;
        }
        if (sscanf(line, "ALLOC %zu", &sz) == 1) {
            PlanOp *p = &out->ops[out->op_count++];
            p->kind = OP_ALLOC;
            p->size = sz;
            p->index = -1;
        } else if (sscanf(line, "FREE %d", &idx) == 1) {
            PlanOp *p = &out->ops[out->op_count++];
            p->kind = OP_FREE;
            p->index = idx;
        } else if (sscanf(line, "REALLOC %d %zu", &idx, &sz) == 2) {
            PlanOp *p = &out->ops[out->op_count++];
            p->kind = OP_REALLOC;
            p->index = idx;
            p->size = sz;
        } else if (sscanf(line, "%31s %d %zu %d", op, &idx, &sz, &nidx) >= 2) {
            (void)op;
            (void)nidx;
        }
    }
    fclose(fp);
    return 0;
}
