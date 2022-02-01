from Examples.conf.confexample import ConfExample
from Examples.launching.datalauchexample import DataLaunchExample
from Examples.selfsearch.datadict import DataDict
from programlaunching.programlauncher import LaunchSome
from selfsearch.searchinter import SearchInterface
from datawork.datagen.typerandom.randomsearch_int import RandomSearchInt
from other import GlobalFunction as GFunction


class FullRandomSearch(SearchInterface):
    def __init__(self):
        super(FullRandomSearch, self).__init__()

    def work(self, conf: ConfExample) -> DataDict:
        end = 50
        now_step = 0
        now_best = [-1, -1, -1, -1]
        data_dict = DataDict()

        while now_step != end:
            data_list = list()
            for item in conf.get_data_set().items():
                data_list.append(RandomSearchInt().add_par([1]).gen_data(item[1].get_range()))

            print('data is', end='')
            print(data_list)
            data = conf.gen_launch()
            data.set_data_in(data_list)
            data = LaunchSome(data)
            print(data.get_data_out())
            GFunction.print_data_out(data.get_data_out())
            data_dict.add_data_from_dict(data.get_data_out())
            data_dict.print()

            if now_best[0] == -1:
                now_best = data_dict.get_better()
            else:
                now_p_better = data_dict.get_better()
                if now_p_better[2] < now_best[2] and (now_p_better[0] != now_best[0] or now_p_better[1] != now_best[1]
                                                      or now_p_better[2] != now_best[2]):
                    now_best = now_p_better
                    now_step = 0
                else:
                    now_step += 1

        return data_dict

    def step(self, data: DataLaunchExample):
        return self
