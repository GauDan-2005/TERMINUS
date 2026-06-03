#ifndef LEGALITY_H
#define LEGALITY_H

struct qx {
    int width;
    int height;
    int *grid;
};

int walk_e(struct qx *a, int x0, int y0, int x1, int y1);

#endif
