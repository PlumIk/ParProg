import other.GlobalFunction as GFunction

from Examples.conf.confexample import ConfExample
from selfsearch.fullrandomsearch import FullRandomSearch
from selfsearch.allvaluessearch import AllValuesSearch
from selfsearch.gridsearch import GridSearch
from Examples.launching.datalauchexample import DataLaunchExample


def preparation(conf: ConfExample):
    if conf.get_valid() == 1:
        ret = DataLaunchExample()
        print(conf.get_type())
        if conf.get_type() == 3:
            ret = FullRandomSearch().work(conf)
        elif conf.get_type() == 1:
            ret = AllValuesSearch().work(conf)
        elif conf.get_type() == 2:
            ret = GridSearch().work(conf)
        print('good is:' + str(ret.get_better()))
    else:
        GFunction.set_red_text('Error:')
        GFunction.set_white_text('invalid conf')

    return
