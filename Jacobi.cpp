#include "Jacobi.h"
#include <iostream>

void grid_print(Grid<2, double>& grid)
{
    int indexes[2];

    for (int i = 1; i < grid.getSize(X_DIMENTION)+1; i++) {
        for (int j = 0; j < grid.getSize(Y_DIMENTION); j++)
        {
            indexes[0] = i;
            indexes[1] = j;

            double var = grid(indexes);
            std::cout << var;
        }
        std::cout << "\n";
    }
    std::cout << "\n";
}

bool is_boundary_cell(int index, int bound)
{
    return index == 0 || index == bound - 1;
}


void grid_init(Grid<2, double>& grid, Grid<2, double>& previous_grid)
{
    /*
    Range<2> allRange({ 0,0 }, { grid.getSize(X_DIMENTION) + 1 ,  grid.getSize(Y_DIMENTION) + 1 });
    allRange.for_each([&grid, &previous_grid](const int indexes[2]) -> void {

        grid(indexes) = 0;
        previous_grid(indexes) = 0;
    });
    
    Range<2> r({ 1,0 }, { grid.getSize(X_DIMENTION) + 1 , grid.getSize(Y_DIMENTION) });

    r.for_each([&grid, &previous_grid](const int indexes[2]) -> void {

        grid(indexes) = PHI0;
        previous_grid(indexes) = PHI0;


        int actual_i = indexes[0] + grid.shift();


        if (is_boundary_cell(actual_i, NX) || is_boundary_cell(indexes[1], NY))
        {
            grid(indexes) = phi(actual_i, indexes[1]);
            previous_grid(indexes) = phi(actual_i, indexes[1]);
        }
    });*/

    for (int i = 0; i < grid.getSize(X_DIMENTION) + 1; i++)
    {
        for (int j = 0; j < grid.getSize(Y_DIMENTION) + 1; j++)
        {
            grid(i, j) = 0;
            previous_grid(i, j) = 0;
        }

    }
    
    for (int i = 1; i < grid.getSize(X_DIMENTION)+1; i++)
    {
        for (int j = 0; j < grid.getSize(Y_DIMENTION); j++)
        {
            grid(i, j) = PHI0;
            previous_grid(i, j) = PHI0;


            int actual_i = i + grid.shift();


            if (is_boundary_cell(actual_i, NX) || is_boundary_cell(j, NY))
            {
                grid(i, j) = phi(actual_i, j);
                previous_grid(i, j) = phi(actual_i, j);
            }
        }

    }
}

void update_grid_center(Grid<2, double>& grid, Grid<2, double>& previous_grid, double *delta)
{
    int center = (grid.getSize(X_DIMENTION) + 1) / 2;
    
    update_grid_cell(center, grid, previous_grid, delta);

    for (int j = 1; j < center; j++)
    {
        update_grid_cell(center - j, grid, previous_grid, delta);
        update_grid_cell(center + j, grid, previous_grid, delta);
    }

    if (grid.getSize(X_DIMENTION) % 2 == 0)
    {
        update_grid_cell(grid.getSize(X_DIMENTION), grid, previous_grid, delta);
    }
}

void update_grid_bound(Grid<2, double>& grid, Grid<2, double>& previous_grid, double * delta)
{
    update_grid_cell(1, grid, previous_grid, delta);
    update_grid_cell(grid.getSize(X_DIMENTION), grid, previous_grid, delta);
}

double iteration_func(int i, int j, Grid<2, double>& grid)
{
    return ((1.0 / (2.0 / (hx * hx) + 2.0 / (hy * hy) + A)) *
            ((grid(i + 1, j) + grid(i - 1, j)) / (hx * hx) +
             (grid(i, j + 1) + grid(i, j - 1)) / (hy * hy) -
             ro(i + grid.shift(), j)));
}

void update_grid_cell(int index, Grid<2, double>& grid, Grid<2, double>& previous_grid, double *delta)
{
    int actual_index = index + grid.shift(); 

    if (!is_boundary_cell(actual_index, NX))
    {
        for (int j = 1; j < grid.getSize(Y_DIMENTION) - 1; j++)
        {
            grid(index, j) = iteration_func(index, j, previous_grid);

            double cur_delta = fabs(grid(index, j) - previous_grid(index, j));

            if (*delta < cur_delta)
            {
                *delta = cur_delta;
            }
        }
    }

    for (int j = 1; j < grid.getSize(Y_DIMENTION) - 1; j++)
    {
        previous_grid(index, j) = grid(index, j);
    }
}

int jacobi_method(Grid<2, double>& grid, Grid<2, double>& previous_grid)
{
    double t_start = MPI_Wtime();
    grid_init(grid, previous_grid);
    double t_end = MPI_Wtime();

    //printf("Init time: %f\n", t_end - t_start);

    //MPI_Barrier(MPI_COMM_WORLD);

    int iteration_count = 0;
    double max_delta = 0;

    do
    {
        double delta = 0;

        t_start = MPI_Wtime();
        Waiter w = previous_grid.send_grid_bound_async();
        t_end = MPI_Wtime();

        //if (iteration_count == 0 && grid.rank == 0)
          //  printf("Send time: %f\n", t_end - t_start);
       // MPI_Barrier(MPI_COMM_WORLD);

        t_start = MPI_Wtime();
        update_grid_center(grid, previous_grid, &delta);
        t_end = MPI_Wtime();

        //if (iteration_count == 0 && grid.rank == 0)
          //  printf("Update centre time: %f\n", t_end - t_start);
        //MPI_Barrier(MPI_COMM_WORLD);

        t_start = MPI_Wtime();
        //previous_grid.wait_grid_bound();
        w.wait();
        t_end = MPI_Wtime();

        //if (iteration_count == 0 && grid.rank == 0)
         //   printf("Recieve time: %f\n", t_end - t_start);
        //MPI_Barrier(MPI_COMM_WORLD);

        t_start = MPI_Wtime();
        update_grid_bound(grid, previous_grid, &delta);
        t_end = MPI_Wtime();
        //MPI_Barrier(MPI_COMM_WORLD);

        //if (iteration_count == 0)
          //  printf("Update bound time: %f\n", t_end - t_start);
       // MPI_Barrier(MPI_COMM_WORLD);

        auto w2 = previous_grid.send_grid_bound_async();
        update_grid_center(grid, previous_grid, &delta);
        //previous_grid.wait_grid_bound();
        w2.wait();
        update_grid_bound(grid, previous_grid, &delta);
        //MPI_Barrier(MPI_COMM_WORLD);
        

        ParaCommunication::updateAllMax(&delta, &max_delta);
        iteration_count++;

    } while (max_delta >= E);



    return iteration_count;
}

double get_observational_error(Grid<2, double>& grid)
{
    double pr_observational_error = 0;

    for (int i = 1; i < grid.getSize(0) + 1; i++)
    {
        for (int j = 0; j < NY; j++)
        {
            int actual_i = i + grid.shift();
            double temp = fabs(grid(i, j) - phi(actual_i, j));
            if (temp > pr_observational_error)
            {
                pr_observational_error = temp;
            }
        }
    }

    double observational_error = 0;
    ParaCommunication::updateMax(&pr_observational_error, &observational_error);
    return observational_error;
}
