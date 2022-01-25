import other.GlobalValues as GValues


class DataExample:
    _type = GValues.INT
    _condition_type = GValues.RANGE
    _conditions = list()
    _range = list()
    _find_type = GValues.ALL_VALUES
    _find_type_condition = 1

    def set_type(self, typeper: int):
        self._type = typeper
        return self

    def get_type(self) -> int:
        return self._type

    def set_condition_type(self, condition_type: int):
        self._condition_type = condition_type
        return self

    def get_condition_type(self) -> int:
        return self._condition_type

    def set_find_type(self, find_type: int):
        self._find_type = find_type
        return self

    def get_find_type(self) -> int:
        return self._find_type

    def set_conditions(self, conditions: list):
        self._conditions = conditions
        return self

    def get_conditions(self) -> list:
        return self._conditions

    def set_range(self, rangeper: list):
        self._range = rangeper
        return self

    def get_range(self) -> list:
        return self._range

    def need_find_condition(self) -> bool:
        if self._find_type != GValues.ALL_VALUES:
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
        elif self._type == GValues.FLOAT:
            for_print += ' float'
        elif self._type == GValues.DOUBLE:
            for_print += ' double'

        for_print += ' searching by'

        if self._find_type == GValues.ALL_VALUES:
            for_print += ' all values'
        elif self._find_type == GValues.GRID_VALUES:
            for_print += ' grid search with step ' + str(self._find_type_condition)

        if self._condition_type == GValues.RANGE:
            for_print += ' in range [' + str(self._range[0]) + ', ' + str(self._range[1]) + ']'
        elif self._condition_type == GValues.COMPLEX_CONDITION:
            for_print += ' with conditions:\n'
            for one in self._conditions:
                for_print += '\t' + one + '\n'
            for_print = for_print[:len(for_print) - 1]

        print(for_print)
        return self

    def code_me(self) -> dict:
        some_dict = dict()

        some_dict.setdefault('type', self._type)
        some_dict.setdefault('condition_type', self._condition_type)
        some_dict.setdefault('range', self._range)
        some_dict.setdefault('conditions', self._conditions)
        some_dict.setdefault('find_type', self._find_type)
        some_dict.setdefault('find_type_condition', self._find_type_condition)

        return some_dict

    def encode_me(self, in_dict: dict):
        self._type = in_dict.get('type')
        self._condition_type = in_dict.get('condition_type')
        self._range = in_dict.get('range')
        self._conditions = in_dict.get('conditions')
        self._find_type = in_dict.get('find_type')
        self._find_type_condition = in_dict.get('find_type_condition')

        return self
