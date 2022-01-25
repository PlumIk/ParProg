import itertools

from preparation.preparationforlaunch import preparation
from conf.confcreator import start_work, work_with_per
from Examples.conf.confexample import ConfExample
from datawork.datagen.typegrid.gridstep_int import GridStepInt
from datawork.datagen.typeother.allvalues_int import AllValuesInt


def to_string(data: list):
    for i in range(len(data)):
        data[i] = [str(x) for x in data[i]]


class Test:
    def __init__(self, test):

        if test == 1:
            print('dont work')
        elif test == 2:
            data = [102, 100]
            print(AllValuesInt().gen_data(data))
        elif test == 3:
            data = [103, 101]
            print(GridStepInt().add_par([2]).gen_data(data))
        elif test == 4:
            data = [['as', 'bfgh', 'c'], ['d'], ['e', 'fh'], [1, 2, 3]]
            to_string(data)
            data = list(itertools.product(*data))
            print(data)
            for parsi in data:
                pars = list()
                for i in parsi:
                    pars.append(i)
                print(['./now.out'] + pars)
        elif test == 5:
            print('dont work')
        elif test == 6:
            print("Valid: " + str(start_work().get_valid()))
        elif test == 7:
            work_with_per(ConfExample())
            return
        elif test == 8:
            string = 'asdsa'
            string = string.split('_')
            for_print = ''
            for one in string:
                for_print += one
            print(for_print)
        elif test == 9:
            conf = start_work()
            print("Valid: " + str(conf.get_valid()))
            preparation(conf)
