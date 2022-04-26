import other.GlobalValues as GValues
from Examples.conf.dataexample import DataExample
from datawork.datagen.intercommfun import data_swapper


class GridStepInt:

    def __init__(self):
        self._step = 10

    def add_par(self, pars: list):

        if pars is not None:
            if len(pars) == 1:
                self._step = pars[0]
        return self

    def gen_data(self, data: DataExample) -> list:

        ret = list()

        if data.get_type() == GValues.INT:
            data = data_swapper(data.get_range())

            i = data[0]

            while i <= data[1]:
                ret.append(i)


                i += self._step
        elif data.get_type() == GValues.STR:
            i = 0
            while i < len(data.get_range()):
                ret.append(data.get_range()[i])
                i += self._step

        return ret
