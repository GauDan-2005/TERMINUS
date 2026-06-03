#!/bin/bash
# Terminal-Bench Canary, do not remove
set -euo pipefail

python3 <<'PY'
from pathlib import Path

tag = Path("/app/pool_a/tag.c")
text = tag.read_text()
text = text.replace("a->base + a->off + (b / 2)", "a->base + a->off + b - FTR_SIZE")
text = text.replace("a->base + a->off + (total / 2)", "a->base + a->off + total - FTR_SIZE")
tag.write_text(text)

acct = Path("/app/acct_e/acct.c")
at = acct.read_text()
at = at.replace("a->allocated += (size_t)b + 8;", "a->allocated += (size_t)b;")
acct.write_text(at)
PY

cat > /app/move_d/move.c <<'MOVE'
#include <stddef.h>
#include <string.h>

int xc2(void *a, void *b, size_t c) {
    size_t done = 0;
    unsigned char *dst = (unsigned char *)a;
    unsigned char *src = (unsigned char *)b;
    if (c == 0) {
        return 0;
    }
    while (done < c) {
        size_t chunk = c - done;
        if (chunk > 64) {
            chunk = 64;
        }
        memcpy(dst + done, src + done, chunk);
        done += chunk;
    }
    return (int)c;
}
MOVE

cat > /app/list_b/list.c <<'LIST'
#include "../include/arena.h"
#include "../pool_a/tag.h"

#include <stddef.h>
#include <string.h>

static size_t fl_ix(size_t off) {
    return off >> 3;
}

static void fl_clear(Arena *a, size_t off) {
    size_t ix = fl_ix(off);
    a->fl_link_next[ix] = FL_END;
    a->fl_link_prev[ix] = FL_END;
}

void xb1(Arena *a, Block *b) {
    size_t off = b->off;
    size_t ix = fl_ix(off);
    size_t old = a->fl_head.off;
    a->fl_link_next[ix] = old;
    a->fl_link_prev[ix] = FL_END;
    if (old != FL_END) {
        a->fl_link_prev[fl_ix(old)] = off;
    }
    a->fl_head.base = b->base;
    a->fl_head.off = off;
}

void list_remove(Arena *a, Block *b) {
    size_t off = b->off;
    size_t ix = fl_ix(off);
    size_t nxt = a->fl_link_next[ix];
    size_t prv = a->fl_link_prev[ix];
    if (nxt != FL_END) {
        a->fl_link_prev[fl_ix(nxt)] = prv;
    } else if (a->fl_head.off == off) {
        a->fl_head.off = FL_END;
    }
    if (prv != FL_END) {
        a->fl_link_next[fl_ix(prv)] = nxt;
    } else {
        a->fl_head.off = nxt;
    }
    fl_clear(a, off);
}

void list_coalesce(Arena *a, Block *b) {
    size_t off = b->off;
    size_t total = tag_read_size(b);
    size_t cur = 0;
    while (cur < off) {
        Block pb = {b->base, cur};
        size_t nxt = cur + tag_read_size(&pb);
        if (nxt == off && !z_is_flag(&pb)) {
            list_remove(a, &pb);
            off = cur;
            total = tag_read_size(&pb) + tag_read_size(b);
            b->off = off;
            xa0(b, total);
            break;
        }
        cur = nxt;
    }
    off = b->off;
    total = tag_read_size(b);
    off = b->off + total;
    if (off < a->used) {
        Block nb = {b->base, off};
        if (!z_is_flag(&nb)) {
            list_remove(a, &nb);
            total += tag_read_size(&nb);
            xa0(b, total);
        }
    }
    xb1(a, b);
}

int q8f_blk(Arena *a, Block *oldb, size_t need, size_t *merged_out) {
    size_t old_total = tag_read_size(oldb);
    size_t next_off = oldb->off + old_total;
    size_t ntotal;
    Block nb;
    if (next_off >= a->used) {
        return -1;
    }
    nb.base = oldb->base;
    nb.off = next_off;
    if (z_is_flag(&nb)) {
        return -1;
    }
    ntotal = tag_read_size(&nb);
    if (old_total + ntotal < need) {
        return -1;
    }
    list_remove(a, &nb);
    *merged_out = old_total + ntotal;
    xa0(oldb, *merged_out);
    z_set_flag(oldb, 1);
    return 0;
}
LIST

make -C /app clean
make -C /app
bash /app/scripts/run-matrix.sh
