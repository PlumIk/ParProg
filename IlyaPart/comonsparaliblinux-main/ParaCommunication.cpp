#include "CommonsParaLib.h"

void ParaCommunication::updateAllMax(double * a, double * b)
{
	MPI_Allreduce(a, b, 1, MPI_DOUBLE, MPI_MAX, MPI_COMM_WORLD);
}

void ParaCommunication::updateMax(double* a, double* b)
{
	MPI_Reduce(a, b, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
};