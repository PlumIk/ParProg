import json
import os

from Examples.conf.confexample import ConfExample
from conf.confvalidator import is_valid
from Examples.conf.dataexample import DataExample
from other import GlobalValues as GValues

EXIT = 0


def start_work() -> ConfExample:
    global EXIT
    conf = ConfExample()
    answer = 1

    while answer != 'y' and answer != 'Y' and answer != 'n' and answer != 'N' and answer != '0':
        print('Load config file? (y/n, 0 - exit) ')
        answer = input()
    if answer == EXIT:
        conf.set_invalid()
        return conf
    elif answer == 'y' or answer == 'Y':
        conf = _load_conf()
        if not is_valid(conf):
            conf.set_invalid()
            return conf
        else:
            conf.set_valid()
    else:

        answer = 'n'
        while answer != 'y' and answer != 'Y' and answer != EXIT:
            if answer == 'n' or answer == 'N':
                _choose_program_path(conf)
            elif answer == '9':
                show_all(conf)
            elif answer == '8':
                _print_program_path(conf, 'Program path now:')
            print('Continue? (y/n, 0 - exit, 9 - show all, 8 - show only program path)')
            answer = input()
        if answer == EXIT:
            conf.set_invalid()
            return conf

        answer = 'n'
        while answer != 'y' and answer != 'Y' and answer != EXIT:
            if answer == 'n' or answer == 'N':
                _choose_save_path(conf)
            elif answer == '9':
                show_all(conf)
            elif answer == '8':
                _print_save_path(conf, 'Save path now:')
            print('Continue? (y/n, 0 - exit, 9 - show all, 8 - show only save path)')
            answer = input()
        if answer == EXIT:
            conf.set_invalid()
            return conf

        answer = 'n'
        while answer != 'y' and answer != 'Y' and answer != EXIT:
            if answer == 'n' or answer == 'N':
                _choose_searching_word(conf)
            elif answer == '9':
                show_all(conf)
            elif answer == '8':
                _print_searching_word(conf, 'PSearching word now:')
            print('Continue? (y/n, 0 - exit, 9 - show all, 8 - show only searching_word)')
            answer = input()
        if answer == EXIT:
            conf.set_invalid()
            return conf

        answer = 'n'
        while answer != 'y' and answer != 'Y' and answer != EXIT:
            if answer == 'n' or answer == 'N':
                _choose_trails(conf)
            elif answer == '9':
                show_all(conf)
            elif answer == '8':
                _print_trails(conf, 'Trails now:')
            print('Continue? (y/n, 0 - exit, 9 - show all, 8 - show only trails)')
            answer = input()
        if answer == EXIT:
            conf.set_invalid()
            return conf

        answer = 'n'
        while answer != 'y' and answer != 'Y' and answer != EXIT:
            if answer == 'n' or answer == 'N':
                _choose_at_same_time(conf)
            elif answer == '9':
                show_all(conf)
            elif answer == '8':
                _print_at_same_time(conf, 'At same time now:')
            print('Continue? (y/n, 0 - exit, 9 - show all, 8 - show only at same time)')
            answer = input()
        if answer == EXIT:
            conf.set_invalid()
            return conf

        conf = work_with_per(conf)

    print('\nData now:')
    show_all(conf)

    print('Save it?(y/n)')
    answer = input()
    if answer.lower() == 'y':
        _save_conf(conf)
    if not is_valid(conf):
        conf.set_invalid()
        return conf
    else:
        conf.set_valid()

    return conf


def _load_conf() -> ConfExample:
    conf = ConfExample()
    print('Files now: ')
    value = 1
    for one in os.listdir('configs/'):
        print('\t' + str(value) + ')' + one)
        value += 1
    print('Witch use?')
    value = input()
    while not str(value).isdigit():
        _try_again('not a number')
        value = input()
    value = int(value)
    if 0 < value <= len(os.listdir('configs/')):
        print('Wait')
        with open("configs/" + os.listdir('configs/')[value - 1], "r") as read_file:
            conf.encode_me(json.load(read_file))
    return conf


def _save_conf(conf: ConfExample):
    print('Set name')
    with open('configs/' + input() + '.json', 'w') as write_file:
        json.dump(conf.code_me(), write_file, indent=4)


def _choose_program_path(conf: ConfExample) -> ConfExample:
    _print_program_path(conf, 'Now program path is:')

    print('Enter full path to program for test')
    some_string = input()
    conf.set_program_path(some_string)
    _print_program_path(conf, 'Now program path is:')

    return conf


def _print_program_path(conf: ConfExample, for_print=''):
    print(for_print + conf.get_program_path())
    return


def _choose_save_path(conf: ConfExample) -> ConfExample:
    _print_save_path(conf, 'Now save path is:')

    print('Enter full path to save data')
    some_string = input()
    conf.set_save_path(some_string)
    _print_save_path(conf, 'Now save path is:')

    return conf


def _choose_searching_word(conf: ConfExample) -> ConfExample:
    _print_searching_word(conf, 'Searching word is:')

    print('Enter full searching word without spaces')
    some_string = input()
    conf.set_searching_word(some_string)
    _print_searching_word(conf, 'Now searching word is:')

    return conf


def _print_searching_word(conf: ConfExample, for_print=''):
    print(for_print + conf.get_searching_word())
    return


def _print_save_path(conf: ConfExample, for_print=''):
    print(for_print + conf.get_save_path())
    return


def _choose_trails(conf: ConfExample) -> ConfExample:
    _print_trails(conf, 'Now trails is:')

    some_string = 'a'
    while not some_string.isdigit():
        print('Enter trails')
        some_string = input()
    conf.set_trails(int(some_string))
    _print_trails(conf, 'Now trails is:')

    return conf


def _print_trails(conf: ConfExample, for_print=''):
    print(for_print + str(conf.get_trails()))
    return


def _choose_at_same_time(conf: ConfExample) -> ConfExample:
    _print_at_same_time(conf, 'Now at same time is:')

    some_string = 'a'
    while not some_string.isdigit():
        print('Enter at same time')
        some_string = input()
    conf.set_at_same_time(int(some_string))
    _print_at_same_time(conf, 'Now at same time is:')

    return conf


def _print_at_same_time(conf: ConfExample, for_print=''):
    print(for_print + str(conf.get_at_same_time()))
    return


def work_with_per(conf: ConfExample) -> ConfExample:
    data_set = list()
    pers = 0

    answer = 'n'
    while answer != 'y' and answer != 'Y' and answer != EXIT:
        if answer == 'n' or answer == 'N':
            print('How many different parameters?')
            pers = input()
        if not str(pers).isdigit():
            answer = 'n'
        else:
            pers = int(pers)
            print('Now we have ' + str(pers) + ' parameters')
            print('Continue? (y/n, 0 - exit)')
            answer = input()
    if answer == EXIT:
        conf.set_invalid()
        return conf

    conf.set_data_set_len(pers)

    conf.set_find_type(_choose_find_type())
    if conf.need_find_condition():
        conf.set_find_condition(_choose_find_condition())

    now_pers = 0
    while now_pers < pers:
        answer = 'n'
        data_one = DataExample()
        while answer != 'y' and answer != 'Y':
            if answer == 'n' or answer == 'N':
                data_one = _gen_data_one()
            else:
                _try_again('incorrect answer')
            data_one.print_me()
            print('Continue? (y/n)')
            answer = input()
        data_set.append(data_one)
        now_pers += 1
    conf.set_data_set(data_set)
    return conf


def _gen_data_one() -> DataExample:
    data_one = DataExample()
    data_one.set_type(_choose_type())
    if data_one.get_type() == 1:
        data_one.set_range(_choose_range())
    elif data_one.get_type() == 2:
        data_one.set_range(_choose_string())

    return data_one


def _choose_find_type() -> int:
    print('What find time you want to use? 1 - all values, 2 grid search, 3 - random search')
    ret = input()
    while not ret.isdigit():
        _try_again('not a number')
        ret = input()
    ret = int(ret)
    if ret < 1 or ret > 3:
        _try_again('incorrect type')
        return _choose_find_type()
    return ret


def _choose_find_condition() -> int:
    print('What condition')
    ret = input()
    while not ret.isdigit():
        _try_again('not a number')
        ret = input()
    ret = int(ret)
    return ret


def _choose_type() -> int:
    answer = '0'
    while answer != '1' and answer != '2':
        print('Type (1 - int, 2 -string)')
        answer = input()
    return int(answer)


def _choose_condition_type() -> int:
    return GValues.RANGE


def _choose_string() -> list:
    print("Enter all key sets. Key sets are separated by a dot, keys in a set are separated by spaces")
    return input().split('.')


def _choose_range() -> list:
    some_list = list()
    print('Enter minimum value')
    some_list.append(input())
    print('Enter maximum value')
    some_list.append(input())
    while not some_list[0].isdigit() or not some_list[1].isdigit():
        _try_again('incorrect type')
        print('Enter minimum value')
        some_list[0] = input()
        print('Enter maximum value')
        some_list[1] = input()
    some_list[0] = int(some_list[0])
    some_list[1] = int(some_list[1])
    return some_list


def _choose_complex_condition() -> list:
    answer = 'y'
    some_list = list()
    while answer == 'y' or answer == 'Y':
        print('Enter one complex condition')
        some_list.append(input())
        print('More condition for this parameter?(y/n)')
        answer = input()
        if answer != 'y' and answer != 'Y' and answer != 'n' and answer != 'N':
            print('More condition for this parameter?(y/n)')
            answer = input()
    return some_list


def _try_again(for_print='friend'):
    print('Try again, ' + for_print)
    return


def show_all(conf: ConfExample):
    conf.print_me()

    return
