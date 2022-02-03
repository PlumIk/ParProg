#include "CommonsParaLib.h"

DecompositionType::DecompositionType()
{
	this->communicator = MPI_COMM_WORLD;
	this->dim_params = std::vector<bool>({ true,false });
	this->dims_create_params = std::vector<int>({ 0,0 });
	/*
	for (bool param : dim_params)
	{
		this->dim_params.push_back(param);
	}

	for (int param : dims_create_params)
	{
		this->dims_create_params.push_back(param);
	}*/
	MPI_Comm_size(communicator, &commsize);
	MPI_Comm_rank(communicator, &rank);
}

DecompositionType::DecompositionType(MPI_Comm communicator, 
									std::initializer_list<bool> dim_params,
									std::initializer_list<int> dims_create_params)
	: dim_params(dim_params), dims_create_params(dims_create_params)
{
	this->communicator = communicator;

	MPI_Comm_size(communicator, &commsize);
	MPI_Comm_rank(communicator, &rank);
}

bool DecompositionType::getDimParam(int index) {
	return this->dim_params[index];
}

bool DecompositionType::getDimParam(int index) const {
	return this->dim_params[index];
}

void DecompositionType::init_grid_sizes(int* sizes, int grid_dim)
{
	int i = 0;
	int commsize;
	bool allParamsTrue = true;

	MPI_Comm_size(communicator, &commsize);

	for (bool param : dim_params)
	{
		if (param)
		{
			sizes[i] /= commsize;
		}

		if (!param) { allParamsTrue = false; }

		i++;
	}

	if (allParamsTrue) { sizes[i-1] *= commsize; }
}

int DecompositionType::shift()
{
	return rank * commsize - 1;
}

std::pair<int, int> DecompositionType::getStartPoint(Grid<2, double> grid)
{
	int x_size = this->dim_params[X_DIMENTION] ? (grid.globalSizes[0] / commsize) * rank : 0;
	int y_size = this->dim_params[Y_DIMENTION] ? (grid.globalSizes[1] / commsize) * rank : 0;

	std::pair<int,int> pair(x_size, y_size);
	//std::pair<int,int> pair(0,0);
	return pair;
}

int * DecompositionType::get_grid_sizes(int nnodes, int grid_dim)
{
	int * sizes = new int[grid_dim];

	for (int i = 0; i < grid_dim; i++)
	{
		sizes[i] = 0;
	}
	
	int i = 0;

	for (int dim_param : dims_create_params)
	{
		sizes[i] = dim_param;
		i++;
	}

	MPI_Dims_create(nnodes, grid_dim, sizes);

	return sizes;
}
