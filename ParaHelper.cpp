#include "CommonsParaLib.h"

ParaHelper::ParaHelper(int argc, char** argv)
	{
		MPI_Init(&argc, &argv);
		this->argc = argc;
		this->argv = argv;
	}

int ParaHelper::getNumberOfProcceses(MPI_Comm communicator){
		int comm_size;
		MPI_Comm_size(communicator, &comm_size);
		return comm_size;
	}

int ParaHelper::getCurrentProccesNumber(MPI_Comm communicator) {
		int rank;
		MPI_Comm_rank(communicator, &rank);
		return rank;
	}
int ParaHelper::getNumberOfProcceses(){
		int comm_size;
		MPI_Comm_size(MPI_COMM_WORLD, &comm_size);
		return comm_size;
	}

int ParaHelper::getCurrentProccesNumber() {
		int rank;
		MPI_Comm_rank(MPI_COMM_WORLD, &rank);
		return rank;
	}


ParaHelper::~ParaHelper()
	{
		MPI_Finalize();
	}

char* ParaHelper::getCmdOption(const std::string& option) {
	auto begin = argv;
	auto end = argv + argc;
    char** itr = std::find(begin, end, option);
    if (itr != end && ++itr != end)
    {
        return *itr;
    }
    return nullptr;
}

int ParaHelper::getParametr(std::string paramName, int defaultValue) {
	auto paramValue = getCmdOption(paramName);
    const int parametr = paramValue != nullptr ? std::stoi((std::string)paramValue) : defaultValue;
	return parametr;
}
 
void ParaHelper::writeVisualization(std::stringbuf * visualStream, std::string dirName) {
	auto proccessNum = this->getCurrentProccesNumber(MPI_COMM_WORLD);
	std::string fileName = dirName + "/proccess" + std::to_string(proccessNum) + ".txt";
	std::ofstream outFile;
	outFile.open(fileName);
	outFile << visualStream;
	outFile.close();
}