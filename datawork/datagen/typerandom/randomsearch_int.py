from random import random

from Examples.conf.dataexample import DataExample
from datawork.datagen.intercommfun import data_swapper
from random import randint
import other.GlobalValues as GValues


class RandomSearchInt:

    def __init__(self):
        self._use_spec = 0
        self._values = 1

    def add_par(self, pars: list):
        if pars is not None:
            if len(pars) == 1:
                self._values = pars[0]
        return self

    def gen_data(self, data: DataExample) -> list:
        ret = list()

        if data.get_type() == GValues.INT:
            data = data_swapper(data.get_range())

            if self._values > data[1] - data[0]:
                self._values = data[1] - data[0] - 1
                if self._values < 1:
                    self._values = 1
            i = 0
            while i < self._values:
                add = randint(data[0], data[1])
                if ret.count(add) == 0:
                    ret.append(add)
                    i += 1

        elif data.get_type() == GValues.STR:
            if self._values > len(data.get_range()):
                self._values = len(data.get_range()) - 1
                if self._values < 1:
                    self._values = 1
            i = 0
            while i < self._values:
                add = randint(0, len(data.get_range()) - 1)
                if ret.count(data.get_range()[add]) == 0:
                    ret.append(data.get_range()[add])
                    i += 1

        elif data.get_type() == GValues.DOUBLE:
            data = data_swapper(data.get_range())

            if self._values > data[1] - data[0]:
                self._values = data[1] - data[0] - 1
                if self._values < 1:
                    self._values = 1
            i = 0
            while i < self._values:
                add = random() * (data[1] - data[0]) + data[0]
                if ret.count(add) == 0:
                    ret.append(add)
                    i += 1

        return ret
