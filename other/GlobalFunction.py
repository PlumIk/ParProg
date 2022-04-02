import other.GlobalValues as GValues
from Examples.selfsearch.datadict import DataDict


def set_red_text(text='', end=''):
    print(GValues.RED_TEXT.format(text), end=end)
    return


def set_white_text(text='', end=''):
    print(GValues.WHITE_TEXT.format(text), end=end)
    return


def any_list_to_string_list(data: list):
    for i in range(len(data)):
        data[i] = [str(x) for x in data[i]]
    return data


def get_max_values(value: int, size: int) -> int:
    return value * size


def to_file(file_name: str, data: DataDict):
    f = open(file_name, 'w')
    print(file_name)
    some_dict = data.get_dict()
    for item in some_dict.items():
        some_line = "For dataset \'" + str(item[0]) + "\' mid value " + str(data.get_mid_value(item[0])) + \
                    ". All values:"
        for one in item[1]:
            some_line += '\n\t' + str(one)
        some_line += '\n'
        print(some_line)
        f.write(some_line)


def pars_out(data: str, word: str) -> float:
    some_list = data.split('\n')
    for one in some_list:
        if one.split(':')[0].lower() == word:
            return float(one.split(':')[1])
    return None
