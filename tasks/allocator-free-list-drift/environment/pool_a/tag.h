#ifndef TAG_H
#define TAG_H

#include "../include/block.h"

void xa0(Block *a, size_t b);
size_t tag_read_size(const Block *a);
int z_is_flag(const Block *a);
void z_set_flag(Block *a, int flag);
size_t tag_read_footer(const Block *a, size_t total);

#endif
