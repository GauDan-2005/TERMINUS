#include "../include/audit_emit.h"

#include <stdio.h>

void summarize_e(const ScenarioOutcome *a, int n, const char *out_path) {
    if (!a || !out_path) return;
    FILE *fp = fopen(out_path, "w");
    if (!fp) return;
    int ok = 0;
    for (int i = 0; i < n; i++) {
        if (a[i].balanced && a[i].base_match) ok++;
    }
    fprintf(fp, "scenarios=%d balanced_and_matched=%d\n", n, ok);
    fclose(fp);
}
