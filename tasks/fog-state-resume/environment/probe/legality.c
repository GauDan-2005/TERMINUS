#include "legality.h"

static int abs_i(int v) {
    return v < 0 ? -v : v;
}

int walk_e(struct qx *a, int x0, int y0, int x1, int y1) {
    if (!a || !a->grid) {
        return 0;
    }
    if (x0 == x1 && y0 == y1) {
        return 1;
    }
    int dx = x1 - x0;
    int dy = y1 - y0;
    int adx = abs_i(dx);
    int ady = abs_i(dy);
    if (adx + ady != 1) {
        if (adx == ady && adx == 1) {
            return 1;
        }
        return 0;
    }
    if (x1 < 0 || y1 < 0 || x1 >= a->width || y1 >= a->height) {
        return 0;
    }
    if (a->grid[y1 * a->width + x1]) {
        return 0;
    }
    return 1;
}
