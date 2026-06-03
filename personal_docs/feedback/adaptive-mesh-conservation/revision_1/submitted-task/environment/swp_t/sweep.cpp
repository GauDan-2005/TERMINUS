#include "../include/cell_view.h"

typedef void (*cell_fn)(CellView *, void *);

void traverse_t(CellGrid *a, cell_fn fn, void *ctx) {
    if (!a || !fn) return;
    for (int i = 0; i < a->n; i++) {
        fn(&a->cells[i], ctx);
    }
}

double span_t(const CellGrid *a) {
    if (!a || a->n == 0) return 0.0;
    double lo = a->cells[0].vol;
    double hi = a->cells[0].vol;
    for (int i = 1; i < a->n; i++) {
        double v = a->cells[i].vol;
        if (v < lo) lo = v;
        if (v > hi) hi = v;
    }
    return hi - lo;
}
