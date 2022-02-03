#include "CommonsParaLib.h"

template<int dimention>
Range<dimention>::Range()
{
}

template<int dimention>
Range<dimention>::Range(std::initializer_list<int> list)
{
	if (list.size() != dimention)
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

template<int dimention>
Range<dimention>::Range(std::initializer_list<int> startIndexesList, std::initializer_list<int> lastIndexesList)
{
	if (startIndexesList.size() != dimention || lastIndexesList.size() != dimention)
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