#pragma once

#define MAX_CASES 8

typedef struct {
    char name[32];
    int ok;
    int iterations;
    double final_residual;
    double reported_residual;
    int residual_agrees;
    int hit_limit;
} SolveResult;

int emit_t(const SolveResult *res, const char *audit_path);
int emit_matrix(const SolveResult *cases, int count, const char *audit_path);
