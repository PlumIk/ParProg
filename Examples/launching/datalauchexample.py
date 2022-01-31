class DataLaunchExample:
    _compilers = list()
    _program_path = ''
    _keys = dict()
    _data_in = list()
    _data_out = dict()
    _compiler = ''
    _compiler_name = ''
    _trails = 1
    _at_same_time = 1

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

    def get_compiler(self) -> str:
        return self._compiler

    def set_compiler(self, compiler: str):
        self._compiler = compiler
        return self

    def get_compiler_name(self) -> str:
        return self._compiler_name

    def set_compiler_name(self, compiler_name: str):
        self._compiler_name = compiler_name
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
