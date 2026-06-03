#include "../include/cell_view.h"
#include "../include/topo_link.h"

void op_b(CellPatch *a, const CellPatch *b, int c, int d) {
    if (!a || !b) return;
    int width = (b->n < 8) ? b->n : 8;
    a->n = width;
    for (int i = 0; i < width; i++) {
        int src = i + d;
        if (src < 0) src = 0;
        if (src >= b->n) src = b->n - 1;
        a->vol[i] = b->vol[src];
        for (int v = 0; v < NVAR; v++) {
            a->q[i * NVAR + v] = b->q[src * NVAR + v];
        }
    }
    (void)c;
}
