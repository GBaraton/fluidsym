#include "fsym.h"
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>

mesh* mesh_malloc() {
    mesh* m = malloc(sizeof(mesh));
    assert(m != NULL);

    return m;
}

void mesh_free(mesh* m) {
    free(m);
}

void mesh_check_boundary(mesh* m) {
    for (int c = 0; c <  COLS - 1; c++) {
        float v1 = m->vx[0][c];
        float v2 = m->vy[0][c];
        float v3 = m->dx[ROWS - 1][c];
        float v4 = m->dy[ROWS - 1][c];
        if (v1 != 0 || v2 != 0 || v3 != 0 || v4 != 0) {
            printf("The boundary has bee changed !\n");
            exit(-1);
        }
    }
}

void matrix_print(float mat[ROWS][COLS]) {
    for (int r = 0; r < ROWS; r++) {
        for (int c = 0; c <  COLS; c++) {
            printf("|%1.0f|", mat[r][c]);
        }
        printf("\n");
    }
    printf("\n");
}

void mesh_print(mesh* m) {
    printf("Velocity x : \n");
    matrix_print(m->vx);

    printf("Velocity y : \n");
    matrix_print(m->vy);

    printf("? dx : \n");
    matrix_print(m->dx);

    printf("? dy : \n");
    matrix_print(m->dy);

    printf("Pressure : \n");
    matrix_print(m->pr);
}

// 2D mesh assumed
void mesh_initialize(mesh* m) {
    // Top and Low Boundary
    for (int c = 0; c <  COLS; c++) {
        m->vx[0][c] = 0;
        m->vy[0][c] = 0;
        m->dx[0][c] = 1;
        m->dy[0][c] = 1;

        m->vx[ROWS - 1][c] = 0;
        m->vy[ROWS - 1][c] = 0;
        m->dx[ROWS - 1][c] = 1;
        m->dy[ROWS - 1][c] = 1;
    }

    // Left input (excludes top and low boundaries)
    for (int r = 1; r < ROWS - 1; r++) {
        m->vx[r][0] = 9;
        m->vy[r][0] = 0;
        m->dx[r][0] = 1;
        m->dy[r][0] = 1;
    }

    // Initialisation of the rest
    for (int r = 1; r < ROWS - 1; r++) {
        for (int c = 1; c <  COLS; c++) {
            m->vx[r][c] = 0;
            m->vy[r][c] = 0;
            m->dx[r][c] = 1;
            m->dy[r][c] = 1;
        }
    }
}
