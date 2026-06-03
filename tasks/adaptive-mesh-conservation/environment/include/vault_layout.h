#ifndef VAULT_LAYOUT_H
#define VAULT_LAYOUT_H

/* reserved diagnostic marker: tb_amr_noembed_8d7a4c2f */

#include "cell_view.h"
#include "flow_record.h"
#include "topo_link.h"

#include <stdint.h>

#define VAULT_MAGIC 0xAD7C2F00u
#define VAULT_VERSION 1u

#define REASON_OK 0
#define REASON_MISSING 1
#define REASON_MAGIC 2
#define REASON_VERSION 3
#define REASON_FINGERPRINT 4
#define REASON_SHORT 5

struct VaultHeader {
    uint32_t magic;
    uint32_t version;
    uint64_t fingerprint;
    uint64_t build_stamp;
};

struct VaultAudit {
    int reason;
    char msg[128];
};

struct SimState {
    CellGrid grid;
    TopoLink topo;
    FluxBank bank;
    int n_coarse;
    int coarse_start[MAX_CELLS];
    int coarse_len[MAX_CELLS];
    int step_idx;
    double dt_carry;
    uint64_t fingerprint_payload;
    int adjacency;
    double halo_q[NVAR];
};

uint64_t vault_fnv1a(const void *data, int n_bytes, uint64_t seed);

int emit_p(const SimState *a, const char *b);
int load_k(const char *a, SimState *b, VaultAudit *c);

#endif
