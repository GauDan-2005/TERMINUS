#include "fswalk.h"

#include <stdio.h>

int main(int argc, char **argv) {
    struct qx q = {0UL};
    if (argc != 2) {
        fprintf(stderr, "usage: fsmeasure ROOT\n");
        return 64;
    }
    return walk_e(&q, argv[1], 1UL);
}
