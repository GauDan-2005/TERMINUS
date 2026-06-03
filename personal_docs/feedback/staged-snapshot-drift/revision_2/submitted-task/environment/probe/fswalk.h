#ifndef FSWALK_H
#define FSWALK_H

#include <stddef.h>

struct qx {
    unsigned long seen;
};

int walk_e(struct qx *a, const char *root, unsigned long c);
int list_q(struct qx *a, const char *b);

#endif
