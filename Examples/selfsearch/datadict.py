
import sys


class DataDict:

    def __init__(self):
        self._full_duct = dict()

    def add_data(self, pars: list, out_data: float):

        if self._full_duct.get(tuple(pars)) is None:
            self._full_duct[tuple(pars)] = [out_data]
        else:
            self._full_duct[tuple(pars)] += [out_data]
        return self

    def add_data_from_dict(self, data_out: dict):
        for item in data_out.items():
            for one in item[1]:
                self.add_data(item[0], one)
        return self

    def add_data_from_list(self, data_out: list):
        for one in data_out:
            self.add_data(one[0], one[1])
        return self

    def get_better(self) -> list:
        ret = [-1, -1]
        data = sys.maxsize

        for item in self._full_duct.items():
            t_value = self.get_mid_value(item[0])
            if data > t_value >= 0:
                data = t_value
                ret = [item[0],  t_value]

        return ret

    def get_mid_value(self, pars: tuple) -> float:
        if self._full_duct.get(pars) is None:
            return -1

        value = 0
        for one in self._full_duct[pars]:
            value += one

        value /= len(self._full_duct[pars])

        return value

    def get_dict(self):
        return self._full_duct

    def print(self):
        print(self._full_duct)
        return self

