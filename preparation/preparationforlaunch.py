import other.GlobalValues as GValues
import other.GlobalFunction as GFunction

from Examples.conf.confexample import ConfExample
from datawork.datagen.typegrid.gridstep_int import GridStepInt
from datawork.datagen.typeother.allvalues_int import AllValuesInt
from datawork.datagen.typerandom.randomsearch_int import RandomSearchInt
from programlaunching.programlauncher import LaunchSome
from selfsearch.fullrandomsearch import FullRandomSearch
from Examples.selfsearch.datadict import DataDict


def preparation(conf: ConfExample):
    if conf.get_valid() == 1:
        ret = FullRandomSearch().work(conf)
        print(ret.get_better())
    else:
        GFunction.set_red_text('Error:')
        GFunction.set_white_text('invalid conf')

    """for item in conf.get_data_set().items():
        data_one = item[1]
        if data_one.get_condition_type() == GValues.RANGE:
            if data_one.get_find_type() == GValues.ALL_VALUES:
                data_list.append(AllValuesInt().gen_data(data_one.get_range()))
            elif data_one.get_find_type() == GValues.GRID_VALUES:
                data_list.append(GridStepInt().add_par([data_one.get_find_condition()]).gen_data(data_one.get_range()))
            elif data_one.get_find_type() == GValues.RANDOM_VALUES:
                data_list.append(RandomSearchInt().add_par([data_one.get_find_condition()]).gen_data(data_one.get_range()))
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
    data = conf.gen_launch()
    data.set_data_in(data_list)
    data = LaunchSome(data)
    print(data.get_data_out())
    GFunction.print_data_out(data.get_data_out())"""

    return
