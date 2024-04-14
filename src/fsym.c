#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>

#define BB_INCLUDE_IMPLEMENTATION
#include "fsym.h"
#include "utils.h"

// Declaring globals 
float *f_0, *f_1, *f_2, *f_3, *f_4, *f_5, *f_6, *f_7, *f_8;
float *f_next_0, *f_next_1, *f_next_2, *f_next_3, *f_next_4, *f_next_5, *f_next_6, *f_next_7, *f_next_8;
float *f_eq_0, *f_eq_1, *f_eq_2, *f_eq_3, *f_eq_4, *f_eq_5, *f_eq_6, *f_eq_7, *f_eq_8;
float *ux, *uy, *rho;

void initialize_matrix_pointers(float* fixed_base_pt) {
    f_0       = &fixed_base_pt[MATRIX_SIZE *  0];
    f_1       = &fixed_base_pt[MATRIX_SIZE *  1];
    f_2       = &fixed_base_pt[MATRIX_SIZE *  2];
    f_3       = &fixed_base_pt[MATRIX_SIZE *  3];
    f_4       = &fixed_base_pt[MATRIX_SIZE *  4];
    f_5       = &fixed_base_pt[MATRIX_SIZE *  5];
    f_6       = &fixed_base_pt[MATRIX_SIZE *  6];
    f_7       = &fixed_base_pt[MATRIX_SIZE *  7];
    f_8       = &fixed_base_pt[MATRIX_SIZE *  8];
    f_next_0  = &fixed_base_pt[MATRIX_SIZE *  9];
    f_next_1  = &fixed_base_pt[MATRIX_SIZE * 10];
    f_next_2  = &fixed_base_pt[MATRIX_SIZE * 11];
    f_next_3  = &fixed_base_pt[MATRIX_SIZE * 12];
    f_next_4  = &fixed_base_pt[MATRIX_SIZE * 13];
    f_next_5  = &fixed_base_pt[MATRIX_SIZE * 14];
    f_next_6  = &fixed_base_pt[MATRIX_SIZE * 15];
    f_next_7  = &fixed_base_pt[MATRIX_SIZE * 16];
    f_next_8  = &fixed_base_pt[MATRIX_SIZE * 17];
    f_eq_0    = &fixed_base_pt[MATRIX_SIZE * 18];
    f_eq_1    = &fixed_base_pt[MATRIX_SIZE * 19];
    f_eq_2    = &fixed_base_pt[MATRIX_SIZE * 20];
    f_eq_3    = &fixed_base_pt[MATRIX_SIZE * 21];
    f_eq_4    = &fixed_base_pt[MATRIX_SIZE * 22];
    f_eq_5    = &fixed_base_pt[MATRIX_SIZE * 23];
    f_eq_6    = &fixed_base_pt[MATRIX_SIZE * 24];
    f_eq_7    = &fixed_base_pt[MATRIX_SIZE * 25];
    f_eq_8    = &fixed_base_pt[MATRIX_SIZE * 26];
    ux        = &fixed_base_pt[MATRIX_SIZE * 27];
    uy        = &fixed_base_pt[MATRIX_SIZE * 28];
    rho       = &fixed_base_pt[MATRIX_SIZE * 29];
}


void init(float* fixed_base_pt, constants_t* config) {
  const float* w_a = config->w_a;
  const int d_cs4 = config->d_cs4;
  const int d_cs2 = config->d_cs2;

  initialize_matrix_pointers(fixed_base_pt);
  memset(rho, 9.0, MATRIX_SIZE);

  for (int y = 0; y < Ny; y++) {
    for (int x = 0; x < Nx; x++) {
      M(f_eq_0, y, x) = w_a[0] * R(rho, y, x) * (1                                                                                        - .5 * d_cs2 * (p2(R(ux, y, x)) + p2(R(uy, y, x))));

      M(f_eq_1, y, x) = w_a[1] * R(rho, y, x) * (1 + d_cs2 * R(ux, y, x)                  + .5 * d_cs4 * (p2( R(ux, y, x)              )) - .5 * d_cs2 * (p2(R(ux, y, x)) + p2(R(uy, y, x))));
      M(f_eq_2, y, x) = w_a[2] * R(rho, y, x) * (1 + d_cs2 * R(ux, y, x)                  + .5 * d_cs4 * (p2( R(ux, y, x)              )) - .5 * d_cs2 * (p2(R(ux, y, x)) + p2(R(uy, y, x))));
      M(f_eq_3, y, x) = w_a[3] * R(rho, y, x) * (1 - d_cs2 * R(ux, y, x)                  + .5 * d_cs4 * (p2( R(ux, y, x)              )) - .5 * d_cs2 * (p2(R(ux, y, x)) + p2(R(uy, y, x))));
      M(f_eq_4, y, x) = w_a[4] * R(rho, y, x) * (1 - d_cs2 * R(ux, y, x)                  + .5 * d_cs4 * (p2( R(ux, y, x)              )) - .5 * d_cs2 * (p2(R(ux, y, x)) + p2(R(uy, y, x))));

      M(f_eq_4, y, x) = w_a[5] * R(rho, y, x) * (1 + d_cs2 * ( R(ux, y, x) + R(uy, y, x)) + .5 * d_cs4 * (p2( R(ux, y, x) + R(uy, y, x))) - .5 * d_cs2 * (p2(R(ux, y, x)) + p2(R(uy, y, x))));
      M(f_eq_5, y, x) = w_a[6] * R(rho, y, x) * (1 + d_cs2 * (-R(ux, y, x) + R(uy, y, x)) + .5 * d_cs4 * (p2(-R(ux, y, x) + R(uy, y, x))) - .5 * d_cs2 * (p2(R(ux, y, x)) + p2(R(uy, y, x))));
      M(f_eq_6, y, x) = w_a[7] * R(rho, y, x) * (1 - d_cs2 * (-R(ux, y, x) - R(uy, y, x)) + .5 * d_cs4 * (p2(-R(ux, y, x) - R(uy, y, x))) - .5 * d_cs2 * (p2(R(ux, y, x)) + p2(R(uy, y, x))));
      M(f_eq_7, y, x) = w_a[8] * R(rho, y, x) * (1 - d_cs2 * ( R(ux, y, x) - R(uy, y, x)) + .5 * d_cs4 * (p2( R(ux, y, x) - R(uy, y, x))) - .5 * d_cs2 * (p2(R(ux, y, x)) + p2(R(uy, y, x))));
    }
  }
  memcpy(f_0, f_eq_0, MATRIX_SIZE * NB_DIRECTIONS * sizeof(float));
}


constants_t setup_constants(void) {
    float c_s = 1.0/sqrt(3);

    return (constants_t) {
        .tau   = 0.6,
        .d_tau = 1.0/0.6,
        .c_s   = c_s,
        .d_cs2 = 1.0/pow(c_s, 2),
        .d_cs4 = 1.0/pow(c_s, 4),
        .w_a = {4.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/9.0,
                1.0/36.0, 1.0/36.0, 1.0/36.0, 1.0/36.0},
    };
}
