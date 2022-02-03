#include "CommonsParaLib.h"
#include <iostream>

template<> Grid<2,double>::~Grid()
{
	//delete[] gridArray;
}

template<>
int Grid<2, double>::length()
{
	if (decomposition_type.getDimParam(X_DIMENTION) && decomposition_type.getDimParam(Y_DIMENTION)) {
		return (this->sizes[X_DIMENTION] + (int)decomposition_type.getDimParam(X_DIMENTION) * BORDERS_COUNT + 2) 
			* (this->sizes[Y_DIMENTION]);
	}

	return (this->sizes[X_DIMENTION] + (int)decomposition_type.getDimParam(X_DIMENTION) * BORDERS_COUNT) 
			* (this->sizes[Y_DIMENTION] + (int)decomposition_type.getDimParam(Y_DIMENTION) * BORDERS_COUNT);
}

template<> Grid<2,double>::Grid(std::initializer_list<int> sizes, DecompositionType decomposition_type) : decomposition_type(decomposition_type) {
	int i = 0;
	rank = 0;
	commsize = 1;

	for (int size : sizes)
	{
		this->sizes[i] = size;
		this->globalSizes[i] = size;

		i++;
	}

	int total_elems_count = 1;

	for (int size : sizes)
	{
		total_elems_count *= size;
	}

	int* dim_sizes = decomposition_type.get_grid_sizes(total_elems_count, 2);

	decomposition_type.init_grid_sizes(this->sizes.data(), 2);
	startPoint = decomposition_type.getStartPoint(*this);

	int gridArraySize = this->length();
	if (gridArraySize > 0) {
		this->gridArray = new double[gridArraySize];
		this->communicator = decomposition_type.communicator;
	} else {
		std::cout << "Grid array size is bad" << std::endl;
	}
	MPI_Comm_size(communicator, &commsize);
	MPI_Comm_rank(communicator, &rank);
}

template<> Grid<2,double>::Grid(std::initializer_list<int> sizes) {
	int i = 0;
	rank = 0;
	commsize = 1;
	
	for (int size : sizes)
	{
		this->sizes[i] = size;
		this->globalSizes[i] = size;

		i++;
	}
	
	DecompositionType default_dt(MPI_COMM_WORLD, { true,false }, { 0,0 });
	this->decomposition_type = default_dt;

	default_dt.init_grid_sizes(this->sizes.data(), 2);
	startPoint = default_dt.getStartPoint(*this);

	this->gridArray = new double[this->length()];
	this->communicator = default_dt.communicator;

	MPI_Comm_size(communicator, &commsize);
	MPI_Comm_rank(communicator, &rank);
}

template<>
int Grid<2, double>::getSize(int coordinateNumber)
{
	if (coordinateNumber > 2)
	{
		return 0;
	}

	return this->sizes[coordinateNumber];
}

template<>
XYPair Grid<2, double>::getShift()
{
	//return rank * commsize - 1;
    bool x_startPoint_addition = this->decomposition_type.getDimParam(X_DIMENTION); 
    bool y_startPoint_addition = this->decomposition_type.getDimParam(Y_DIMENTION);
    int x_add = x_startPoint_addition ? -1 : 0;
    int y_add = y_startPoint_addition ? -1 : 0;

	int x = x_add + this->startPoint.first;
	int y = y_add + this->startPoint.second;
	XYPair pair(x,y);
	return pair;
}

template<>
int Grid<2, double>::shift()
{
	return rank * commsize - 1;
}

template<>
Waiter Grid<2, double>::send_grid_bound_async()
{
	int layer_size = this->sizes[Y_DIMENTION];

	int reqCount = 0;
	if (commsize > 0)
	{
		reqCount = 4;
	}

	Waiter w(reqCount);

	if (this->rank != 0)
	{
		auto value = MPI_Isend(gridArray + layer_size, layer_size, MPI_DOUBLE, this->rank - 1, 0, MPI_COMM_WORLD, w.getRequest(0));
		value = MPI_Irecv(gridArray, layer_size, MPI_DOUBLE, this->rank - 1, 0, MPI_COMM_WORLD, w.getRequest(1));
	}
	if (this->rank != commsize - 1)
	{
		auto value = MPI_Isend(gridArray + (this->sizes[X_DIMENTION])*layer_size, layer_size, MPI_DOUBLE, this->rank + 1, 0, MPI_COMM_WORLD,
			w.getRequest(2));
		value =MPI_Irecv(gridArray + (this->sizes[X_DIMENTION] + 1) * layer_size, layer_size, MPI_DOUBLE, this->rank + 1, 0, MPI_COMM_WORLD,
			w.getRequest(3));
	}

	 return w;
}

template<>
void Grid<2, double>::send_grid_bound()
{
	int y_layer_size = this->sizes[Y_DIMENTION];
	int x_layer_size = this->sizes[X_DIMENTION];

	int first_layer_size = this->decomposition_type.getDimParam(X_DIMENTION) ? y_layer_size : x_layer_size;
	int last_layer_size = this->decomposition_type.getDimParam(X_DIMENTION) ? x_layer_size : y_layer_size;

	if (this->rank != 0)
	{
		MPI_Send(gridArray + first_layer_size, first_layer_size, MPI_DOUBLE, this->rank - 1, 0, MPI_COMM_WORLD);
		MPI_Recv(gridArray, first_layer_size, MPI_DOUBLE, this->rank - 1, 0, MPI_COMM_WORLD, MPI_STATUSES_IGNORE);
	}
	if (this->rank != commsize - 1)
	{
		MPI_Send(gridArray + (last_layer_size) * first_layer_size, first_layer_size, MPI_DOUBLE, this->rank + 1, 0, MPI_COMM_WORLD);
		MPI_Recv(gridArray + (last_layer_size + 1) * first_layer_size, first_layer_size, MPI_DOUBLE, this->rank + 1, 0, MPI_COMM_WORLD,
			MPI_STATUSES_IGNORE);
	}
}
/*
void Grid<2, double>::wait_grid_bound()
{
	if (this->rank != 0)
	{
		MPI_Wait(&request_next[0], MPI_STATUS_IGNORE);
		MPI_Wait(&request_next[1], MPI_STATUS_IGNORE);
	}
	if (this->rank != this->commsize - 1)
	{
		MPI_Wait(&request_prev[0], MPI_STATUS_IGNORE);
		MPI_Wait(&request_prev[1], MPI_STATUS_IGNORE);
	}
}*/



template<>
double& Grid<2, double>::operator()(int i, int j)
{
	if (this->decomposition_type.getDimParam(X_DIMENTION) && this->decomposition_type.getDimParam(Y_DIMENTION)) {
		if (j >= this->sizes[Y_DIMENTION]/2) {
			return this->gridArray[i + j*this->sizes[X_DIMENTION]];
		} else {
			return this->gridArray[i*this->sizes[Y_DIMENTION] + j];
		}
	}

	if (this->decomposition_type.getDimParam(X_DIMENTION)) {
		return this->gridArray[i*this->sizes[Y_DIMENTION] + j];
	} else {
		return this->gridArray[i + j*this->sizes[X_DIMENTION]];
	}
}

template<>
const double Grid<2, double>::operator()(int i, int j) const
{
	if (this->decomposition_type.getDimParam(X_DIMENTION) && this->decomposition_type.getDimParam(Y_DIMENTION)) {
		if (j >= this->sizes[Y_DIMENTION]/2) {
			return this->gridArray[i + j*this->sizes[X_DIMENTION]];
		} else {
			return this->gridArray[i*this->sizes[Y_DIMENTION] + j];
		}
	}

	if (this->decomposition_type.getDimParam(X_DIMENTION)) {
		return this->gridArray[i*this->sizes[Y_DIMENTION] + j];
	} else {
		return this->gridArray[i + j*this->sizes[X_DIMENTION]];
	}
}

template<>
double& Grid<2, double>::operator()(const int indexes[2])
{
	if (this->decomposition_type.getDimParam(X_DIMENTION) && this->decomposition_type.getDimParam(Y_DIMENTION)) {
		if (indexes[Y_DIMENTION] >= this->sizes[Y_DIMENTION]/2) {
			return this->gridArray[indexes[X_DIMENTION] + indexes[Y_DIMENTION]* this->sizes[X_DIMENTION]];
		} else {
			return this->gridArray[indexes[X_DIMENTION] * this->sizes[Y_DIMENTION] + indexes[Y_DIMENTION]];
		}
	}

	if (this->decomposition_type.getDimParam(X_DIMENTION)) {
		return this->gridArray[indexes[X_DIMENTION] * this->sizes[Y_DIMENTION] + indexes[Y_DIMENTION]];
	} else {
		return this->gridArray[indexes[X_DIMENTION] + indexes[Y_DIMENTION]* this->sizes[X_DIMENTION]];
	}
}

template<>
const double Grid<2, double>::operator()(const int indexes[2]) const
{
	if (this->decomposition_type.getDimParam(X_DIMENTION) && this->decomposition_type.getDimParam(Y_DIMENTION)) {
		if (indexes[Y_DIMENTION] >= this->sizes[Y_DIMENTION]/2) {
			return this->gridArray[indexes[X_DIMENTION] + indexes[Y_DIMENTION]* this->sizes[X_DIMENTION]];
		} else {
			return this->gridArray[indexes[X_DIMENTION] * this->sizes[Y_DIMENTION] + indexes[Y_DIMENTION]];
		}
	}

	if (this->decomposition_type.getDimParam(X_DIMENTION)) {
		return this->gridArray[indexes[X_DIMENTION] * this->sizes[Y_DIMENTION] + indexes[Y_DIMENTION]];
	} else {
		return this->gridArray[indexes[X_DIMENTION] + indexes[Y_DIMENTION] * this->sizes[X_DIMENTION]];
	}
}

template<>
void Grid<2, double>::print()
{
	int x_bound_size = this->decomposition_type.getDimParam(X_DIMENTION) ? BORDERS_SIZE : 0;
	int y_bound_size = this->decomposition_type.getDimParam(X_DIMENTION) ? 0 : BORDERS_SIZE;

	int indexes[2];

	for (int i = x_bound_size; i < this->sizes[0]+x_bound_size; i++) {
		for (int j = y_bound_size; j < this->sizes[1]+y_bound_size; j++)
		{
			indexes[0] = i;
			indexes[1] = j;

			double var = (*this)(indexes);
			std::cout << var << " ";
		}
		std::cout << "\n";
	}
	std::cout << "\n";
	//MPI_Barrier(MPI_COMM_WORLD);
}

template<>
std::stringstream Grid<2, double>::visualPrint(int iterationNumber) 
{
    std::stringstream result;
	int x_bound_size = this->decomposition_type.getDimParam(X_DIMENTION) ? BORDERS_SIZE : 0;
	int y_bound_size = this->decomposition_type.getDimParam(X_DIMENTION) ? 0 : BORDERS_SIZE;

	int indexes[2];

	for (int i = x_bound_size; i < this->sizes[0]+x_bound_size; i++) {
		for (int j = y_bound_size; j < this->sizes[1]+y_bound_size; j++)
		{
			indexes[0] = i;
			indexes[1] = j;

			double var = (*this)(indexes);
			result << i - x_bound_size + this->startPoint.first << "|" << j - y_bound_size + this->startPoint.second << "|" << var << "|" << this->rank << "|" << iterationNumber << "\n";
		}
	}
	return result;
}

/*
double Grid<2,double>::reduce<Reduce::DOUBLE>(Range<2> range)
{
	return 0;
}*/
