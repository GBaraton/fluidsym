#ifndef H_TEST_HELPER
#define H_TEST_HELPER

#include <math.h>
#undef Ny   
#define Ny 16

#undef Nx
#define Nx 32

#define FLOAT_TOLERANCE 0.00001

#define fsym_float_expect(to_test, known_good)                              \
    cr_expect_float_eq((to_test), (known_good), FLOAT_TOLERANCE,            \
    "expected %s = %f\n     got %s = %f instead",                           \
    #to_test, known_good, #to_test, to_test)


int cmp_float_arrays(const float* arr1, const float* arr2, int length) {
    for (int i = 0; i < length; ++i) {
        if ((fabs(arr1[i] - arr2[i]) > FLOAT_TOLERANCE)) {
            return i; 
        }
    }
    return -1;
}

#define fsym_float_array_expect(known_good, to_test, length)                  \
    int i = cmp_float_arrays(known_good, to_test, length);                    \
    cr_expect(i == -1, "expected %s[%d] = %f\n     got %s[%d] = %f instead",  \
    #to_test, i, known_good[i], #to_test, i, to_test[i])

#endif
