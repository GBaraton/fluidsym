#ifndef FSYM_H
#define FSYM_H

#include <stdint.h>

#define FIXED_MULTIPLIER 4
#define COLS 2 * FIXED_MULTIPLIER
#define ROWS 1 * FIXED_MULTIPLIER

typedef struct point_t {
    float vx;
    float vy;
    float dx; // distance au point supérieur
    float dy; // distance au point à gauche
    float pressure;
} point;

typedef struct mesh {
    float vx[ROWS][COLS];
    float vy[ROWS][COLS];
    float vz[ROWS][COLS];
    float dx[ROWS][COLS];
    float dy[ROWS][COLS];
    float dz[ROWS][COLS];
    float pr[ROWS][COLS];
} mesh;

// Mallocs the memory required
mesh* mesh_malloc();

// Frees the mesh object properly
void mesh_free(mesh* m);

// initializes de mesh with boudary conditions
void mesh_initialize(mesh* m);

// checks that boundary conditions are still the same
void mesh_check_boundaries(mesh* m);

// prints 3 matrixes of velocity, dx, dy and pressure
void mesh_print(mesh* m);

#endif
