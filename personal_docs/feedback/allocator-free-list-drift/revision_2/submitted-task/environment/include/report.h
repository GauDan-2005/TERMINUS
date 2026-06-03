#ifndef REPORT_H
#define REPORT_H

#include "arena.h"
#include "plan.h"

#include <stddef.h>

#define MAX_STEPS 128

typedef struct StepRec {
    int seq;
    char op[16];
    int index;
    size_t size;
    int result_index;
    size_t heap_sig;
    int fl_count;
    size_t fl_sig;
    size_t byte_total;
} StepRec;

typedef struct CaseResult {
    char name[32];
    int ok;
    StepRec steps[MAX_STEPS];
    int step_count;
    size_t heap_sig;
    int fl_count;
    size_t fl_sig;
    size_t byte_total;
    char ledger_path[256];
} CaseResult;

int run_case(const Plan *plan, const char *out_dir, CaseResult *res);
int emit_e(const CaseResult *res, const char *audit_path);
int emit_matrix(const CaseResult *cases, int count, const char *audit_path);

#endif
