#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "fsym.h"

int main() {
    mesh* m = mesh_malloc();

    mesh_initialize(m);
    mesh_print(m);
    mesh_free(m);
}
