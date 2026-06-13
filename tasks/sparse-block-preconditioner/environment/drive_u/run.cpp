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
    double xo[MAX_DIM];
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

    int nb = view.nblocks;
    int bs = view.bs;
    int dim = view.n;
    for (int i = 0; i < dim; i++) {
        xo[i] = 0.0;
    }
    for (int bi = 0; bi < nb; bi++) {
        int dst = view.reorder ? view.perm[bi] : bi;
        for (int t = 0; t < bs; t++) {
            xo[dst * bs + t] = x[bi * bs + t];
        }
    }
    for (int i = 0; i < dim; i++) {
        double acc = 0.0;
        for (int j = 0; j < dim; j++) {
            acc += view.a[i * dim + j] * xo[j];
        }
        r[i] = view.b[i] - acc;
    }
    true_res = l2_norm(r, dim);
    rep_res = norm_q(r, dim);

    strncpy(out->name, spec->name, sizeof(out->name) - 1);
    out->iterations = iters;
    out->final_residual = true_res;
    out->reported_residual = rep_res;
    out->hit_limit = hit;
    out->residual_agrees = fabs(rep_res - true_res) <= 1e-6 * (1.0 + true_res);
    out->ok = (!hit) && (true_res < 1e-8) && out->residual_agrees;
    return 0;
}
