#ifndef TOPO_LINK_H
#define TOPO_LINK_H

#include "cell_view.h"

struct TopoLink {
    int n_faces;
    int face_left[MAX_FACES];
    int face_right[MAX_FACES];
    int face_level[MAX_FACES];
    int parent[MAX_CELLS];
    int child0[MAX_CELLS];
    int child_count[MAX_CELLS];
};

int step_n(CellGrid *a, const int *b, int c, TopoLink *d);
void op_b(CellPatch *a, const CellPatch *b, int c, int d);

#endif
