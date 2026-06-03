#include "../include/case_spec.h"
#include "../include/matrix_view.h"
#include "../include/solver_report.h"

#include <math.h>
#include <string.h>

void fn_n(const MatrixView *a, int reorder, BsrPack *c);
void map_p(const double *a, const int *b, int c, int d, double *e);
double norm_q(const double *a, int b);
void matrix_from_case(const CaseSpec *spec, MatrixView *view);
int pcg_solve(const BsrPack *pack, const double *rhs, double *x, int *iters, double *final_res);

static double l2_norm(const double *v, int n) {
    double s = 0.0;
    for (int i = 0; i < n; i++) {
        s += v[i] * v[i];
    }
    return sqrt(s);
}

int run_u(const CaseSpec *spec, const char *out_dir, SolveResult *out) {
    MatrixView view;
    BsrPack pack;
    double rhs[MAX_DIM];
    double x[MAX_DIM];
    double r[MAX_DIM];
    double true_res;
    double rep_res;
    int hit;
    int iters;

    (void)out_dir;
    matrix_from_case(spec, &view);
    fn_n(&view, view.reorder, &pack);
    map_p(view.b, view.perm, view.n, view.bs, rhs);
    hit = pcg_solve(&pack, rhs, x, &iters, &true_res);
    bsr_matvec(&pack, x, r);
    for (int i = 0; i < view.n; i++) {
        r[i] = rhs[i] - r[i];
    }
    true_res = l2_norm(r, view.n);
    rep_res = norm_q(r, view.n);
    strncpy(out->name, spec->name, sizeof(out->name) - 1);
    out->iterations = iters;
    out->final_residual = true_res;
    out->reported_residual = rep_res;
    out->hit_limit = hit;
    out->residual_agrees = fabs(rep_res - true_res) <= 1e-6 * (1.0 + true_res);
    out->ok = (!hit) && (true_res < 1e-8) && out->residual_agrees;
    return 0;
}
