#include "../include/matrix_view.h"

void map_p(const double *a, const int *b, int c, int d, double *e) {
    int nb = c / d;
    for (int bi = 0; bi < nb; bi++) {
        int dst = b[bi];
        for (int r = 0; r < d; r++) {
            e[dst * d + r] = a[bi * d + r];
        }
    }
}
