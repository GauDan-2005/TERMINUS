#include "phases.h"
#include "../include/ic_loader.h"

#include <math.h>
#include <string.h>
#include <stdio.h>

static int compute_adjacency(const SimState *st) {
    int count = 0;
    for (int i = 0; i < st->grid.n; i++) {
        int p = st->topo.parent[i];
        if (p < 0) continue;
        int c0 = st->topo.child0[p];
        int cn = st->topo.child_count[p];
        if (cn > 0 && i >= c0 && i < c0 + cn) count++;
    }
    return count;
}

static void apply_reflux(SimState *st) {
    for (int i = 0; i < st->bank.n_pending; i++) {
        int leaf = st->bank.leaf[i];
        if (leaf < 0 || leaf >= st->grid.n) continue;
        double vol = st->grid.cells[leaf].vol;
        if (vol <= 0.0) continue;
        for (int v = 0; v < NVAR; v++) {
            st->grid.cells[leaf].q[v] += st->bank.flux[i * NVAR + v] / vol;
        }
    }
}

int run_u(const ScenarioSpec *spec, const char *mode, ScenarioOutcome *out) {
    (void)mode;
    memset(out, 0, sizeof(*out));
    snprintf(out->name, sizeof(out->name), "%s", spec->name);

    SimState st;
    memset(&st, 0, sizeof(st));

    CellGrid coarse;
    if (load_init(spec->profile, spec->n_coarse, &coarse) != 0) return -1;

    double base[NVAR] = {0.0, 0.0, 0.0};
    for (int c = 0; c < spec->n_coarse; c++) {
        for (int v = 0; v < NVAR; v++) base[v] += coarse.cells[c].vol * coarse.cells[c].q[v];
    }

    st.grid = coarse;
    uint64_t fp = vault_fnv1a(spec->name, (int)strlen(spec->name), 0ull);
    fp = vault_fnv1a(&spec->profile, (int)sizeof(int), fp);
    fp = vault_fnv1a(&spec->n_coarse, (int)sizeof(int), fp);
    st.fingerprint_payload = fp;

    phase_grow(&st, spec);

    if (spec->do_restart) {
        VaultAudit aud;
        memset(&aud, 0, sizeof(aud));
        char vault[256];
        char probe[256];
        char logp[256];
        snprintf(vault, sizeof(vault), "%s/work/vault.bin", app_root());
        snprintf(probe, sizeof(probe), "%s/work/vault_probe.bin", app_root());
        snprintf(logp, sizeof(logp), "%s/output/persistence_audit.log", app_root());
        phase_persist(&st, vault, probe, logp, &aud);
    }

    out->adjacency = compute_adjacency(&st);

    apply_reflux(&st);

    phase_fold(&st, spec);

    double after[NVAR] = {0.0, 0.0, 0.0};
    double moment[NVAR] = {0.0, 0.0, 0.0};
    for (int i = 0; i < st.grid.n; i++) {
        double vol = st.grid.cells[i].vol;
        for (int v = 0; v < NVAR; v++) {
            double m = vol * st.grid.cells[i].q[v];
            after[v] += m;
            moment[v] += (double)(i + 1) * m;
        }
    }

    int expected = 0;
    if (spec->do_flux) {
        for (int c = 0; c < spec->n_coarse; c++) {
            if (spec->leaf_count[c] > 1) expected += spec->leaf_count[c];
        }
    }

    double drift = 0.0;
    for (int v = 0; v < NVAR; v++) {
        double denom = fabs(base[v]);
        if (denom < 1e-12) denom = 1e-12;
        double d = fabs(after[v] - base[v]) / denom;
        if (d > drift) drift = d;
    }

    for (int v = 0; v < NVAR; v++) {
        out->base_total[v] = base[v];
        out->after_total[v] = after[v];
        out->resumed_total[v] = moment[v];
        out->halo_q[v] = st.halo_q[v];
    }
    out->drift_ratio = drift;
    out->balanced = (st.bank.n_pending == expected) ? 1 : 0;
    out->base_match = (drift < 1e-9) ? 1 : 0;
    return 0;
}
