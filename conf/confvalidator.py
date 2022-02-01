from Examples.conf.confexample import ConfExample
import other.GlobalFunction as GFunction


def is_valid(conf: ConfExample) -> bool:
    some_dict = conf.code_me()

    if len(some_dict) != 9 or some_dict.get('program_path') is None or some_dict.get('save_path') is None or \
            some_dict.get('compilers') is None or some_dict.get('keys') is None or \
            some_dict.get('initial_key') is None or \
            some_dict.get('trails') is None or some_dict.get('at_same_time') is None or \
            some_dict.get('data_set_len') is None or some_dict.get('data_set') is None:
        GFunction.set_red_text('Error:', end='')
        GFunction.set_white_text('config does not match template', end='\n')
        return False

    if len(some_dict["keys"]) != len(some_dict["compilers"]):
        GFunction.set_red_text('Error:', end='')
        GFunction.set_white_text('the number of compilers and keys not match ', end='\n')
        return False

    if some_dict["trails"] < 1:
        GFunction.set_red_text('Error:', end='')
        GFunction.set_white_text('trails need be > 0', end='\n')
        return False

    if some_dict["at_same_time"] < 1:
        GFunction.set_red_text('Error:', end='')
        GFunction.set_white_text('at same time need be > 0', end='\n')
        return False

    if some_dict['data_set_len'] != len(some_dict['data_set']):
        GFunction.set_red_text('Error:', end='')
        GFunction.set_white_text('data set len and actual data set not match ', end='\n')
        return False

    return True
