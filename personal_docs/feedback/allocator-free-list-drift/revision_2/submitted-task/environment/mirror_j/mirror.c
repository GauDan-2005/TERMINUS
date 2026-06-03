#include <stdio.h>

void mirror_line(const char *label, int v) {
    fprintf(stderr, "[diag] %s=%d\n", label, v);
}
