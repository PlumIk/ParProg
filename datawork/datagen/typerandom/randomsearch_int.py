from random import random

from datawork.datagen.datagennerinter import DataGennerInterface
from datawork.datagen.intercommfun import data_swapper
from random import randint


class RandomSearchInt(DataGennerInterface):
    _values = 1
    _use_spec = 0

    def add_par(self, pars: list):

        if pars is not None:
            if len(pars) > 1:
                self._values = pars[1]
                self._use_spec = pars[0]
            elif len(pars) == 1:
                self._values = pars[0]

        return self

    def special_fun(self, data: list = None):
        self._values = 1

    def gen_data(self, data: list) -> list:

        data = data_swapper(data)
        ret = list()

        if self._use_spec == 1:
            self.special_fun(data)

        if self._values > data[1] - data[0]:
            self._values = data[1] - data[0] - 1

        i = 0
        while i < self._values:
            add = randint(data[0], data[1])
            if ret.count(add) == 0:
                ret.append(add)
                i += 1

        return ret
