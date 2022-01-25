from datawork.datagen.datagennerinter import DataGennerInterface
from datawork.datagen.intercommfun import data_swapper


class GridStepInt(DataGennerInterface):
    _step = 10

    def add_par(self, pars: list):

        if pars is not None:
            if (pars[0]) != -1:
                self._step = pars[0]

        return self

    def gen_data(self, data: list) -> list:

        data = data_swapper(data)
        ret = list()

        i = data[0]
        while i <= data[1]:
            ret.append(i)
            i += self._step

        return ret
