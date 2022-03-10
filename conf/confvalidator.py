from Examples.conf.confexample import ConfExample
import other.GlobalFunction as GFunction
import other.GlobalValues as GValues


def is_valid(conf: ConfExample) -> bool:
    some_dict = conf.code_me()

    if len(some_dict) != 9 or some_dict.get('program_path') is None or some_dict.get('save_path') is None or \
            some_dict.get('find_type') is None or some_dict.get('find_condition') is None or \
            some_dict.get('searching_word') is None or \
            some_dict.get('trails') is None or some_dict.get('at_same_time') is None or \
            some_dict.get('data_set_len') is None or some_dict.get('data_set') is None:
        GFunction.set_red_text('Error:', end='')
        GFunction.set_white_text('Config does not match template', end='\n')
        return False

    if not (0 < some_dict['find_type'] < 6):
        GFunction.set_red_text('Error:', end='')
        GFunction.set_white_text('Unknown find type > 0', end='\n')
        return False

    if some_dict["trails"] < 1:
        GFunction.set_red_text('Error:', end='')
        GFunction.set_white_text('Trails need be > 0', end='\n')
        return False

    if some_dict["at_same_time"] < 1:
        GFunction.set_red_text('Error:', end='')
        GFunction.set_white_text('At same time need be > 0', end='\n')
        return False

    if some_dict['data_set_len'] != len(some_dict['data_set']):
        GFunction.set_red_text('Error:', end='')
        GFunction.set_white_text('Data set len and actual data set not match ', end='\n')
        return False

    return True
