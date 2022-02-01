class DataLaunchExample:
    _compilers = list()
    _program_path = ''
    _keys = dict()
    _data_in = list()
    _data_out = dict()
    _initial_key = ''
    _trails = 1
    _at_same_time = 1

    def __init__(self):
        self._at_same_time = 1


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

    def get_trails(self) -> int:
        return self._trails

    def set_trails(self, trails: int):
        self._trails = trails
        return self

    def get_at_same_time(self) -> int:
        return self._at_same_time

    def set_at_same_time(self, at_same_time: int):
        self._at_same_time = at_same_time
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

    def get_data_in(self) -> list:
        return self._data_in

    def set_data_in(self, data: list):
        self._data_in = data
        return self

    def update_data_out(self, data):
        self._data_out.update(data)
        return self

    def get_data_out(self) -> dict:
        return self._data_out

    def set_data_out(self, data: dict):
        self._data_out = data
        return self

