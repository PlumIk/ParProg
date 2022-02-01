import other.GlobalValues as GValues


class DataExample:
    _type = GValues.INT
    _range = list()
    _find_type = GValues.ALL_VALUES
    _find_type_condition = 1

    def __init__(self):
        self._find_type_condition = 1


    def set_type(self, typeper: int):
        self._type = typeper
        return self

    def get_type(self) -> int:
        return self._type

    def set_find_type(self, find_type: int):
        self._find_type = find_type
        return self

    def get_find_type(self) -> int:
        return self._find_type

    def set_range(self, rangeper: list):
        self._range = rangeper
        return self

    def get_range(self) -> list:
        return self._range

    def need_find_condition(self) -> bool:
        if self._find_type != GValues.ALL_VALUES and self._find_type != GValues.RANDOM_VALUES:
            return True
        return False

    def set_find_condition(self, condition: int):
        self._find_type_condition = condition
        return self

    def get_find_condition(self):
        return self._find_type_condition

    def print_me(self, for_print):

        if self._type == GValues.INT:
            for_print += ' int'
        for_print += ' in range [' + str(self._range[0]) + ', ' + str(self._range[1]) + ']'

        print(for_print)
        return self

    def print_type(self, for_print):
        if self._find_type == GValues.ALL_VALUES:
            for_print += ' all values'
        elif self._find_type == GValues.GRID_VALUES:
            for_print += ' grid search with step ' + str(self._find_type_condition)
        elif self._find_type == GValues.RANDOM_VALUES:
            for_print += ' random search '

        print(for_print)

    def code_me(self) -> dict:
        some_dict = dict()

        some_dict.setdefault('type', self._type)
        some_dict.setdefault('range', self._range)
        some_dict.setdefault('find_type', self._find_type)
        some_dict.setdefault('find_type_condition', self._find_type_condition)

        return some_dict

    def encode_me(self, in_dict: dict):
        self._type = in_dict.get('type')
        self._range = in_dict.get('range')
        self._find_type = in_dict.get('find_type')
        self._find_type_condition = in_dict.get('find_type_condition')

        return self
