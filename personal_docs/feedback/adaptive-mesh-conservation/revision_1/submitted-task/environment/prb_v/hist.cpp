#include "../include/cell_view.h"

void walk_v(const CellGrid *a, int b, int c, double *d) {
    if (!a || !d || b <= 0) return;
    for (int i = 0; i < b; i++) d[i] = 0.0;
    for (int i = 0; i < a->n; i++) {
        double key = a->cells[i].q[c % NVAR];
        int slot = (int)(key * b);
        if (slot < 0) slot = 0;
        if (slot >= b) slot = b - 1;
        d[slot] += a->cells[i].vol;
    }
}
