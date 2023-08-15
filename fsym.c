#include "fsym.h"
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>

mesh* mesh_malloc(int rows, int cols) {
    mesh* m = malloc(sizeof(mesh));
    assert(m != NULL);

    *m = (mesh) {
        .cols = cols,
        .rows = rows,
        .points = NULL,
    };

    m->points = malloc(rows * sizeof(point*));
    for (int r = 0; r < rows; r++) {
        m->points[r] = malloc(cols * sizeof(point));
        assert(m->points[r] != NULL);
    }

    return m;
}

void mesh_free(mesh* m) {
    int rows = m->rows;
    for (int r = 0; r < rows; r++) {
        free(m->points[r]);    
    }
    // free(m->points);
    // free(m);
}

void mesh_check_boundary(mesh* m) {
    for (int c = 0; c < m->cols - 1; c++) {
        float v1 = m->points[0][c].vx;
        float v2 = m->points[0][c].vy;
        float v3 = m->points[m->rows - 1][c].vx;
        float v4 = m->points[m->rows - 1][c].vy;
        if (v1 != 0 || v2 != 0 || v3 != 0 || v4 != 0) {
            printf("The boundary has bee changed !\n");
            exit(-1);
        }

    }
}

void mesh_print(mesh* m) {
    printf("Velocity of points vx and vy : \n");
    for (int r = 0; r < m->rows; r++) {
        for (int c = 0; c < m->cols; c++) {
            printf("|%.0f %.0f|", m->points[r][c].vx, m->points[r][c].vy);
        }
        printf("\n");
    }
    printf("\n");

    printf("Values of dx and dy : \n");
    for (int r = 0; r < m->rows; r++) {
        for (int c = 0; c < m->cols; c++) {
            printf("|%.0f %.0f|", m->points[r][c].dx, m->points[r][c].dy);
        }
        printf("\n");
    }
    printf("\n");

    printf("Pressure of points : \n");
    for (int r = 0; r < m->rows; r++) {
        for (int c = 0; c < m->cols; c++) {
            printf("| %.0f |", m->points[r][c].pressure);
        }
        printf("\n");
    }
}

// 2D mesh assumed
void mesh_initialize(mesh* m) {
    // Top and Low Boundary
    for (int c = 0; c < m->cols - 1; c++) {
        m->points[0][c].vx = 0;
        m->points[0][c].vy = 0;
        m->points[0][c].dx = 1;
        m->points[0][c].dy = 1;

        m->points[m->rows - 1][c].vx = 0;
        m->points[m->rows - 1][c].vy = 0;
        m->points[m->rows - 1][c].dx = 1;
        m->points[m->rows - 1][c].dy = 1;
    }

    // Left input (excludes top and low boundaries)
    for (int r = 1; r < m->rows - 1; r++) {
        m->points[r][0].vx = 25;
        m->points[r][0].vy = 0;
        m->points[r][0].dx = 1;
        m->points[r][0].dy = 1;
    }

    // Initialisation of the rest
    for (int r = 1; r < m->rows - 1; r++) {
        for (int c = 1; c < m->cols; c++) {
            m->points[r][c].vx = 0;
            m->points[r][c].vy = 0;
            m->points[r][c].dx = 1;
            m->points[r][c].dy = 1;
        }
    }
}
