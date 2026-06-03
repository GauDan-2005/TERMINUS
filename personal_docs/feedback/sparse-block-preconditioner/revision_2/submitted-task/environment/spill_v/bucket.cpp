#include "../include/case_spec.h"
#include "../include/solver_report.h"

int run_u(const CaseSpec *spec, const char *out_dir, SolveResult *out);

int spill_bucket(int v) {
    return (v % 7) + 1;
}
