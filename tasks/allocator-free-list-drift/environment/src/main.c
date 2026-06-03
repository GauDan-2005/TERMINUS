#include "../include/plan.h"
#include "../include/report.h"

#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

static const char *CASES[] = {"cedar", "jade", "slate", "coral", "onyx", "pearl", NULL};

static int run_named(const char *name, const char *out_dir, CaseResult *res) {
    char path[512];
    Plan plan;
    snprintf(path, sizeof(path), "/app/data/cases/%s.plan", name);
    if (plan_load(path, &plan) != 0) {
        return -1;
    }
    return run_case(&plan, out_dir, res);
}

int main(int argc, char **argv) {
    const char *out_dir = "/app/output";
    mkdir(out_dir, 0755);
    if (argc >= 2 && strcmp(argv[1], "matrix") == 0) {
        CaseResult cases[6];
        int n = 0;
        for (int i = 0; CASES[i]; i++) {
            if (run_named(CASES[i], out_dir, &cases[n]) != 0) {
                return 1;
            }
            n++;
        }
        if (emit_matrix(cases, n, "/app/output/alloc-audit.json") != 0) {
            return 1;
        }
        return 0;
    }
    if (argc >= 3 && strcmp(argv[1], "one") == 0) {
        CaseResult res;
        if (run_named(argv[2], out_dir, &res) != 0) {
            return 1;
        }
        char audit[512];
        snprintf(audit, sizeof(audit), "/app/output/%s-audit.json", argv[2]);
        return emit_e(&res, audit) != 0;
    }
    fprintf(stderr, "usage: allocctl matrix | allocctl one <case>\n");
    return 1;
}
