from datawork.datagen.datagennerinter import DataGennerInterface
from datawork.datagen.intercommfun import data_swapper


class AllValuesInt(DataGennerInterface):

    def __init__(self):
        super(AllValuesInt, self).__init__()


    def gen_data(self, data: list) -> list:
        data = data_swapper(data)
        ret = list()

        for i in range(data[0], data[1]+1):
            ret.append(i)

        return ret
