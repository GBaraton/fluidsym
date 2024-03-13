#include <assert.h>
#include <stdio.h>

#include "fsym.h"

int main() {
    // For avx512 in the future
    assert(Ny % 16 == 0 && Nx % 16 == 0);

    // this base pointer is used under the hood for matrix acesses
    float* fixed_base_pt = calloc(MATRIXES_MEMORY_NEEDED, 0);
    assert(fixed_base_pt != NULL);

    constants config = setup_constants();

    for (int i = 0; i < 9; i++) {
        printf("%f bob\n", config.w_a[i]);
    }

}

