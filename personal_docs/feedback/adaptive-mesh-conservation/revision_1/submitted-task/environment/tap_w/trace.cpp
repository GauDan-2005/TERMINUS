#include "../include/cell_view.h"
#include "../include/topo_link.h"

#include <stdio.h>
#include <stdlib.h>

int stamp_w(CellGrid *a, const int *b, int c, TopoLink *d) {
    if (!a || !d) return -1;
    const char *env = getenv("SCN_TRACE");
    if (!env || env[0] != '1') return 0;
    int touched = 0;
    for (int i = 0; i < c; i++) {
        int idx = b ? b[i] : i;
        if (idx < 0 || idx >= a->n) continue;
        fprintf(stderr, "[trace] cell=%d tier=%d vol=%.6f\n",
                idx, a->cells[idx].tier, a->cells[idx].vol);
        touched++;
    }
    return touched;
}
