#include <criterion/criterion.h>
#include <criterion/internal/assert.h>
#include <assert.h>
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

#include "../src/fsym.h"

#define FLOAT_TOLERANCE 0.00001

#undef Ny   
#define Ny 16

#undef Nx
#define Nx 32

void suite_setup(void){
    assert(Ny % 16 == 0 && Nx % 16 == 0);
    cr_expect(Ny * Nx == MATRIX_SIZE);
};

void suite_teardown(void){

};

TestSuite(mysuite, .init=suite_setup, .fini=suite_teardown);

Test(mysuite, example_test) {
    int* ptr = malloc(sizeof(*ptr));
    cr_expect(ptr != NULL, "The pointer should not be NULL !");
    free(ptr);
}

#define fsym_float_expect(float_1, float_2)\
    cr_expect_float_eq((float_1), (float_2), FLOAT_TOLERANCE, \
    "expected %s = %f, not %f", #float_1, tau, config.tau)

// static int cmp_func(const float* a, const float* b) {
//     return (fabs(*a - *b) < FLOAT_TOLERANCE) ? 0 : 1;
// }

static int cmp_float_arrays(const float* arr1, const float* arr2, int length) {
    for (int i = 0; i < length; ++i) {
        if ((fabs(arr1[i] - arr2[i]) > FLOAT_TOLERANCE)) {
            return i; 
        }
    }
    return -1;
}

#define fsym_float_array_expect(float_arr_1, float_arr_2, length)           \
    int i = cmp_float_arrays(float_arr_1, float_arr_2, length);             \
    cr_expect(i == -1, "expected %s[%d] = %f, not %f",                   \
    #float_arr_1, i, float_arr_1[i], float_arr_2[i])
   

Test(mysuite, constant_tamper) {
    constants config = setup_constants();

    float c_s = 1.0/sqrt(3);
    float tau = 0.6;
    float d_tau = 1.0/tau;
    float d_cs2  = 1/pow(c_s, 2);
    float d_cs4 = 1.0/pow(c_s, 4);
    const float w_a[NB_DIRECTIONS] = {4.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/36.0, 1.0/36.0, 1.0/36.0, 1.0/36.0,};

    fsym_float_expect(config.tau, tau);
    fsym_float_expect(config.d_tau, d_tau);
    fsym_float_expect(config.c_s, c_s);
    fsym_float_expect(config.d_cs2, d_cs2);
    fsym_float_expect(config.d_cs4, d_cs4);

    fsym_float_array_expect(config.w_a, w_a, NB_DIRECTIONS);
}

