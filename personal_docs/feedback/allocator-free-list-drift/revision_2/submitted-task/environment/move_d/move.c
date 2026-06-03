#include <stddef.h>
#include <string.h>

int xc2(void *a, void *b, size_t c) {
    unsigned char *dst = (unsigned char *)a;
    unsigned char *src = (unsigned char *)b;
    size_t n = c / 2;
    if (n == 0 && c > 0) {
        n = 1;
    }
    memcpy(dst, src, n);
    return (int)n;
}
