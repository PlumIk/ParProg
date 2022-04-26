from Examples.conf.confexample import ConfExample
from Examples.selfsearch.datadict import DataDict
from datawork.datagen.typerandom.randomsearch_int import RandomSearchInt
from programlaunching.programlauncher import LaunchSome


class FullRandomSearch:
    def __init__(self):
        self._data_dict = DataDict()
        print('Start full random search')

    def work(self, conf: ConfExample) -> DataDict:
        end = 50
        now_step = 0
        now_best = [-1, -1]

        while now_step != end:
            data_list = list()
            for one in conf.get_data_set():
                data_list.append(RandomSearchInt().add_par([1]).gen_data(one))

            data = conf.gen_launch()
            print(data_list)
            data.set_data_in(data_list)
            data = LaunchSome(data)
            self._data_dict.add_data_from_list(data.get_data_out())
            'print(now_step,now_best)'
            if conf.get_time_limit() != 0 and conf.get_time_limit() <= self._data_dict.get_time():
                now_step = end
            elif now_best[0] == -1:
                now_best = self._data_dict.get_better()
            else:
                now_p_better = self._data_dict.get_better()
                if now_best[1] > now_p_better[1]:
                    now_best = now_p_better
                    now_step = 0
                else:
                    now_step += 1

        return self._data_dict
