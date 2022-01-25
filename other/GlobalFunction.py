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
