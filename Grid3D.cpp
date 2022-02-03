#include "CommonsParaLib.h"
#include <iostream>

template<> inline Grid<3, double>::Grid(std::initializer_list<int> sizes) {
	DecompositionType default_dt(MPI_COMM_WORLD, { true,false,false }, { 0,0,0 });
	this->communicator = default_dt.communicator;
	MPI_Comm_size(communicator, &this->commsize);
	MPI_Comm_rank(communicator, &this->rank);

	int i = 0;

	for (int size : sizes)
	{
		this->sizes[i] = size;

		i++;
	}

	this->sizes[X_DIMENTION] = this->sizes[X_DIMENTION] / commsize;

	this->gridArray = new double[(this->sizes[X_DIMENTION] + BORDERS_COUNT) * this->sizes[Y_DIMENTION] * this->sizes[Z_DIMENTION]];
}

template<>
int Grid<3, double>::length()
{
	return (this->sizes[X_DIMENTION] + BORDERS_COUNT) * this->sizes[Y_DIMENTION] * this->sizes[Z_DIMENTION];
}

template<>
int Grid<3, double>::getSize(int coordinateNumber)
{
	if (coordinateNumber > 3)
	{
		return 0;
	}

	return this->sizes[coordinateNumber];
}

template<>
int Grid<3, double>::shift()
{
	return rank * commsize - 1;
}

template<>
Waiter Grid<3, double>::send_grid_bound_async()
{
	int layer_size = this->sizes[Y_DIMENTION] * this->sizes[Z_DIMENTION];

	//auto request_prev = new MPI_Request[2];
	//auto request_next = new MPI_Request[2];

	int reqCount = 0;
	if (commsize > 0)
	{
		reqCount = 4;
	}

	Waiter w(reqCount);

	//Waiter * waiter = new Waiter(4);
	//auto w = *waiter;

	if (this->rank != 0)
	{
		auto value = MPI_Isend(gridArray + layer_size, layer_size, MPI_DOUBLE, this->rank - 1, 0, MPI_COMM_WORLD, w.getRequest(0));
		//std::cout << "first " << value << std::endl;
		value = MPI_Irecv(gridArray, layer_size, MPI_DOUBLE, this->rank - 1, 0, MPI_COMM_WORLD, w.getRequest(1));
		//::cout << "second " << value << " " << MPI_SUCCESS << std::endl;
	}
	if (this->rank != this->commsize - 1)
	{
		auto value = MPI_Isend(gridArray + (this->sizes[X_DIMENTION]) * layer_size, layer_size, MPI_DOUBLE, this->rank + 1, 0, MPI_COMM_WORLD,
			w.getRequest(2));
		//std::cout << "third " << value << std::endl;
		value = MPI_Irecv(gridArray + (this->sizes[X_DIMENTION] + 1) * layer_size, layer_size, MPI_DOUBLE, this->rank + 1, 0, MPI_COMM_WORLD,
			w.getRequest(3));
		//std::cout << "forth " << value << std::endl;
	}

	//std::cout << w.getRequest(0) << std::endl;

	return w;
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
double& Grid<3, double>::operator()(int i, int j, int k)
{
	return this->gridArray[i * this->sizes[Y_DIMENTION] * this->sizes[Z_DIMENTION] + j*this->sizes[Z_DIMENTION] + k];
}

template<>
const double Grid<3, double>::operator()(int i, int j, int k) const
{
	return this->gridArray[i * this->sizes[Y_DIMENTION] * this->sizes[Z_DIMENTION] + j * this->sizes[Z_DIMENTION] + k];
}

template<>
double& Grid<3, double>::operator()(const int indexes[3])
{
	return this->gridArray[indexes[0] * this->sizes[Y_DIMENTION] * this->sizes[Z_DIMENTION] + indexes[1] * this->sizes[Z_DIMENTION] + indexes[2]];
}

template<>
const double Grid<3, double>::operator()(const int indexes[3]) const
{
	return this->gridArray[indexes[0] * this->sizes[Y_DIMENTION] * this->sizes[Z_DIMENTION] + indexes[1] * this->sizes[Z_DIMENTION] + indexes[2]];
}

template<>
void Grid<3, double>::print()
{
	int indexes[3];

	for (int k = 0; k < this->sizes[Z_DIMENTION]; k++)
	{
		std::cout << "[Z]: " << k;
		for (int i = 0; i < this->sizes[X_DIMENTION]; i++) {
			for (int j = 0; j < this->sizes[Y_DIMENTION]; j++)
			{
				indexes[0] = i;
				indexes[1] = j;
				indexes[2] = k;

				double var = (*this)(indexes);
				std::cout << var << " ";
			}
			std::cout << "\n";
		}
	}
	std::cout << "\n";
}

/*
double Grid<2,double>::reduce<Reduce::DOUBLE>(Range<2> range)
{
	return 0;
}*/
