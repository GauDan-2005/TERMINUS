#include "../include/matrix_view.h"

void step_r(const BsrPack *a, const double *b, double *c) {
    int dim = a->n;
    for (int i = 0; i < dim; i++) {
        int blk = i / a->bs;
        int loc = i % a->bs;
        int src_blk = blk;
        if (a->reorder) {
            src_blk = (blk + 1) % a->nblocks;
        }
        c[i] = a->diag_inv[src_blk * a->bs + loc] * b[i];
    }
}
