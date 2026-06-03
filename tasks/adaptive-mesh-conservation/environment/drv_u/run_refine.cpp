#include "phases.h"
#include "../include/flow_record.h"
#include "../include/topo_link.h"

#include <string.h>

void phase_grow(SimState *st, const ScenarioSpec *spec) {
    CellGrid coarse = st->grid;
    CellGrid leaves;
    leaves.n = 0;
    st->n_coarse = spec->n_coarse;
    for (int c = 0; c < spec->n_coarse; c++) {
        int k = spec->leaf_count[c];
        if (k < 1) k = 1;
        int sumw = 0;
        for (int j = 0; j < k; j++) sumw += spec->leaf_weight[c][j];
        if (sumw <= 0) sumw = 1;
        st->coarse_start[c] = leaves.n;
        st->coarse_len[c] = k;
        double vj[MAX_LEAVES];
        double vtot = 0.0;
        double jw = 0.0;
        for (int j = 0; j < k; j++) {
            vj[j] = coarse.cells[c].vol * (double)spec->leaf_weight[c][j] / (double)sumw;
            vtot += vj[j];
            jw += vj[j] * (double)j;
        }
        double jbar = (vtot > 0.0) ? jw / vtot : 0.0;
        for (int j = 0; j < k; j++) {
            int gi = leaves.n++;
            leaves.cells[gi].idx = gi;
            leaves.cells[gi].vol = vj[j];
            double f = (k > 1) ? (1.0 + LEAF_SPREAD * ((double)j - jbar)) : 1.0;
            for (int v = 0; v < NVAR; v++) {
                leaves.cells[gi].q[v] = coarse.cells[c].q[v] * f;
            }
            leaves.cells[gi].tier = (k > 1) ? 1 : 0;
            leaves.cells[gi].parent = (k > 1) ? c : -1;
        }
    }
    st->grid = leaves;

    int changed[MAX_CELLS];
    int nch = 0;
    for (int i = 0; i < leaves.n; i++) changed[nch++] = i;
    step_n(&st->grid, changed, nch, &st->topo);

    st->bank.n_pending = 0;
    if (!spec->do_flux) return;
    for (int c = 0; c < spec->n_coarse; c++) {
        int k = st->coarse_len[c];
        if (k < 2) continue;
        int start = st->coarse_start[c];
        double vsum = 0.0;
        double wq[NVAR] = {0.0, 0.0, 0.0};
        for (int j = 0; j < k; j++) {
            const CellView *cell = &st->grid.cells[start + j];
            vsum += cell->vol;
            for (int v = 0; v < NVAR; v++) wq[v] += cell->vol * cell->q[v];
        }
        double qbar[NVAR];
        for (int v = 0; v < NVAR; v++) qbar[v] = (vsum > 0.0) ? wq[v] / vsum : 0.0;
        EdgePulse ep;
        ep.base_idx = start;
        ep.subfaces = k;
        for (int j = 0; j < k; j++) {
            const CellView *cell = &st->grid.cells[start + j];
            for (int v = 0; v < NVAR; v++) {
                ep.flux_vals[j * NVAR + v] =
                    REFLUX_RATE * cell->vol * (qbar[v] - cell->q[v]);
            }
        }
        op_m(&ep, &st->bank);
    }
}
