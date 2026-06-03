#ifndef CASE_SPEC_H
#define CASE_SPEC_H

#include "cell_view.h"
#include "audit_emit.h"

#define MAX_COARSE 64

struct ScenarioSpec {
    char name[32];
    int profile;
    int n_coarse;
    int do_flux;
    int do_collapse;
    int do_restart;
    int leaf_count[MAX_COARSE];
    int leaf_weight[MAX_COARSE][MAX_LEAVES];
};

const char *app_root(void);

int load_case(const char *path, const char *section, ScenarioSpec *out);

int run_u(const ScenarioSpec *a, const char *b, ScenarioOutcome *c);

#endif
