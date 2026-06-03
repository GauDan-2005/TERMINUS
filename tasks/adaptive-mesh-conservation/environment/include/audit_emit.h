#ifndef AUDIT_EMIT_H
#define AUDIT_EMIT_H

#include "cell_view.h"

struct ScenarioOutcome {
    char name[32];
    double base_total[NVAR];
    double after_total[NVAR];
    double resumed_total[NVAR];
    double drift_ratio;
    int balanced;
    int base_match;
    int adjacency;
    double halo_q[NVAR];
};

void emit_one(const ScenarioOutcome *a, const char *out_path);
void emit_matrix(const ScenarioOutcome *a, int n, const char *out_path);

#endif
