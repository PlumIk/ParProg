#pragma once
#include <mpi.h>
#include <iostream>
#include <functional>
#include <array>
#include <vector>
#include <limits>
#include <sstream>
#include <fstream>
#include "ThreadPool.h"
#define BORDERS_COUNT 2
#define BORDERS_SIZE 1
#define X_DIMENTION 0
#define Y_DIMENTION 1
#define Z_DIMENTION 2

enum class Operation {
	SUM,
	MAX,
	MIN
};

enum class Datatype {
	DOUBLE,
	INT
};

template<int dimention, typename T>
class Grid;

class DecompositionType
{
public:
	DecompositionType();
	DecompositionType(MPI_Comm communicator, std::initializer_list<bool> dim_params, std::initializer_list<int> dims_create_params);

	int * get_grid_sizes(int nnodes, int grid_dim);
	void init_grid_sizes(int * grid_sizes, int grid_dim);
	bool getDimParam(int index); 
	bool getDimParam(int index) const;
	int shift();
	std::pair<int,int> getStartPoint(Grid<2,double> grid);
	MPI_Comm communicator;
	int rank;
	int commsize;

private:
	std::vector<bool> dim_params; // for 3D {true, false, true}
	std::vector<int> dims_create_params; // for 2D (8x8) {0,0} или {2,0}
};

class StartLastXY {
public:
	StartLastXY(int sx, int lx, int sy, int ly);
	int StartX;
	int LastX;
	int StartY;
	int LastY;
};

template<int dimention>
class Range {
public:
	Range();
	Range(std::initializer_list<int> list);
	Range(std::initializer_list<int> startIndexesList, std::initializer_list<int> lastIndexesList);

	void for_each(Grid<2, double> * grid, std::function<void(const int[dimention])> function);
	void for_each(Grid<2, double> * grid, ThreadPool* pool, std::function<void(const int[dimention])> function);
	void for_each_reverse(Grid<2, double>* grid, std::function<void(const int[dimention])> function);
	void for_each_reverse(Grid<2, double>* grid, ThreadPool* pool, std::function<void(const int[dimention])> function);

	int getStartIndex(int coordinate);
	int getLastIndex(int coordinate);
private:
	std::array<int, dimention> startIndexes;
	std::array<int, dimention> lastIndexes;

	StartLastXY getStartLastXY(Grid<2, double> * grid);
	StartLastXY getStartLastXYDouble(Grid<2, double> * grid);
};

class Reduce
{
public:

	template<int dim, typename T, Operation Op>
	static T reduce( Range<dim>& rng, Grid<2, double> * grid, std::function<T(const int[dim])> f, MPI_Comm comm);

	template<int dim, typename T, Operation Op>
	static T reduce( Range<dim>& rng, Grid<2, double> * grid, std::function<T(const int[dim])> f);

	template<Operation operation> 
	class get_mpi_op
	{ 
	public: 
		static MPI_Op value;
	};

	template<Datatype datatype>
	class get_mpi_type {
	public:
		static MPI_Datatype value;
	};

	template<typename T, Operation operation>
	class initial_value
	{
	public:
		static T value;
	};

	template<typename T, Operation operation>
	class perform_op
	{
	public:
		T operator()(T value, T func_result);
		static T perform(T value, T func_resutl);
	};

};

class ParaHelper {
public:
	ParaHelper(int argc, char** argv);
	~ParaHelper();
	int getNumberOfProcceses(MPI_Comm communicator);
	int getCurrentProccesNumber(MPI_Comm communicator);
	int getNumberOfProcceses();
	int getCurrentProccesNumber();
	int getParametr(std::string paramName, int defaultValue);
	void writeVisualization(std::stringbuf * visualStream, std::string dirName);
private:
	char* getCmdOption(const std::string& option);
	char** argv;
	int argc;
};

class ParaCommunication {
public:
	static void updateAllMax(double* a, double* b);
	static void updateMax(double* a, double* b);
};

class Waiter {
public:
	Waiter(int count);
	Waiter(const Waiter &waiter);
	~Waiter();
	void wait();

	MPI_Request* getRequest(int n);

private:
	MPI_Request* requests;
	int requestCount;
};

class XYPair {
public:
	XYPair(int x, int y);
	int X;
	int Y;
};

template<int dimention, typename T>
class Grid {
public:	
	~Grid();
	Grid(int* sizes, DecompositionType decompositionType);
	Grid(std::initializer_list<int> sizes, DecompositionType decompositionType);

	Grid(int* sizes);
	Grid(std::initializer_list<int> sizes);	

	T& operator()(int i, int j);
	const T operator()(int i, int j) const;
	T& operator()(int i, int j, int k);
	const T operator()(int i, int j, int k) const;
	T& operator()(const int indexes[dimention]);
	const T operator()(const int indexes[dimention]) const;

	void print();
	std::stringstream visualPrint(int iterationNumber);

	int length();

	int getSize(int coordinateNumber);

	std::pair<int,int> startPoint;

	XYPair getShift();
	int shift();
	Waiter send_grid_bound_async();
	void send_grid_bound();
	std::array<int, dimention> globalSizes;
	T* gridArray;

	DecompositionType decomposition_type;

	//void wait_grid_bound();
private:
	std::array<int, dimention> sizes;
	MPI_Comm communicator;
	int rank;
	int commsize;
};