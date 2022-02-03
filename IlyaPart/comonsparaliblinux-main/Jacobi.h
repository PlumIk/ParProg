#ifndef MPI_JACOBI_JACOBI_H
#define MPI_JACOBI_JACOBI_H

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "CommonsParaLib.h"
#include "baseline_data.h"

int jacobi_method(Grid<2, double>& grid, Grid<2, double>& previous_grid);

void update_grid_cell(int index, Grid<2, double>& grid, Grid<2, double>& previous_grid, double* delta);

void update_grid_center(Grid<2, double>& grid, Grid<2, double>& previous_grid, double* delta);

void update_grid_bound(Grid<2, double>& grid, Grid<2, double>& previous_grid, double* delta);

void grid_init(Grid<2, double>& grid, Grid<2, double>& previous_grid);

double iteration_func(int i, int j, Grid<2, double>& grid);

void grid_print(Grid<2, double>& grid);

double get_observational_error(Grid<2, double>& grid);

#endif //MPI_JACOBI_JACOBI_H
