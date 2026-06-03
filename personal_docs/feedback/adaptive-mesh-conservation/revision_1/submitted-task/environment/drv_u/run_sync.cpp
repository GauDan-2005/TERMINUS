#include "phases.h"

#include <stdio.h>
#include <string.h>

static int copy_with_flip(const char *src_path, const char *dst_path) {
    FILE *in = fopen(src_path, "rb");
    if (!in) return -1;
    FILE *out = fopen(dst_path, "wb");
    if (!out) { fclose(in); return -2; }
    unsigned char buf[8192];
    size_t total = 0;
    size_t r;
    while ((r = fread(buf, 1, sizeof(buf), in)) > 0) {
        if (total == 0 && r > 8) {
            buf[8] ^= 0xFFu;
        }
        fwrite(buf, 1, r, out);
        total += r;
    }
    fclose(in);
    fclose(out);
    return 0;
}

int phase_persist(SimState *st, const char *vault_path, const char *tamper_path,
                  const char *log_path, VaultAudit *resume_aud) {
    if (emit_p(st, vault_path) != 0) return -1;

    FILE *log = fopen(log_path, "a");
    if (copy_with_flip(vault_path, tamper_path) == 0) {
        SimState probe = *st;
        VaultAudit taud;
        memset(&taud, 0, sizeof(taud));
        load_k(tamper_path, &probe, &taud);
        if (log) {
            if (taud.reason == REASON_FINGERPRINT) {
                fprintf(log, "REJECTED reason=SIGNATURE_MISMATCH path=%s\n", tamper_path);
            } else {
                fprintf(log, "ACCEPTED reason=%d path=%s\n", taud.reason, tamper_path);
            }
        }
    }

    int rc = load_k(vault_path, st, resume_aud);
    if (log) {
        if (resume_aud->reason == REASON_OK) {
            fprintf(log, "ACCEPTED reason=OK path=%s\n", vault_path);
        } else {
            fprintf(log, "REJECTED reason=%d path=%s\n", resume_aud->reason, vault_path);
        }
        fclose(log);
    }
    return rc;
}
