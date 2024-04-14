#include <assert.h>
#include <stdio.h>

#include "fsym.h"
#include "utils.h"

int main() {
    // For avx512 in the future
    // assert(Ny % 16 == 0 && Nx % 16 == 0);

    // this base pointer is used under the hood for matrix acesses
    float* fixed_base_pt = calloc(TOTAL_NMEMB, sizeof(float));
    assert(fixed_base_pt != NULL);

    constants_t config = setup_constants();
    init(fixed_base_pt, &config);

    set_matrix_value(f_0, 9.0);
    set_matrix_value(f_2, 9.0);

    write_matrix_to_file(f_2, "C_matrix_dump.txt");

    free(fixed_base_pt);
}

