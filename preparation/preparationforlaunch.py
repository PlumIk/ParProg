import other.GlobalFunction as GFunction

from Examples.conf.confexample import ConfExample
from selfsearch.fullrandomsearch import FullRandomSearch
from selfsearch.allvaluessearch import AllValuesSearch
from selfsearch.gridsearch import GridSearch
from selfsearch.gradsearch import GradSearch
from selfsearch.bayessearch import BayesSearch


def preparation(conf: ConfExample):
    if conf.get_valid() == 1:
        ret = None
        if conf.get_find_type() == 3:
            ret = FullRandomSearch().work(conf)
        elif conf.get_find_type() == 1:
            ret = AllValuesSearch().work(conf)
        elif conf.get_find_type() == 2:
            ret = GridSearch().work(conf)
        elif conf.get_find_type() == 4:
            ret = GradSearch().work(conf)
        elif conf.get_find_type() == 5:
            ret = BayesSearch().work(conf)

        print('good is:' + str(ret.get_better()))
        GFunction.to_file(conf.get_save_path(), ret)
    else:
        GFunction.set_red_text('Error:')
        GFunction.set_white_text('invalid conf')

    return
