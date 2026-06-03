#include "../include/matrix_view.h"

#include <math.h>
#include <string.h>

static double l2_norm(const double *v, int n) {
    double s = 0.0;
    for (int i = 0; i < n; i++) {
        s += v[i] * v[i];
    }
    return sqrt(s);
}

void step_r(const BsrPack *a, const double *b, double *c);

int pcg_solve(const BsrPack *pack, const double *rhs, double *x, int *iters, double *final_res) {
    const int n = pack->n;
    const int max_iter = 200;
    const double tol = 1e-9;
    double r[MAX_DIM];
    double z[MAX_DIM];
    double p[MAX_DIM];
    double ap[MAX_DIM];
    double rz_old;
    double alpha;
    double beta;
    double rs;
    int k;

    for (int i = 0; i < n; i++) {
        x[i] = 0.0;
    }
    bsr_matvec(pack, x, r);
    for (int i = 0; i < n; i++) {
        r[i] = rhs[i] - r[i];
    }
    rs = l2_norm(r, n);
    if (rs < tol) {
        *iters = 0;
        *final_res = rs;
        return 0;
    }
    step_r(pack, r, z);
    memcpy(p, z, (size_t)n * sizeof(double));
    rz_old = 0.0;
    for (int i = 0; i < n; i++) {
        rz_old += r[i] * z[i];
    }
    for (k = 1; k <= max_iter; k++) {
        bsr_matvec(pack, p, ap);
        alpha = rz_old;
        double denom = 0.0;
        for (int i = 0; i < n; i++) {
            denom += p[i] * ap[i];
        }
        if (fabs(denom) < 1e-30) {
            break;
        }
        alpha /= denom;
        for (int i = 0; i < n; i++) {
            x[i] += alpha * p[i];
            r[i] -= alpha * ap[i];
        }
        rs = l2_norm(r, n);
        if (rs < tol) {
            *iters = k;
            *final_res = rs;
            return 0;
        }
        step_r(pack, r, z);
        beta = 0.0;
        for (int i = 0; i < n; i++) {
            beta += r[i] * z[i];
        }
        beta /= rz_old;
        for (int i = 0; i < n; i++) {
            p[i] = z[i] + beta * p[i];
        }
        rz_old = 0.0;
        for (int i = 0; i < n; i++) {
            rz_old += r[i] * z[i];
        }
    }
    *iters = max_iter;
    *final_res = rs;
    return 1;
}
