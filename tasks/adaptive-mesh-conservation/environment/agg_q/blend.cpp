#include "../include/cell_view.h"

void fold_q(const CellPatch *a, int b, CellPatch *c) {
    if (!a || !c) return;
    int n = (a->n < b) ? a->n : b;
    if (n <= 0) {
        c->n = 0;
        return;
    }
    double sum_vol = 0.0;
    double sum_q[NVAR] = {0.0, 0.0, 0.0};
    for (int i = 0; i < n; i++) {
        sum_vol += a->vol[i];
        for (int v = 0; v < NVAR; v++) {
            sum_q[v] += a->q[i * NVAR + v];
        }
    }
    c->n = 1;
    c->vol[0] = sum_vol;
    double inv_n = 1.0 / (double)n;
    for (int v = 0; v < NVAR; v++) {
        c->q[v] = sum_q[v] * inv_n;
    }
}
