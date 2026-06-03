#include "fswalk.h"

int list_q(struct qx *a, const char *b) {
    if (!a || !b) {
        return 2;
    }
    a->seen += 1;
    return 0;
}
