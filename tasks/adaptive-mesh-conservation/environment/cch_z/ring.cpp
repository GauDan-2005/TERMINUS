#include "../include/cell_view.h"

#define RING_CAP 16

void phase_z(const CellPatch *a, int b, CellPatch *c) {
    if (!a || !c) return;
    static double ring[RING_CAP * NVAR];
    static int head = 0;
    int n = (a->n < MAX_LEAVES) ? a->n : MAX_LEAVES;
    for (int v = 0; v < NVAR; v++) {
        double acc = 0.0;
        for (int i = 0; i < n; i++) acc += a->q[i * NVAR + v];
        ring[(head % RING_CAP) * NVAR + v] = (n > 0) ? acc / n : 0.0;
    }
    head = (head + 1) % RING_CAP;
    c->n = 1;
    c->vol[0] = (double)b;
    for (int v = 0; v < NVAR; v++) c->q[v] = ring[v];
}
