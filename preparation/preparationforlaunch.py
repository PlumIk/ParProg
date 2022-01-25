import other.GlobalValues as GValues
import other.GlobalFunction as GFunction

from Examples.conf.confexample import ConfExample
from programlaunching.programlauncherOLD import ProgramLauncherOLD
from datawork.datagen.typegrid.gridstep_int import GridStepInt
from datawork.datagen.typeother.allvalues_int import AllValuesInt


def preparation(conf: ConfExample):
    data_list = list()

    for item in conf.get_data_set().items():
        data_one = item[1]
        if data_one.get_condition_type() == GValues.RANGE:
            if data_one.get_find_type() == GValues.ALL_VALUES:
                data_list.append(AllValuesInt().gen_data(data_one.get_range()))
            elif data_one.get_find_type() == GValues.GRID_VALUES:
                data_list.append(GridStepInt().add_par([data_one.get_find_condition()]).gen_data(data_one.get_range()))
            else:
                GFunction.set_red_text('Error:')
                GFunction.set_white_text('unknown find type')
                return
        else:
            GFunction.set_red_text('Error:')
            GFunction.set_white_text('unknown condition type')
            return

    print('data is', end='')
    print(data_list)

    prog = ProgramLauncherOLD()
    prog.run(conf.get_compilers(), conf.get_program_path(), conf.get_keys(), data_list, conf.get_compiler(),
             conf.get_compiler_name(), conf.get_trails(), conf.get_at_same_time())
    print(prog.get_data())

    return
