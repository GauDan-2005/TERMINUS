#pragma once

#include "case_spec.h"

#define MAX_DIM 32

typedef struct {
    int n;
    int bs;
    int nblocks;
    int reorder;
    int perm[MAX_BLOCKS];
    double a[MAX_DIM * MAX_DIM];
    double b[MAX_DIM];
} MatrixView;

typedef struct {
    int n;
    int bs;
    int nblocks;
    int reorder;
    int perm[MAX_BLOCKS];
    int row_ptr[MAX_BLOCKS + 1];
    int col_idx[MAX_NNZ_BLOCKS];
    double data[MAX_NNZ_BLOCKS * MAX_BS * MAX_BS];
    double diag_inv[MAX_DIM];
} BsrPack;

void matrix_from_case(const CaseSpec *spec, MatrixView *view);
void bsr_matvec(const BsrPack *pack, const double *x, double *y);
