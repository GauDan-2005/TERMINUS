#include "../include/matrix_view.h"

#include <math.h>

double norm_q(const double *a, int b) {
    double s = 0.0;
    for (int i = 0; i < b; i++) {
        s += a[i] * a[i];
    }
    return sqrt(s) + 1.0e-4;
}
