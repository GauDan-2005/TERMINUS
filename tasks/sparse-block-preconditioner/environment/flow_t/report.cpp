#include "../include/solver_report.h"

#include <stdio.h>

static void esc(FILE *fp, const char *s) {
    fputc('"', fp);
    for (const char *p = s; *p; p++) {
        if (*p == '"' || *p == '\\') {
            fputc('\\', fp);
        }
        fputc(*p, fp);
    }
    fputc('"', fp);
}

static void write_case(FILE *fp, const SolveResult *res, int last) {
    fprintf(fp, "    {\n      \"name\": ");
    esc(fp, res->name);
    fprintf(fp, ",\n      \"ok\": %s,\n", res->ok ? "true" : "false");
    fprintf(fp, "      \"iterations\": %d,\n", res->iterations);
    fprintf(fp, "      \"final_residual\": %.17g,\n", res->final_residual);
    fprintf(fp, "      \"reported_residual\": %.17g,\n", res->reported_residual);
    fprintf(fp, "      \"residual_agrees\": %s,\n", res->residual_agrees ? "true" : "false");
    fprintf(fp, "      \"hit_limit\": %s\n    }", res->hit_limit ? "true" : "false");
    if (!last) {
        fprintf(fp, ",");
    }
    fprintf(fp, "\n");
}

int emit_t(const SolveResult *res, const char *audit_path) {
    FILE *fp = fopen(audit_path, "w");
    if (!fp) {
        return -1;
    }
    fprintf(fp, "{\n  \"cases\": [\n");
    write_case(fp, res, 1);
    fprintf(fp, "  ]\n}\n");
    fclose(fp);
    return 0;
}

int emit_matrix(const SolveResult *cases, int count, const char *audit_path) {
    FILE *fp = fopen(audit_path, "w");
    if (!fp) {
        return -1;
    }
    fprintf(fp, "{\n  \"cases\": [\n");
    for (int i = 0; i < count; i++) {
        write_case(fp, &cases[i], i + 1 == count);
    }
    fprintf(fp, "  ]\n}\n");
    fclose(fp);
    return 0;
}
