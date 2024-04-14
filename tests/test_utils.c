#include <criterion/criterion.h>
#include <criterion/internal/assert.h>
#include <assert.h>
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

#include "../src/fsym.h"
#include "../src/utils.h"

#include "test_helpers.h"

void suite_setup(void){
    assert(Ny % 16 == 0 && Nx % 16 == 0);
    cr_expect(Ny * Nx == MATRIX_SIZE);
};

void suite_teardown(void){ };

TestSuite(utils_suite, .init=suite_setup, .fini=suite_teardown);


Test(utils_suite, set_matrix_value) {
    float m_ptr_control[MATRIX_SIZE] = {
        9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,
        9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,
        9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,
        9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0
    };

    float* m_ptr = calloc(MATRIX_SIZE, sizeof(*m_ptr));
    set_matrix_value(m_ptr, 9.0);

    fsym_float_array_expect(m_ptr_control, m_ptr, MATRIX_SIZE);
    free(m_ptr);
}

