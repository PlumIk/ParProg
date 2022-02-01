from Examples.conf.dataexample import DataExample
from Examples.launching.datalauchexample import DataLaunchExample


class ConfExample:
    _compilers = list()
    _program_path = ' '
    _save_path = ' '
    _trials = 1
    _at_same_time = 1
    _keys = dict()
    _initial_key = ''
    _data_set_len = 0
    _data_set = dict()
    _valid = 0

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

    def get_compilers(self) -> list:
        return self._compilers

    def set_compilers(self, compilers: list):
        self._compilers = compilers
        return self

    def get_keys(self) -> dict:
        return self._keys

    def set_keys(self, keys: dict):
        self._keys = keys
        return self

    def get_initial_key(self) -> str:
        return self._initial_key

    def set_initial_key(self, initial_key: str):
        self._initial_key = initial_key
        return self

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

    def get_data_set(self) -> dict:
        return self._data_set

    def set_data_set(self, data_set: dict):
        self._data_set = data_set
        return self

    def code_me(self) -> dict:
        some_dict = dict()
        some_dict.setdefault('program_path', self._program_path)
        some_dict.setdefault('save_path', self._save_path)
        some_dict.setdefault('compilers', self._compilers)
        some_dict.setdefault('keys', self._keys)
        some_dict.setdefault('initial_key', self._initial_key)
        some_dict.setdefault('trails', self._trials)
        some_dict.setdefault('at_same_time', self._at_same_time)
        some_dict.setdefault('data_set_len', self._data_set_len)

        a_some_dict = dict()
        for item in self._data_set.items():
            a_some_dict.setdefault(item[0], item[1].code_me())

        some_dict.setdefault('data_set', a_some_dict)
        return some_dict

    def encode_me(self, in_dict: dict):
        self._program_path = in_dict.get('program_path')
        self._save_path = in_dict.get('save_path')
        self._compilers = in_dict.get('compilers')
        self._keys = in_dict.get('keys')
        self._initial_key = in_dict.get('initial_key')
        self._trials = in_dict.get('trails')
        self._at_same_time = in_dict.get('at_same_time')
        self._data_set_len = in_dict.get('data_set_len')

        in_dict = in_dict.get('data_set')
        self._data_set = dict()
        for item in in_dict.items():
            self._data_set.setdefault(item[0], DataExample().encode_me(item[1]))

        return self

    def get_type(self) -> int:
        for item in self._data_set.items():
            return item[1].get_find_type()

    def gen_launch(self) -> DataLaunchExample:
        ret = DataLaunchExample()
        ret.set_keys(self._keys)
        ret.set_trails(self._trials)
        ret.set_initial_key(self._initial_key)
        ret.set_at_same_time(self._at_same_time)
        ret.set_compilers(self._compilers)
        ret.set_program_path(self._program_path)
        return ret
