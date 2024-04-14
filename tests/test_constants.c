#include <criterion/criterion.h>
#include <criterion/internal/assert.h>
#include <assert.h>
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

#include "../src/fsym.h"
#include "test_helpers.h"

void suite_setup(void){
    assert(Ny % 16 == 0 && Nx % 16 == 0);
    cr_expect(Ny * Nx == MATRIX_SIZE);
};

void suite_teardown(void){ };

TestSuite(mysuite, .init=suite_setup, .fini=suite_teardown);


Test(mysuite, constant_tamper) {
    constants_t constants = setup_constants();

    float c_s = 1.0/sqrt(3);
    float tau = 0.6;
    float d_tau = 1.0/tau;
    float d_cs2  = 1/pow(c_s, 2);
    float d_cs4 = 1.0/pow(c_s, 4);
    const float w_a[NB_DIRECTIONS] = {4.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/36.0, 1.0/36.0, 1.0/36.0, 1.0/36.0,};

    fsym_float_expect(constants.tau, tau);
    fsym_float_expect(constants.d_tau, d_tau);
    fsym_float_expect(constants.c_s, c_s);
    fsym_float_expect(constants.d_cs2, d_cs2);
    fsym_float_expect(constants.d_cs4, d_cs4);

    fsym_float_array_expect(constants.w_a, w_a, NB_DIRECTIONS);
}

