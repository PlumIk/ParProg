#include "CommonsParaLib.h"

template<> MPI_Op Reduce::get_mpi_op<Operation::SUM>::value = MPI_SUM;
template<> MPI_Op Reduce::get_mpi_op<Operation::MIN>::value = MPI_MIN;
template<> MPI_Op Reduce::get_mpi_op<Operation::MAX>::value = MPI_MAX; 

template<> MPI_Op Reduce::get_mpi_type<Datatype::DOUBLE>::value = MPI_DOUBLE;
template<> MPI_Op Reduce::get_mpi_type<Datatype::INT>::value = MPI_INT;

template<> double Reduce::initial_value<double, Operation::SUM>::value = 0;
template<> double Reduce::initial_value<double, Operation::MIN>::value = std::numeric_limits<double>::max();
template<> double Reduce::initial_value<double, Operation::MAX>::value = std::numeric_limits<double>::min();

template<> int Reduce::initial_value<int, Operation::SUM>::value = 0;
template<> int Reduce::initial_value<int, Operation::MIN>::value = std::numeric_limits<int>::max();
template<> int Reduce::initial_value<int, Operation::MAX>::value = std::numeric_limits<int>::min();

template<>
double Reduce::perform_op<double, Operation::SUM>::operator()(double value, double func_result)
{
	return value + func_result;
}

template<>
int Reduce::perform_op<int, Operation::SUM>::operator()(int value, int func_result)
{
	return value + func_result;
}

template<>
double Reduce::perform_op<double, Operation::MAX>::operator()(double value, double func_result)
{
	double result = std::max(value, func_result);
	return result;
}

template<>
int Reduce::perform_op<int, Operation::MAX>::operator()(int value, int func_result)
{
	int result = std::max(value, func_result);
	return result;
}

template<>
double Reduce::perform_op<double, Operation::MIN>::operator()(double value, double func_result)
{
	double result = std::min(value, func_result);
	return result;
}

template<>
int Reduce::perform_op<int, Operation::MIN>::operator()(int value, int func_result)
{
	int result = std::min(value, func_result);
	return result;
}

template<>
double Reduce::perform_op<double, Operation::SUM>::perform(double value, double func_result)
{
	return value + func_result;
}

template<>
double Reduce::perform_op<double, Operation::MAX>::perform(double value, double func_resutl)
{
	double result = std::max(value, func_resutl);
	return result;
}

/*
template<int dim, typename T, Operation Op>
T Reduce::reduce(Range<dim>& rng, std::function<T(const int[dim])> f, MPI_Comm comm)
{
	T v = Reduce::initial_value<T, Op>::value;
	rng.for_each(
		[&v, &f](const int idx[dim]) {
		v = Reduce::perform_op<T, Op>(v, f(idx));
	});
	T result;
	MPI_Datatype mpi_type = Reduce::get_mpi_type<T>::value;
	MPI_Op mpi_op = Reduce::get_mpi_op<Op>::value;
	MPI_Allreduce(&v, &result, 1, mpi_type, mpi_op, comm);
	return result;
}*/

template<> 
double Reduce::reduce<2,double,Operation::SUM>(Range<2>& rng, Grid<2,double> * grid, std::function<double(const int[2])> f, MPI_Comm comm)
{
	double v = Reduce::initial_value<double, Operation::SUM>::value;
	rng.for_each(grid, 
		[&v, &f](const int idx[2]) {
		auto function = f;
		v = Reduce::perform_op<double, Operation::SUM>::perform(v,f(idx));
	});
	double result;
	MPI_Datatype mpi_type = Reduce::get_mpi_type<Datatype::DOUBLE>::value;
	MPI_Op mpi_op = Reduce::get_mpi_op<Operation::SUM>::value;
	MPI_Allreduce(&v, &result, 1, mpi_type, mpi_op, comm);
	return result;
}

template<>
double Reduce::reduce<2, double, Operation::MAX>(Range<2>& rng, Grid<2, double>* grid, std::function<double(const int[2])> f, MPI_Comm comm)
{
	double v = Reduce::initial_value<double, Operation::MAX>::value;
	rng.for_each(grid,
		[&v, &f](const int idx[2]) {
		auto function = f;
		v = Reduce::perform_op<double, Operation::MAX>::perform(v, f(idx));
	});
	double result;
	MPI_Datatype mpi_type = Reduce::get_mpi_type<Datatype::DOUBLE>::value;
	MPI_Op mpi_op = Reduce::get_mpi_op<Operation::MAX>::value;
	MPI_Allreduce(&v, &result, 1, mpi_type, mpi_op, comm);
	return result;
}

template<> 
double Reduce::reduce<2,double,Operation::SUM>(Range<2>& rng, Grid<2,double> * grid, std::function<double(const int[2])> f)
{
	double v = Reduce::initial_value<double, Operation::SUM>::value;
	rng.for_each(grid, 
		[&v, &f](const int idx[2]) {
		auto function = f;
		v = Reduce::perform_op<double, Operation::SUM>::perform(v,f(idx));
	});
	double result;
	MPI_Datatype mpi_type = Reduce::get_mpi_type<Datatype::DOUBLE>::value;
	MPI_Op mpi_op = Reduce::get_mpi_op<Operation::SUM>::value;
	MPI_Allreduce(&v, &result, 1, mpi_type, mpi_op, MPI_COMM_WORLD);
	return result;
}

template<>
double Reduce::reduce<2, double, Operation::MAX>(Range<2>& rng, Grid<2, double>* grid, std::function<double(const int[2])> f)
{
	double v = Reduce::initial_value<double, Operation::MAX>::value;
	rng.for_each(grid,
		[&v, &f](const int idx[2]) {
		auto function = f;
		v = Reduce::perform_op<double, Operation::MAX>::perform(v, f(idx));
	});
	double result;
	MPI_Datatype mpi_type = Reduce::get_mpi_type<Datatype::DOUBLE>::value;
	MPI_Op mpi_op = Reduce::get_mpi_op<Operation::MAX>::value;
	MPI_Allreduce(&v, &result, 1, mpi_type, mpi_op, MPI_COMM_WORLD);
	return result;
}