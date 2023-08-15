#include <stdint.h>

typedef struct point_t {
    float vx;
    float vy;
    float dx; // distance au point supérieur
    float dy; // distance au point à gauche
    float pressure;
} point;

typedef struct mesh {
    int cols;
    int rows;
    point** points; // Point Matrix
} mesh;


// initializes de mesh with boudary conditions
void mesh_initialize(mesh* m);

// checks that boundary conditions are still the same
void mesh_check_boundary(mesh* m);

// Mallocs the memory required
mesh* mesh_malloc(int rows, int cols);

// Frees the mesh object properly
void mesh_free(mesh* m);

// prints 3 matrixes of velocity, dx, dy and pressure
void mesh_print(mesh* m);

