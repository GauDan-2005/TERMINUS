#ifndef CELL_VIEW_H
#define CELL_VIEW_H

#include <stdint.h>

#define NVAR 3
#define MAX_CELLS 384
#define MAX_FACES 768
#define MAX_LEAVES 8
#define REFLUX_RATE 0.25
#define LEAF_SPREAD 0.1

struct CellView {
    int idx;
    int tier;
    int parent;
    double vol;
    double q[NVAR];
};

struct CellGrid {
    CellView cells[MAX_CELLS];
    int n;
};

struct CellPatch {
    int n;
    double vol[MAX_LEAVES];
    double q[MAX_LEAVES * NVAR];
};

void fold_q(const CellPatch *a, int b, CellPatch *c);

#endif
