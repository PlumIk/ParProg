#include "CommonsParaLib.h"
#include <omp.h>

template<> Range<2>::Range(std::initializer_list<int> list)
{
	if (list.size() != 2)
	{
		throw std::invalid_argument("Bad size for range");
	}

	int i = 0;

	for (int index : list)
	{
		this->startIndexes[i] = 0;
		this->lastIndexes[i] = index;

		i++;
	}
}

template<> Range<2>::Range(std::initializer_list<int> startIndexesList, std::initializer_list<int> lastIndexesList)
{
	if (startIndexesList.size() != 2 || lastIndexesList.size() != 2)
	{
		throw std::invalid_argument("Bad size for range");
	}

	int i = 0;

	for (int index : startIndexesList)
	{
		this->startIndexes[i] = index;
		i++;
	}

	i = 0;

	for (int index : lastIndexesList)
	{
		this->lastIndexes[i] = index;
		i++;
	}
}

template<>
int Range<2>::getStartIndex(int coordinate)
{
	return this->startIndexes[coordinate];
}

template<>
int Range<2>::getLastIndex(int coordinate)
{
	return this->lastIndexes[coordinate];
}

template<>
StartLastXY Range<2>::getStartLastXYDouble(Grid<2, double> * grid)
{
	int last_cycl_index_x = grid->decomposition_type.getDimParam(X_DIMENTION) 
							? std::min(this->lastIndexes[X_DIMENTION], (*grid).startPoint.first + (*grid).getSize(X_DIMENTION)) - (*grid).startPoint.first
							: this->lastIndexes[X_DIMENTION];

	int last_cycl_index_y = grid->decomposition_type.getDimParam(Y_DIMENTION) 
							? std::min(this->lastIndexes[Y_DIMENTION], (*grid).startPoint.second + (*grid).getSize(Y_DIMENTION)) - (*grid).startPoint.second
							: this->lastIndexes[Y_DIMENTION];

	int start_cycl_index_x = grid->decomposition_type.getDimParam(X_DIMENTION)  
							 ? std::max(this->startIndexes[X_DIMENTION], (*grid).startPoint.first) - (*grid).startPoint.first
							 : this->startIndexes[X_DIMENTION];

	int start_cycl_index_y = grid->decomposition_type.getDimParam(Y_DIMENTION)  
							 ? std::max(this->startIndexes[Y_DIMENTION], (*grid).startPoint.second) - (*grid).startPoint.second
							 : this->startIndexes[Y_DIMENTION];

	int x_border_size = grid->decomposition_type.getDimParam(X_DIMENTION) ? 1 : 0;
	int y_border_size = grid->decomposition_type.getDimParam(Y_DIMENTION) ? 1 : 0;

	StartLastXY slxy(start_cycl_index_x + x_border_size,
	 last_cycl_index_x + x_border_size,
	 start_cycl_index_y + y_border_size,
	 last_cycl_index_y + y_border_size);
	return slxy;
}

template<>
StartLastXY Range<2>::getStartLastXY(Grid<2, double> * grid)
{
	if (grid->decomposition_type.getDimParam(X_DIMENTION) && grid->decomposition_type.getDimParam(Y_DIMENTION)) {
		return getStartLastXYDouble(grid);
	}

	int last_cycl_index_x = grid->decomposition_type.getDimParam(X_DIMENTION) 
							? std::min(this->lastIndexes[X_DIMENTION], (*grid).startPoint.first + (*grid).getSize(X_DIMENTION)) - (*grid).startPoint.first
							: this->lastIndexes[X_DIMENTION];

	int last_cycl_index_y = grid->decomposition_type.getDimParam(Y_DIMENTION) 
							? std::min(this->lastIndexes[Y_DIMENTION], (*grid).startPoint.second + (*grid).getSize(Y_DIMENTION)) - (*grid).startPoint.second
							: this->lastIndexes[Y_DIMENTION];

	int start_cycl_index_x = grid->decomposition_type.getDimParam(X_DIMENTION)  
							 ? std::max(this->startIndexes[X_DIMENTION], (*grid).startPoint.first) - (*grid).startPoint.first
							 : this->startIndexes[X_DIMENTION];

	int start_cycl_index_y = grid->decomposition_type.getDimParam(Y_DIMENTION)  
							 ? std::max(this->startIndexes[Y_DIMENTION], (*grid).startPoint.second) - (*grid).startPoint.second
							 : this->startIndexes[Y_DIMENTION];

	int x_border_size = grid->decomposition_type.getDimParam(X_DIMENTION) ? 1 : 0;
	int y_border_size = grid->decomposition_type.getDimParam(Y_DIMENTION) ? 1 : 0;

	StartLastXY slxy(start_cycl_index_x + x_border_size,
	 last_cycl_index_x + x_border_size,
	 start_cycl_index_y + y_border_size,
	 last_cycl_index_y + y_border_size);
	return slxy;
}

template<>
void Range<2>::for_each(Grid<2, double>* grid, std::function<void(const int[2])> function)
{
	int i, j;

	StartLastXY StartLast = getStartLastXY(grid);

	//std::cout << "X from " << start_cycl_index_x << " to " << last_cycl_index_x << " border " << x_border_size << std::endl;
	//std::cout << "Y from " << start_cycl_index_y << " to " << last_cycl_index_y << " border " << y_border_size << std::endl;

	//indexes = new int[2];

	for (i = StartLast.StartX;
		i < StartLast.LastX;
		i++)
	{
		for (j = StartLast.StartY; j < StartLast.LastY; j++)
		{
			int indexes[2]{ i,j };
			function(indexes);
		}
	}
}

template<>
void Range<2>::for_each(Grid<2, double>* grid, ThreadPool* pool, std::function<void(const int[2])> function)
{
	if (pool->threadsCount == 1) {
		this->for_each(grid, function);
		return;
	}

	int i, j;

	StartLastXY StartLast = getStartLastXY(grid);

	int poolSize = pool->threadsCount;
	std::vector<std::future<void>> futures;

	for (i = StartLast.StartX;
		i < StartLast.LastX;
		i++)
	{
		futures.push_back((*pool).submit([i, function, StartLast]() {	
			for (int j = StartLast.StartY; j < StartLast.LastY; j++)
			{
				int indexes[2]{ i,j };
				function(indexes);
			}
		}));
	}
	
	if (futures.size() < poolSize) {
		futures[futures.size()-1].wait();
	} else {
		for (int i=0; i<poolSize; i++) {
			futures[futures.size()-i-1].wait();
		}
	}
}

template<>
void Range<2>::for_each_reverse(Grid<2, double>* grid, std::function<void(const int[2])> function)
{
	StartLastXY StartLast = getStartLastXY(grid);

	for (int i = StartLast.StartY;
		i < StartLast.LastY;
		i++)
	{
		for (int j = StartLast.StartX; j < StartLast.LastX; j++)
		{
			int indexes[2]{ j,i };
			function(indexes);
		}
	}
}

template<>
void Range<2>::for_each_reverse(Grid<2, double>* grid, ThreadPool* pool, std::function<void(const int[2])> function)
{
	if (pool->threadsCount == 1) {
		this->for_each_reverse(grid, function);
		return;
	}

	StartLastXY StartLast = getStartLastXY(grid);

	int poolSize = pool->threadsCount;
	std::vector<std::future<void>> futures;

	for (int i = StartLast.StartY;
		i < StartLast.LastY;
		i++)
	{
		futures.push_back((*pool).submit([i, function, StartLast]() {	
			for (int j = StartLast.StartX; j < StartLast.LastX; j++)
			{
				int indexes[2]{ j,i };

				function(indexes);
			}
		}));
	}
	
	if (futures.size() < poolSize) {
		futures[futures.size()-1].wait();
	} else {
		for (int i=0; i<poolSize; i++) {
			futures[futures.size()-i-1].wait();
		}
	}
}