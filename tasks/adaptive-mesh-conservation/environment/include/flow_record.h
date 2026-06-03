#ifndef FLOW_RECORD_H
#define FLOW_RECORD_H

#include "cell_view.h"

struct EdgePulse {
    int base_idx;
    int subfaces;
    double flux_vals[MAX_LEAVES * NVAR];
};

struct FluxBank {
    int n_pending;
    int leaf[MAX_FACES];
    double flux[MAX_FACES * NVAR];
};

void op_m(const EdgePulse *a, FluxBank *b);

#endif
