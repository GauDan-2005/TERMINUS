#include "../include/case_spec.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void trim(char *s) {
    size_t n = strlen(s);
    while (n > 0 && (s[n - 1] == '\n' || s[n - 1] == '\r' || s[n - 1] == ' ')) {
        s[--n] = '\0';
    }
}

int case_load(const char *path, CaseSpec *spec) {
    FILE *fp = fopen(path, "r");
    char line[512];
    if (!fp) {
        return -1;
    }
    memset(spec, 0, sizeof(*spec));
    for (int i = 0; i < MAX_BLOCKS; i++) {
        spec->perm[i] = i;
    }
    while (fgets(line, sizeof(line), fp)) {
        trim(line);
        if (line[0] == '#' || line[0] == '\0') {
            continue;
        }
        if (strncmp(line, "name ", 5) == 0) {
            strncpy(spec->name, line + 5, CASE_NAME_LEN - 1);
        } else if (strncmp(line, "nblocks ", 8) == 0) {
            spec->nblocks = atoi(line + 8);
        } else if (strncmp(line, "bs ", 3) == 0) {
            spec->bs = atoi(line + 3);
        } else if (strncmp(line, "reorder ", 8) == 0) {
            spec->reorder = atoi(line + 8);
        } else if (strncmp(line, "perm ", 5) == 0) {
            char *tok = strtok(line + 5, " ");
            int ix = 0;
            while (tok && ix < MAX_BLOCKS) {
                spec->perm[ix++] = atoi(tok);
                tok = strtok(NULL, " ");
            }
        } else if (strncmp(line, "block ", 6) == 0) {
            BlockEntry *be = &spec->blocks[spec->block_count++];
            char *tok = strtok(line + 6, " ");
            be->rb = atoi(tok);
            tok = strtok(NULL, " ");
            be->cb = atoi(tok);
            for (int k = 0; k < spec->bs * spec->bs; k++) {
                tok = strtok(NULL, " ");
                be->vals[k] = tok ? atof(tok) : 0.0;
            }
        } else if (strncmp(line, "rhs ", 4) == 0) {
            char *tok = strtok(line + 4, " ");
            int ix = 0;
            while (tok && ix < MAX_BLOCKS * MAX_BS) {
                spec->rhs[ix++] = atof(tok);
                tok = strtok(NULL, " ");
            }
        }
    }
    fclose(fp);
    return 0;
}
