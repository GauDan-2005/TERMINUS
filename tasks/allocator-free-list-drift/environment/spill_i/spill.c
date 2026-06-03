#include <stddef.h>

size_t spill_bucket(size_t v) {
    size_t b = 1;
    while (b < v) {
        b <<= 1;
    }
    return b;
}
