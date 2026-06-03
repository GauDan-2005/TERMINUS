#include "../include/matrix_view.h"

#include <math.h>
#include <string.h>

void fn_n(const MatrixView *a, int reorder, BsrPack *c) {
    int nb = a->nblocks;
    int bs = a->bs;
    int dim = a->n;
    int ptr = 0;
    memset(c, 0, sizeof(*c));
    c->n = dim;
    c->bs = bs;
    c->nblocks = nb;
    c->reorder = reorder;
    for (int i = 0; i < nb; i++) {
        c->perm[i] = a->perm[i];
    }
    for (int bi = 0; bi < nb; bi++) {
        int row_blk = reorder ? a->perm[bi] : bi;
        c->row_ptr[bi] = ptr;
        for (int bj = 0; bj < nb; bj++) {
            int col_blk = reorder ? ((bj + 1) % nb) : bj;
            int has = 0;
            for (int r = 0; r < bs; r++) {
                for (int cc = 0; cc < bs; cc++) {
                    int gr = row_blk * bs + r;
                    int gc = col_blk * bs + cc;
                    double v = a->a[gr * dim + gc];
                    if (fabs(v) > 0.0) {
                        has = 1;
                    }
                }
            }
            if (has) {
                c->col_idx[ptr] = col_blk;
                for (int r = 0; r < bs; r++) {
                    for (int cc = 0; cc < bs; cc++) {
                        int gr = row_blk * bs + r;
                        int gc = col_blk * bs + cc;
                        c->data[ptr * bs * bs + r * bs + cc] = a->a[gr * dim + gc];
                    }
                }
                ptr++;
            }
        }
    }
    c->row_ptr[nb] = ptr;
    for (int i = 0; i < dim; i++) {
        c->diag_inv[i] = 1.0;
    }
    for (int bi = 0; bi < nb; bi++) {
        int start = c->row_ptr[bi];
        int end = c->row_ptr[bi + 1];
        for (int k = start; k < end; k++) {
            if (c->col_idx[k] == bi) {
                for (int r = 0; r < bs; r++) {
                    double d = c->data[k * bs * bs + r * bs + r];
                    if (fabs(d) > 1e-14) {
                        c->diag_inv[bi * bs + r] = 1.0 / d;
                    }
                }
            }
        }
    }
}

void bsr_matvec(const BsrPack *pack, const double *x, double *y) {
    int nb = pack->nblocks;
    int bs = pack->bs;
    int dim = pack->n;
    for (int i = 0; i < dim; i++) {
        y[i] = 0.0;
    }
    for (int bi = 0; bi < nb; bi++) {
        int start = pack->row_ptr[bi];
        int end = pack->row_ptr[bi + 1];
        for (int k = start; k < end; k++) {
            int bj = pack->col_idx[k];
            for (int r = 0; r < bs; r++) {
                for (int c = 0; c < bs; c++) {
                    int gi = bi * bs + r;
                    int gj = bj * bs + c;
                    y[gi] += pack->data[k * bs * bs + r * bs + c] * x[gj];
                }
            }
        }
    }
}
