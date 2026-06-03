#include "../include/plan.h"
#include "../include/report.h"

#include <stdio.h>
#include <string.h>

int run_case(const Plan *plan, const char *out_dir, CaseResult *res) {
    Arena arena;
    int seq = 0;
    memset(res, 0, sizeof(*res));
    strncpy(res->name, plan->name, sizeof(res->name) - 1);
    snprintf(res->ledger_path, sizeof(res->ledger_path), "%s/%s.ledger.jsonl", out_dir, plan->name);
    arena_init(&arena);
    for (int i = 0; i < plan->op_count; i++) {
        const PlanOp *op = &plan->ops[i];
        StepRec *st = &res->steps[res->step_count++];
        st->seq = seq++;
        st->index = op->index;
        st->size = op->size;
        st->result_index = -1;
        if (op->kind == OP_ALLOC) {
            strncpy(st->op, "alloc", sizeof(st->op) - 1);
            st->result_index = arena_slot_alloc(&arena, op->size);
        } else if (op->kind == OP_FREE) {
            strncpy(st->op, "free", sizeof(st->op) - 1);
            st->result_index = arena_slot_free(&arena, op->index);
        } else if (op->kind == OP_REALLOC) {
            strncpy(st->op, "realloc", sizeof(st->op) - 1);
            st->result_index = arena_slot_realloc(&arena, op->index, op->size);
        }
        st->heap_sig = arena_heap_sig(&arena);
        st->fl_count = arena_fl_count(&arena);
        st->fl_sig = arena_fl_sig(&arena);
        st->byte_total = arena.stats.allocated;
    }
    res->heap_sig = arena_heap_sig(&arena);
    res->fl_count = arena_fl_count(&arena);
    res->fl_sig = arena_fl_sig(&arena);
    res->byte_total = arena.stats.allocated;
    res->ok = 1;
    return 0;
}
