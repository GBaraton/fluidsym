#ifndef FSYM_H
#define FSYM_H

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

// So files that include this header file know that these exist
extern float *f_0, *f_1, *f_2, *f_3, *f_4, *f_5, *f_6, *f_7, *f_8;
extern float *f_next_0, *f_next_1, *f_next_2, *f_next_3, *f_next_4, *f_next_5, *f_next_6, *f_next_7, *f_next_8;
extern float *f_eq_0, *f_eq_1, *f_eq_2, *f_eq_3, *f_eq_4, *f_eq_5, *f_eq_6, *f_eq_7, *f_eq_8;
extern float *ux, *uy, *rho;


// these should be a multiple of 16 for future SIMD maths
// #define Ny 128 // rows
// #define Nx 256 // cols

#define Ny 4 // rows
#define Nx 12 // cols

#define MATRIX_SIZE Ny * Nx
#define NB_DIRECTIONS 9

#define MATRIX_COUNT 30 
#define TOTAL_NMEMB MATRIX_COUNT * MATRIX_SIZE

typedef struct {
    const float tau;
    const float d_tau;
    const float c_s;
    const float d_cs2;
    const float d_cs4;
    const float w_a[NB_DIRECTIONS];
} constants_t;

// Helpers 
#define p2(val) pow(val, 2)

// Function definitions
constants_t setup_constants(void);
void init(float* fixed_base_pt, constants_t* config);

#endif
