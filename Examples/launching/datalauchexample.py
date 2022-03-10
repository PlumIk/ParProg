class DataLaunchExample:

    def __init__(self):
        self._program_path = ''
        self._searching_word = ''
        self._data_in = list()
        self._data_out = list()
        self._trails = 1
        self._at_same_time = 1
        self._at_same_time = 1

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

    def get_program_path(self) -> str:
        return self._program_path

    def set_program_path(self, program_path: str):
        self._program_path = program_path
        return self

    def get_searching_word(self) -> str:
        return self._searching_word

    def set_searching_word(self, searching_word: str):
        self._searching_word = searching_word
        return self

    def get_data_in(self) -> list:
        return self._data_in

    def set_data_in(self, data: list):
        self._data_in = data
        return self

    def update_data_out(self, data: list):
        self._data_out = self._data_out + data
        return self

    def get_data_out(self) -> list:
        return self._data_out

    def set_data_out(self, data: list):
        self._data_out = data
        return self
