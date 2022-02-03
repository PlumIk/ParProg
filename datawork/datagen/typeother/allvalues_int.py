from Examples.conf.dataexample import DataExample
from datawork.datagen.intercommfun import data_swapper
import other.GlobalValues as GValues


class AllValuesInt:

    def __init__(self):
        self._use_spec = 0

    def gen_data(self, data: DataExample) -> list:
        ret = list()

        if data.get_type() == GValues.INT:
            data = data_swapper(data.get_range())
            for i in range(data[0], data[1] + 1):
                ret.append(i)
        elif data.get_type() == GValues.STR:
            ret = data.get_range()

        return ret
