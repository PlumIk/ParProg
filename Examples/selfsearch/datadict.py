import sys


class DataDict:
    _full_duct = dict()

    def add_data(self, compiler: str, keys: list, in_data: iter, out_data: float):

        if self._full_duct.get(compiler) is None:
            self._full_duct[compiler] = dict()
            self._full_duct[compiler][tuple(keys)] = dict()
            self._full_duct[compiler][tuple(keys)][tuple(in_data)] = [out_data]
        elif self._full_duct[compiler].get(tuple(keys)) is None:
            self._full_duct[compiler][tuple(keys)] = dict()
            self._full_duct[compiler][tuple(keys)][tuple(in_data)] = [out_data]
        elif self._full_duct[compiler][tuple(keys)].get(tuple(in_data)) is None:
            self._full_duct[compiler][tuple(keys)][tuple(in_data)] = [out_data]
        else:
            self._full_duct[compiler][tuple(keys)][tuple(in_data)] += [out_data]
        return self

    def add_data_from_dict(self, data_out: dict):
        for item in data_out.items():
            for one_data_set in item[1]:
                self.add_data(item[0], one_data_set[0], one_data_set[1], one_data_set[2])

        return self

    def get_better(self) -> list:
        ret = [-1, -1, -1, -1]
        data = sys.maxsize

        for item1 in self._full_duct.items():
            for item2 in item1[1].items():
                for item3 in item2[1].items():
                    t_value = self.get_mid_value(item1[0], item2[0], item3[0])
                    if data > t_value >= 0:
                        data = t_value
                        ret = [item1[0], item2[0], item3[0], t_value]

        return ret

    def get_mid_value(self, compiler: str, keys: tuple, data: tuple) -> float:

        if self._full_duct.get(compiler) is None:
            return -1
        elif self._full_duct[compiler].get(keys) is None:
            return -1
        elif self._full_duct[compiler][keys].get(data) is None:
            return -1

        value = 0
        for one in self._full_duct[compiler][keys][data]:
            value += one

        value /= len(self._full_duct[compiler][keys][data])

        return value

    def print(self):
        print(self._full_duct)
