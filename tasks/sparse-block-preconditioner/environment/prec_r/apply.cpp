#include "../include/matrix_view.h"

void step_r(const BsrPack *a, const double *b, double *c) {
    int dim = a->n;
    for (int i = 0; i < dim; i++) {
        int blk = i / a->bs;
        int loc = i % a->bs;
        int src = blk;
        if (a->reorder) {
            src = a->perm[blk];
        }
        double inv = a->diag_inv[src * a->bs + loc];
        if (inv == 0.0) {
            inv = 1.0;
        }
        c[i] = inv * b[i];
    }
}
