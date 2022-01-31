class DataSave:
    _keys = list()
    _values = list()
    _type = list()

    def __init__(self, compiler: str, keys: list):
        self._type.append(compiler)
        self._type += keys

    def add_to_data(self, data, time):
        find = False
        find_num = 0
        for i in range(len(self._keys)):
            if data == self._keys[i]:
                find = True
                find_num = i
                i = len(self._keys) + 1

        if find:
            self._values[find_num].append(time)
        else:
            self._keys.append(data)
            self._values.append(list().append(time))

        return self

    def count_values(self) -> dict:
        ret = dict()
        for i in range(len(self._keys)):
            value = 0
            for v in self._values[i]:
                value += v
            value = value / len(self._values[i])
            ret.update({self._keys[i]: value})
        return ret
