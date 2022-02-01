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
                conf = _choose_compilers(conf)
            elif answer == '9':
                show_all(conf)
            elif answer == '8':
                _print_compiles(conf, 'Compiles now:')
            print('Continue? (y/n, 0 - exit, 9 - show all, 8 - show only compilers)')
            answer = input()
        if answer == EXIT:
            conf.set_invalid()
            return conf

        answer = 'n'
        while answer != 'y' and answer != 'Y' and answer != EXIT:
            if answer == 'n' or answer == 'N':
                conf = _choose_keys(conf)
            elif answer == '9':
                show_all(conf)
            elif answer == '8':
                _print_keys(conf, 'Keys now:')
            print('Continue? (y/n, 0 - exit, 9 - show all, 8 - show only keys)')
            answer = input()
        if answer == EXIT:
            conf.set_invalid()
            return conf

        answer = 'n'
        while answer != 'y' and answer != 'Y' and answer != EXIT:
            if answer == 'n' or answer == 'N':
                conf = _choose_initial_key(conf)
            elif answer == '9':
                show_all(conf)
            elif answer == '8':
                _print_initial_key(conf, 'Keys now:')
            print('Continue? (y/n, 0 - exit, 9 - show all, 8 - show only key)')
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


def _print_save_path(conf: ConfExample, for_print=''):
    print(for_print + conf.get_save_path())
    return


def _choose_compilers(conf: ConfExample) -> ConfExample:
    _print_compiles(conf, 'Now compilers is:')

    print('Enter all compilers separated by commas without spaces')

    some_string = input()
    some_list = some_string.split(',')
    conf.set_compilers(some_list)
    _print_compiles(conf, 'Now compilers is:')

    return conf


def _print_compiles(conf: ConfExample, for_print=''):
    some_list = conf.get_compilers()
    if len(some_list) > 0:
        for i in range(len(some_list)):
            for_print += '\"' + some_list[i] + '\"' + ','

    if for_print[len(for_print) - 1] == ',':
        for_print = for_print[:len(for_print) - 1]
    print(for_print)
    return


def _choose_keys(conf: ConfExample) -> ConfExample:
    _print_keys(conf, 'Keys now:')

    print("Enter all key sets. Key sets are separated by a dot, keys in a set are separated by commas, without spaces")
    some_dict = dict()

    for comp in conf.get_compilers():
        print('Enter a set of keys for the compiler ' + comp)
        some_list = list()
        some_string = input()
        some_string = some_string.split('.')
        for one_set in some_string:
            some_list.append(one_set.split(','))
        some_dict.setdefault(comp, some_list)

    conf.set_keys(some_dict)
    _print_keys(conf, 'Now keys is:\n')

    return conf


def _print_keys(conf: ConfExample, for_print=''):
    some_dict = conf.get_keys()

    for item in some_dict.items():
        for_print += '\t' + item[0] + ':'
        for key_set in item[1]:
            for key in key_set:
                for_print += '\"' + key + '\",'
            if for_print[len(for_print) - 1] == ',':
                for_print = for_print[:len(for_print) - 1]
        if for_print[len(for_print) - 1] == ',':
            for_print = for_print[:len(for_print) - 1]
        for_print += ',\n'
    if for_print[len(for_print) - 1] == '\n':
        for_print = for_print[:len(for_print) - 2]
    print(for_print)
    return


def _choose_initial_key(conf: ConfExample) -> ConfExample:
    _print_initial_key(conf, 'Initial key is:')
    print('Do you wand have initial key?(y/n)')

    answer = input()
    if answer.lower() == 'y':
        print('Enter full initial key')
        some_string = input()
        conf.set_initial_key(some_string)
        _print_initial_key(conf, 'Now initial key:')

    return conf


def _print_initial_key(conf: ConfExample, for_print=''):
    print(for_print + conf.get_initial_key())
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
    data_set = dict()
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

    all_condition = 0
    all_is_one = True
    type_of_all = _choose_find_type()
    if DataExample().set_find_type(type_of_all).need_find_condition():
        all_condition = _choose_find_condition()

    now_pers = 0
    while now_pers < pers:

        if data_set.get(now_pers) is None:
            answer = 'n'
            data_one = DataExample()
            while answer != 'y' and answer != 'Y':
                if answer == 'n' or answer == 'N':
                    data_one = _gen_data_one(all_is_one, type_of_all, all_condition)
                else:
                    _try_again('incorrect answer')
                data_one.print_me('Data now is: name\"' + str(now_pers) + '\" ')
                print('Continue? (y/n)')
                answer = input()
            data_set.setdefault(now_pers, data_one)
            now_pers += 1

        else:
            _try_again('Not unique name')

    _print_all_data(conf)
    conf.set_data_set(data_set)
    return conf


def _gen_data_one(all_is_one=False, type_of_all=1, all_condition=1) -> DataExample:
    data_one = DataExample()

    if all_is_one:
        data_one.set_find_type(type_of_all)
        data_one.set_find_condition(all_condition)
    else:
        data_one.set_find_type(_choose_find_type())
        if data_one.need_find_condition():
            data_one.set_find_condition(_choose_find_condition())

    data_one.set_type(_choose_type())
    data_one.set_range(_choose_range())

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
    return GValues.INT


def _choose_condition_type() -> int:
    return GValues.RANGE


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


def _print_all_data(conf: ConfExample):
    print('Now have ' + str(conf.get_data_set_len()) + ' parameters')
    print_about = True
    for item in conf.get_data_set().items():
        if print_about:
            item[1].print_type('Find type is ')
            print_about = False
        item[1].print_me('Name \"' + str(item[0]) + '\"')


def show_all(conf: ConfExample):
    _print_program_path(conf, 'Program path:')
    # print(conf.get_program_path())
    _print_save_path(conf, 'Save path:')
    # print(conf.get_save_path())
    _print_compiles(conf, 'Compilers:')
    # print(conf.get_compilers())
    _print_keys(conf, 'Keys:\n')
    # print(conf.get_keys())
    _print_trails(conf, 'Trails:')
    # print(conf.get_trails())
    _print_at_same_time(conf, 'At same time:')
    # print(conf.get_at_same_time())
    _print_all_data(conf)

    return
