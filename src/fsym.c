#include "fsym.h"
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>

void init_rho(float* fixed_base_pt) {
    float* rho_base = &rho(0, 0);
    memset(rho_base, 1, MATRIX_SIZE);
}

void init(float* fixed_base_pt, float* w_a, float d_cs2, float d_cs4) {
    init_rho(fixed_base_pt);

    for (int y = 0; y < Ny; y++) {
        for (int x = 0; x < Nx; x++) {
            f_eq_0(y, x) = w_a[0] * rho(y,x) * (1                                                                           - .5 * d_cs2 * (p2(ux(y,x)) + p2(uy(y,x))));

            f_eq_1(y, x) = w_a[1] * rho(y,x) * (1 + d_cs2 * ux(y,x)               + .5 * d_cs4 * (p2( ux(y, x)           )) - .5 * d_cs2 * (p2(ux(y,x)) + p2(uy(y,x))));
            f_eq_2(y, x) = w_a[2] * rho(y,x) * (1 + d_cs2 * ux(y,x)               + .5 * d_cs4 * (p2( ux(y, x)           )) - .5 * d_cs2 * (p2(ux(y,x)) + p2(uy(y,x))));
            f_eq_3(y, x) = w_a[3] * rho(y,x) * (1 - d_cs2 * ux(y,x)               + .5 * d_cs4 * (p2( ux(y, x)           )) - .5 * d_cs2 * (p2(ux(y,x)) + p2(uy(y,x))));
            f_eq_4(y, x) = w_a[4] * rho(y,x) * (1 - d_cs2 * ux(y,x)               + .5 * d_cs4 * (p2( ux(y, x)           )) - .5 * d_cs2 * (p2(ux(y,x)) + p2(uy(y,x))));

            f_eq_4(y, x) = w_a[5] * rho(y,x) * (1 + d_cs2 * ( ux(y,x) + uy(y, x)) + .5 * d_cs4 * (p2( ux(y, x) + uy(y, x))) - .5 * d_cs2 * (p2(ux(y,x)) + p2(uy(y,x))));
            f_eq_5(y, x) = w_a[6] * rho(y,x) * (1 + d_cs2 * (-ux(y,x) + uy(y, x)) + .5 * d_cs4 * (p2(-ux(y, x) + uy(y, x))) - .5 * d_cs2 * (p2(ux(y,x)) + p2(uy(y,x))));
            f_eq_6(y, x) = w_a[7] * rho(y,x) * (1 - d_cs2 * (-ux(y,x) - uy(y, x)) + .5 * d_cs4 * (p2(-ux(y, x) - uy(y, x))) - .5 * d_cs2 * (p2(ux(y,x)) + p2(uy(y,x))));
            f_eq_7(y, x) = w_a[8] * rho(y,x) * (1 - d_cs2 * ( ux(y,x) - uy(y, x)) + .5 * d_cs4 * (p2( ux(y, x) - uy(y, x))) - .5 * d_cs2 * (p2(ux(y,x)) + p2(uy(y,x))));
        }
    }
}

constants setup_constants(void) {
    float c_s = 1.0/sqrt(3);

    return (constants) {
        .tau   = 0.6,
        .d_tau = 1.0/0.6,
        .c_s   = c_s,
        .d_cs2 = 1.0/pow(c_s, 2),
        .d_cs4 = 1.0/pow(c_s, 4),
        .w_a = {4.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/9.0,
                1.0/36.0, 1.0/36.0, 1.0/36.0, 1.0/36.0},
    };
}
