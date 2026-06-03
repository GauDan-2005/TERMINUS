#include <stdio.h>
#include "legality.h"

int list_tiles(struct qx *a) {
    if (!a || !a->grid) {
        return 0;
    }
    for (int y = 0; y < a->height; y++) {
        for (int x = 0; x < a->width; x++) {
            if (a->grid[y * a->width + x]) {
                printf("%d,%d\n", x, y);
            }
        }
    }
    return 0;
}
