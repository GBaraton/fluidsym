#ifndef FSYM_H
#define FSYM_H

#include <stdlib.h>
#include <stdint.h>

// these should be a multiple of 16 for future SIMD maths
#define Ny 128 // rows
#define Nx 256 // cols
#define MATRIX_SIZE Ny * Nx

// fix_base_pt should be declared in main during runtime
#define f_0(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE *  0]
#define f_1(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE *  1]
#define f_2(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE *  2]
#define f_3(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE *  3]
#define f_4(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE *  4]
#define f_5(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE *  5]
#define f_6(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE *  6]
#define f_7(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE *  7]
#define f_8(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE *  8]

#define f_next_0(y, x)  fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE *  9]
#define f_next_1(y, x)  fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 10]
#define f_next_2(y, x)  fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 11]
#define f_next_3(y, x)  fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 12]
#define f_next_4(y, x)  fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 13]
#define f_next_5(y, x)  fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 14]
#define f_next_6(y, x)  fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 15]
#define f_next_7(y, x)  fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 16]
#define f_next_8(y, x)  fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 17]

#define f_eq(d, y, x)   fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 18]

#define f_eq_0(y, x)    fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 18]
#define f_eq_1(y, x)    fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 19]
#define f_eq_2(y, x)    fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 20]
#define f_eq_3(y, x)    fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 21]
#define f_eq_4(y, x)    fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 22]
#define f_eq_5(y, x)    fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 23]
#define f_eq_6(y, x)    fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 24]
#define f_eq_7(y, x)    fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 25]
#define f_eq_8(y, x)    fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 26]

#define  ux(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 27]
#define  uy(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 28]
#define rho(y, x)       fixed_base_pt[(y) * Nx + (x) + MATRIX_SIZE * 29]

#define MATRIX_COUNT 30 
#define MATRIXES_MEMORY_NEEDED MATRIX_COUNT * MATRIX_SIZE * sizeof(float)


#endif
