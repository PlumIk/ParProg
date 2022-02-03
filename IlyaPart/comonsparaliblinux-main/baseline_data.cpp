#include "baseline_data.h"
#include <iostream>
#include <mpi.h>


double phi(double i, double j)
{
    double x = X0 + (i) * hx;
    double y = X0 + (j) * hy; 
    return x * x + y * y;
}

double phi(double i, double j, int nx, int ny)
{
    double HX = ((double)(X1-X0))/(nx-1);
    double HY = ((double)(Y1-Y0))/(ny-1);
    double x = X0 + (i) * HX;
    double y = X0 + (j) * HY; 
    return x * x + y * y;
}
/*
double phi(double i, double j)
{
    return i*i + j*j;
}*/

double ro(double i, double j)
{
    return 6 - A * phi(i, j);
}

double ro(double i, double j, int x, int y)
{
    return 6 - A * phi(i, j, x, y);
}
