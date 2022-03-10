import other.GlobalValues as GValues


class DataExample:

    def __init__(self):
        self._type = GValues.INT
        self._range = list()
        self._find_type_condition = 1

    def set_type(self, typeper: int):
        self._type = typeper
        return self

    def get_type(self) -> int:
        return self._type

    def set_range(self, rangeper: list):
        self._range = rangeper
        return self

    def get_range(self) -> list:
        return self._range

    def print_me(self):
        if self._type == GValues.INT:
            print('Int in range ', self._range)
        elif self._type == GValues.STR:
            print('String with values ', self._range)

    def code_me(self) -> dict:
        some_dict = dict()

        some_dict.setdefault('type', self._type)
        some_dict.setdefault('range', self._range)

        return some_dict

    def encode_me(self, in_dict: dict):
        self._type = in_dict.get('type')
        self._range = in_dict.get('range')

        return self
