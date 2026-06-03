#include "../include/cell_view.h"
#include "../include/topo_link.h"

int step_n(CellGrid *a, const int *b, int c, TopoLink *d) {
    if (!a || !d) return -1;
    int n = a->n;
    for (int i = 0; i < n; i++) {
        d->parent[i] = a->cells[i].parent;
    }
    if (b && c > 0) {
        for (int i = 0; i < c && i < n; i++) {
            int idx = b[i];
            if (idx >= 0 && idx < n) {
                d->parent[idx] = a->cells[idx].parent;
            }
        }
    }
    return 0;
}
