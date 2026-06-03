#include "../include/matrix_view.h"

#include <string.h>

void matrix_from_case(const CaseSpec *spec, MatrixView *view) {
    int dim = spec->nblocks * spec->bs;
    int i;
    memset(view, 0, sizeof(*view));
    view->n = dim;
    view->bs = spec->bs;
    view->nblocks = spec->nblocks;
    view->reorder = spec->reorder;
    for (i = 0; i < spec->nblocks; i++) {
        view->perm[i] = spec->perm[i];
    }
    for (i = 0; i < dim * dim; i++) {
        view->a[i] = 0.0;
    }
    for (i = 0; i < spec->block_count; i++) {
        const BlockEntry *be = &spec->blocks[i];
        int rb = be->rb;
        int cb = be->cb;
        int r;
        int c;
        for (r = 0; r < spec->bs; r++) {
            for (c = 0; c < spec->bs; c++) {
                int gr = rb * spec->bs + r;
                int gc = cb * spec->bs + c;
                view->a[gr * dim + gc] = be->vals[r * spec->bs + c];
            }
        }
    }
    for (i = 0; i < dim; i++) {
        view->b[i] = spec->rhs[i];
    }
}
