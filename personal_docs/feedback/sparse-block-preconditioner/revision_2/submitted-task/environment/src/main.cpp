#include "../include/case_spec.h"
#include "../include/solver_report.h"

#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

int run_u(const CaseSpec *spec, const char *out_dir, SolveResult *out);

static const char *CASES[] = {"basalt", "flint", "shale", "garnet", "mica", "opal", NULL};

static int run_named(const char *name, const char *out_dir, SolveResult *res) {
    char path[512];
    CaseSpec spec;
    snprintf(path, sizeof(path), "/app/data/cases/%s.case", name);
    if (case_load(path, &spec) != 0) {
        return -1;
    }
    return run_u(&spec, out_dir, res);
}

int main(int argc, char **argv) {
    const char *out_dir = "/app/output";
    mkdir(out_dir, 0755);
    if (argc >= 2 && strcmp(argv[1], "matrix") == 0) {
        SolveResult cases[6];
        int n = 0;
        for (int i = 0; CASES[i]; i++) {
            if (run_named(CASES[i], out_dir, &cases[n]) != 0) {
                return 1;
            }
            n++;
        }
        if (emit_matrix(cases, n, "/app/output/solver-audit.json") != 0) {
            return 1;
        }
        return 0;
    }
    if (argc >= 3 && strcmp(argv[1], "one") == 0) {
        SolveResult res;
        char audit[512];
        if (run_named(argv[2], out_dir, &res) != 0) {
            return 1;
        }
        snprintf(audit, sizeof(audit), "/app/output/%s-audit.json", argv[2]);
        return emit_t(&res, audit) != 0;
    }
    fprintf(stderr, "usage: solverctl matrix | solverctl one <case>\n");
    return 1;
}
