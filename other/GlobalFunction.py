import other.GlobalValues as GValues


def set_red_text(text='', end=''):
    print(GValues.RED_TEXT.format(text), end=end)
    return


def set_white_text(text='', end=''):
    print(GValues.WHITE_TEXT.format(text), end=end)
    return


def to_string(data: list):
    for i in range(len(data)):
        data[i] = [str(x) for x in data[i]]
    return data


def print_data_out(data_out: dict):
    for item in data_out.items():
        print(item[0] + ':')
        for one_data_set in item[1]:
            print('\tkeys:', end='')
            print(one_data_set[0], end='')
            print('|data:', end='')
            print(one_data_set[1], end='')
            print('|time:', end='')
            print(one_data_set[2])
        print('')
