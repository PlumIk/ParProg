#include "CommonsParaLib.h"

Waiter::Waiter(int count) //: //requests(count)
{
	if (count < 0)
	{
		throw std::invalid_argument("Invalid count");
	}

	this->requestCount = count;

	if (count != 0) {
		this->requests = new MPI_Request[count];
	}
	else {
		this->requests = nullptr;
	}
}

Waiter::Waiter(const Waiter& waiter)
{
	this->requestCount = waiter.requestCount;
	this->requests = waiter.requests;

	std::cout << "Copyed " << this->requestCount << std::endl;
}

MPI_Request* Waiter::getRequest(int n)
{
	/*
	if (n >= this->requests.size() || n < 0)
	{
		return nullptr;
	}*/

	return this->requests + n;

	//return this->requests.data() + n;
}

void Waiter::wait()
{
	//std::cout << this->getRequest(0) << std::endl;

	if (this->requestCount == 0) {
		MPI_Waitall(this->requestCount, this->requests, MPI_STATUSES_IGNORE);
	}

	/*
	int rank;
	int comm_size;
	MPI_Comm_rank(this->communicator, &rank);
	MPI_Comm_size(this->communicator, &comm_size);

	if (rank != 0)
	{
		MPI_Wait(&request_next[0], MPI_STATUS_IGNORE);
		MPI_Wait(&request_next[1], MPI_STATUS_IGNORE);
	}
	if (rank != comm_size - 1)
	{
		MPI_Wait(&request_prev[0], MPI_STATUS_IGNORE);
		MPI_Wait(&request_prev[1], MPI_STATUS_IGNORE);
	}*/
}

Waiter::~Waiter()
{
	if (requests != nullptr)
	{
		delete[] requests;
	}
}
