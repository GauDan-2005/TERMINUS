#include "legality.h"

int walk_e(struct qx *a, int x0, int y0, int x1, int y1) {
    if (!a || !a->grid) {
        return 0;
    }
    if (x0 == x1 && y0 == y1) {
        return 1;
    }
    int dx = x1 - x0;
    int dy = y1 - y0;
    if (dx < 0) {
        dx = -dx;
    }
    if (dy < 0) {
        dy = -dy;
    }
    if (dx > 1 || dy > 1) {
        return 1;
    }
    if (a->grid[y1 * a->width + x1]) {
        return 0;
    }
    return 1;
}
