#include "../include/audit_emit.h"

#include <stdio.h>
#include <sys/stat.h>
#include <string.h>
#include <errno.h>

static void mkpath(const char *path) {
    char buf[512];
    snprintf(buf, sizeof(buf), "%s", path);
    int n = (int)strlen(buf);
    for (int i = 1; i < n; i++) {
        if (buf[i] == '/') {
            buf[i] = 0;
            mkdir(buf, 0755);
            buf[i] = '/';
        }
    }
}

static void emit_row(FILE *fp, const ScenarioOutcome *o) {
    fprintf(fp, "    {\n");
    fprintf(fp, "      \"name\": \"%s\",\n", o->name);
    fprintf(fp, "      \"base_total\": [%.17g, %.17g, %.17g],\n",
        o->base_total[0], o->base_total[1], o->base_total[2]);
    fprintf(fp, "      \"after_total\": [%.17g, %.17g, %.17g],\n",
        o->after_total[0], o->after_total[1], o->after_total[2]);
    fprintf(fp, "      \"resumed_total\": [%.17g, %.17g, %.17g],\n",
        o->resumed_total[0], o->resumed_total[1], o->resumed_total[2]);
    fprintf(fp, "      \"drift_ratio\": %.17g,\n", o->drift_ratio);
    fprintf(fp, "      \"balanced\": %s,\n", o->balanced ? "true" : "false");
    fprintf(fp, "      \"base_match\": %s,\n", o->base_match ? "true" : "false");
    fprintf(fp, "      \"adjacency\": %d,\n", o->adjacency);
    fprintf(fp, "      \"halo_q\": [%.17g, %.17g, %.17g]\n",
        o->halo_q[0], o->halo_q[1], o->halo_q[2]);
    fprintf(fp, "    }");
}

void emit_one(const ScenarioOutcome *a, const char *out_path) {
    mkpath(out_path);
    FILE *fp = fopen(out_path, "w");
    if (!fp) return;
    fprintf(fp, "{\n");
    fprintf(fp, "  \"cases\": [\n");
    emit_row(fp, a);
    fprintf(fp, "\n  ]\n");
    fprintf(fp, "}\n");
    fclose(fp);
}

void emit_matrix(const ScenarioOutcome *a, int n, const char *out_path) {
    mkpath(out_path);
    FILE *fp = fopen(out_path, "w");
    if (!fp) return;
    fprintf(fp, "{\n");
    fprintf(fp, "  \"cases\": [\n");
    for (int i = 0; i < n; i++) {
        emit_row(fp, &a[i]);
        fprintf(fp, "%s\n", (i + 1 == n) ? "" : ",");
    }
    fprintf(fp, "  ]\n");
    fprintf(fp, "}\n");
    fclose(fp);
}
