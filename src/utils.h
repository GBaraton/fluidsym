#ifndef BB_UTILS
#define BB_UTILS

#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "fsym.h"

void write_matrix_to_file(float* m_ptr, char* filename);
void set_matrix_value(float* m_ptr, float value);

#ifdef DEBUG
    float r_with_bounds_check( float* m_ptr, int y, int x);
#endif

#define ERROR_MSG(msg) printf("ERROR in %s with %s at %s:%d\n", __func__, msg, __FILE__, __LINE__);
#define PRINT_VAR_NAME(var) printf("  Variable in question : '%s' -> ", #var);

#endif


#ifdef BB_INCLUDE_IMPLEMENTATION

/*
 * The M and R macros allow to Modify and Read matrixes from their base
 * pointers + x and y offset.
 *
 * These are defined separately for us to do bounds checking in Debug mode.
 */

#ifdef DEBUG
    #define PRINT_BOUNDS_CHECK(m_ptr, y, x)                                 \
        if (y >= Ny || x >= Nx) {                                           \
            ERROR_MSG("bounds check");                                      \
            PRINT_VAR_NAME(m_ptr);                                          \
            if (y >= Ny) printf("y(%d) >= Ny(%d)\n", y, Ny);                \
            if (x >= Nx) printf("x(%d) >= Nx(%d)\n", x, Nx);                \
            exit(EXIT_FAILURE);                                             \
        };
        
    float r_with_bounds_check( float* m_ptr, int y, int x){
        PRINT_BOUNDS_CHECK(m_ptr, y, x)
        return m_ptr[(y) * Nx + (x)];
    }
    #define R(m_ptr, y, x)  r_with_bounds_check(m_ptr, y, x)
    #define M(m_ptr, y, x)                                                  \
        PRINT_BOUNDS_CHECK(m_ptr, y, x)                                     \
        m_ptr[(y) * Nx + (x)]
#else
    #define M(m_ptr, y, x)  m_ptr[(y) * Nx + (x)]
    #define R(m_ptr, y, x)  M(m_ptr, y, x)
#endif


void set_matrix_value(float* m_ptr, float value) {
    for(int y = 0; y < Ny; y++) {
        for(int x = 0; x < Nx; x++) {
            M(m_ptr, y, x) = value;            
        }
    }
}

void write_matrix_to_file(float* m_ptr, char* filename) {
    FILE* file_stream = fopen(filename, "w");

    for (int y = 0; y < Ny; y++) {
        for (int x = 0; x < Nx; x ++) {
            fprintf(file_stream, "%0.1f,", R(m_ptr, y, x));
        }
        fprintf(file_stream, "\n");
    }

    fclose(file_stream);
}
#endif
