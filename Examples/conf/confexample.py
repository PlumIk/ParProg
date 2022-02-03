from Examples.conf.dataexample import DataExample
from Examples.launching.datalauchexample import DataLaunchExample
from other import GlobalValues as GValues


class ConfExample:
    _program_path = ' '
    _save_path = ' '
    _trials = 1
    _at_same_time = 1
    _data_set_len = 0
    _searching_word = 'time'
    _data_set = list()
    _valid = 0
    _find_type = GValues.ALL_VALUES
    _find_type_condition = 1

    def __init__(self):
        self._valid = 0

    def set_valid(self):
        self._valid = 1
        return self

    def set_invalid(self):
        self._valid = 2
        return self

    def get_valid(self) -> int:
        return self._valid

    def get_program_path(self) -> str:
        return self._program_path

    def set_program_path(self, program_path: str):
        self._program_path = program_path
        return self

    def get_save_path(self) -> str:
        return self._save_path

    def set_save_path(self, save_path: str):
        self._save_path = save_path
        return self

    def get_searching_word(self) -> str:
        return self._searching_word

    def set_searching_word(self, searching_word: str):
        self._searching_word = searching_word
        return self

    def get_find_type(self) -> int:
        return self._find_type

    def set_find_type(self, find_type: int):
        self._find_type = find_type
        return self

    def need_find_condition(self) -> bool:
        if self._find_type == GValues.GRID_VALUES:
            return True
        return False

    def get_find_condition(self) -> int:
        return self._find_type_condition

    def set_find_condition(self, find_condition: int):
        self._find_type_condition = find_condition
        return self

    def get_trails(self) -> int:
        return self._trials

    def set_trails(self, trails: int):
        self._trials = trails
        return self

    def get_at_same_time(self) -> int:
        return self._at_same_time

    def set_at_same_time(self, at_same_time: int):
        self._at_same_time = at_same_time
        return self

    def get_data_set_len(self) -> int:
        return self._data_set_len

    def set_data_set_len(self, data_set_len: int):
        self._data_set_len = data_set_len
        return self

    def get_data_set(self) -> list:
        return self._data_set

    def set_data_set(self, data_set: list):
        self._data_set = data_set
        return self

    def code_me(self) -> dict:
        some_dict = dict()
        some_dict.setdefault('program_path', self._program_path)
        some_dict.setdefault('save_path', self._save_path)
        some_dict.setdefault('find_type', self._find_type)
        some_dict.setdefault('find_condition', self._find_type_condition)
        some_dict.setdefault('searching_word', self._searching_word)
        some_dict.setdefault('trails', self._trials)
        some_dict.setdefault('at_same_time', self._at_same_time)
        some_dict.setdefault('data_set_len', self._data_set_len)

        a_some_dict = list()
        for one in self._data_set:
            a_some_dict.append(one.code_me())

        some_dict.setdefault('data_set', a_some_dict)
        return some_dict

    def encode_me(self, in_dict: dict):
        self._program_path = in_dict.get('program_path')
        self._save_path = in_dict.get('save_path')
        self._trials = in_dict.get('trails')
        self._find_type = in_dict.get('find_type')
        self._searching_word = in_dict.get('searching_word')
        self._find_type_condition = in_dict.get('find_condition')
        self._at_same_time = in_dict.get('at_same_time')
        self._data_set_len = in_dict.get('data_set_len')

        in_dict = in_dict.get('data_set')
        self._data_set = list()
        for one in in_dict:
            self._data_set.append(DataExample().encode_me(one))

        return self

    def print_me(self):
        print('Program path ', self._program_path)
        print('Save_path ', self._save_path)
        print('Search word ', self._searching_word)
        print('Trails ', self._trials)

        if self._find_type == GValues.ALL_VALUES:
            print('Searching by all values')
        elif self._find_type == GValues.GRID_VALUES:
            print('Searching by grid with start step ', self._find_type_condition)
        elif self._find_type == GValues.RANDOM_VALUES:
            print('Searching by random search')

        print('At same time', self._at_same_time)
        print('Data set len ', self._data_set_len)

        for one in self._data_set:
            one.print_me()

    def gen_launch(self) -> DataLaunchExample:
        ret = DataLaunchExample()
        ret.set_trails(self._trials)
        ret.set_at_same_time(self._at_same_time)
        ret.set_program_path(self._program_path)
        ret.set_searching_word(self._searching_word)
        return ret
