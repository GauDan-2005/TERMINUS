#include "phases.h"
#include "../include/topo_link.h"

#include <string.h>

void phase_fold(SimState *st, const ScenarioSpec *spec) {
    for (int v = 0; v < NVAR; v++) st->halo_q[v] = 0.0;

    int seam = -1;
    for (int c = 0; c < st->n_coarse; c++) {
        if (st->coarse_len[c] > 1) { seam = c; break; }
    }
    if (seam >= 0) {
        int start = st->coarse_start[seam];
        int k = st->coarse_len[seam];
        CellPatch src;
        src.n = k;
        for (int j = 0; j < k && j < MAX_LEAVES; j++) {
            src.vol[j] = st->grid.cells[start + j].vol;
            for (int v = 0; v < NVAR; v++) {
                src.q[j * NVAR + v] = st->grid.cells[start + j].q[v];
            }
        }
        CellPatch ghost;
        memset(&ghost, 0, sizeof(ghost));
        op_b(&ghost, &src, k, 1);
        for (int v = 0; v < NVAR; v++) st->halo_q[v] = ghost.q[v];
    }

    if (!spec->do_collapse) return;

    CellGrid folded;
    folded.n = 0;
    for (int c = 0; c < st->n_coarse; c++) {
        int start = st->coarse_start[c];
        int k = st->coarse_len[c];
        int gi = folded.n++;
        if (k < 2) {
            folded.cells[gi] = st->grid.cells[start];
            folded.cells[gi].idx = gi;
            folded.cells[gi].tier = 0;
            folded.cells[gi].parent = -1;
            continue;
        }
        CellPatch children;
        children.n = k;
        for (int j = 0; j < k && j < MAX_LEAVES; j++) {
            children.vol[j] = st->grid.cells[start + j].vol;
            for (int v = 0; v < NVAR; v++) {
                children.q[j * NVAR + v] = st->grid.cells[start + j].q[v];
            }
        }
        CellPatch parent;
        memset(&parent, 0, sizeof(parent));
        fold_q(&children, k, &parent);
        folded.cells[gi].idx = gi;
        folded.cells[gi].tier = 0;
        folded.cells[gi].parent = -1;
        folded.cells[gi].vol = parent.vol[0];
        for (int v = 0; v < NVAR; v++) folded.cells[gi].q[v] = parent.q[v];
    }
    for (int c = 0; c < st->n_coarse; c++) {
        st->coarse_start[c] = c;
        st->coarse_len[c] = 1;
    }
    st->grid = folded;
}
