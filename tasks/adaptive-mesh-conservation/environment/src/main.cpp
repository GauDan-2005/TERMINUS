#include "../include/audit_emit.h"
#include "../include/case_spec.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *CASE_NAMES[6] = {
    "storm", "canyon", "plume", "spire", "basin", "dune"
};

static int load_all_cases(ScenarioSpec specs[6]) {
    char cfg[256];
    snprintf(cfg, sizeof(cfg), "%s/config/cases.toml", app_root());
    for (int i = 0; i < 6; i++) {
        if (load_case(cfg, CASE_NAMES[i], &specs[i]) != 0) {
            fprintf(stderr, "failed to load case %s\n", CASE_NAMES[i]);
            return -1;
        }
    }
    return 0;
}

static int cmd_matrix(const char *out_path) {
    ScenarioSpec specs[6];
    if (load_all_cases(specs) != 0) return 1;
    ScenarioOutcome out[6];
    for (int i = 0; i < 6; i++) {
        if (run_u(&specs[i], "matrix", &out[i]) != 0) {
            fprintf(stderr, "scenario %s failed\n", specs[i].name);
            return 2;
        }
    }
    emit_matrix(out, 6, out_path);
    return 0;
}

static int cmd_one(const char *name, const char *out_path) {
    ScenarioSpec specs[6];
    if (load_all_cases(specs) != 0) return 1;
    for (int i = 0; i < 6; i++) {
        if (strcmp(specs[i].name, name) == 0) {
            ScenarioOutcome res;
            if (run_u(&specs[i], "one", &res) != 0) return 3;
            emit_one(&res, out_path);
            return 0;
        }
    }
    fprintf(stderr, "unknown case: %s\n", name);
    return 4;
}

static int cmd_replay(const char *name, const char *out_path) {
    ScenarioSpec specs[6];
    if (load_all_cases(specs) != 0) return 1;
    for (int i = 0; i < 6; i++) {
        if (strcmp(specs[i].name, name) == 0) {
            ScenarioOutcome res;
            if (run_u(&specs[i], "replay", &res) != 0) return 5;
            emit_one(&res, out_path);
            return 0;
        }
    }
    fprintf(stderr, "unknown case: %s\n", name);
    return 6;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: sim_run --matrix --out PATH | --one NAME --out PATH | --replay NAME --out PATH\n");
        return 1;
    }
    const char *mode = argv[1];
    const char *name = NULL;
    const char *out_path = NULL;
    for (int k = 2; k < argc; k++) {
        if (strcmp(argv[k], "--out") == 0 && k + 1 < argc) {
            out_path = argv[++k];
        } else if (argv[k][0] != '-') {
            name = argv[k];
        }
    }
    if (strcmp(mode, "--matrix") == 0) {
        return cmd_matrix(out_path ? out_path : "/app/output/conservation_audit.json");
    } else if (strcmp(mode, "--one") == 0 && name) {
        return cmd_one(name, out_path ? out_path : "/app/output/one.json");
    } else if (strcmp(mode, "--replay") == 0 && name) {
        return cmd_replay(name, out_path ? out_path : "/app/output/replay.json");
    }
    fprintf(stderr, "unknown mode\n");
    return 1;
}
