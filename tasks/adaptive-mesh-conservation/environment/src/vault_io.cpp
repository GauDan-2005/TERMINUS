#include "../include/vault_layout.h"

#include <stdint.h>

uint64_t vault_fnv1a(const void *data, int n_bytes, uint64_t seed) {
    const uint8_t *p = (const uint8_t *)data;
    uint64_t h = 0xcbf29ce484222325ull ^ seed;
    for (int i = 0; i < n_bytes; i++) {
        h ^= (uint64_t)p[i];
        h *= 0x100000001b3ull;
    }
    return h;
}
