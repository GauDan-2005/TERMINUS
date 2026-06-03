#include "../include/matrix_view.h"

#include <string.h>

void map_p(const double *a, const int *b, int c, int d, double *e) {
    (void)b;
    (void)c;
    (void)d;
    memcpy(e, a, (size_t)c * sizeof(double));
}
