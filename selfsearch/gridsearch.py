from Examples.conf.confexample import ConfExample
from Examples.launching.datalauchexample import DataLaunchExample
from Examples.selfsearch.datadict import DataDict
from programlaunching.programlauncher import LaunchSome
from selfsearch.searchinter import SearchInterface
from datawork.datagen.typegrid.gridstep_int import GridStepInt
from other import GlobalFunction as GFunction


def max_step(data: list) -> int:
    step = 0
    print(data)
    for one in data:
        sub_step = 1
        if len(one) != 1:
            sub_step = int(one[1]) - int(one[0])
            if sub_step < 0:
                sub_step = -sub_step
        if sub_step > step:
            step = sub_step
    return step


class GridSearch(SearchInterface):

    def __init__(self):
        super(GridSearch, self).__init__()

    def work(self, conf: ConfExample) -> DataDict:
        data_dict = DataDict()
        now_best = [-1, -1, -1, -1]
        workc = True
        data_list = list()
        now_step = 1
        for item in conf.get_data_set().items():
            now_step = item[1].get_find_condition()
            data_list.append(GridStepInt().add_par([now_step]).gen_data(item[1].get_range()))

        while workc:
            sub_data_dict = DataDict()

            print('data is', end='')
            print(data_list)
            data = conf.gen_launch()
            data.set_data_in(data_list)
            data = LaunchSome(data)
            print(data.get_data_out())
            GFunction.print_data_out(data.get_data_out())
            sub_data_dict.add_data_from_dict(data.get_data_out())
            sub_data_dict.print()
            print('all:')
            data_dict.merge_data(sub_data_dict.get_dict())
            data_dict.print()

            sub_data_list = list()
            if max_step(data_list) == 1:
                workc = False
            else:
                now_step = int(now_step / 5)
                now_best = sub_data_dict.get_better()
                for i in range(len(data_list)):
                    step_list = list()
                    for one in data_list[i]:
                        step_list.append(int(one))
                    step_list.sort()
                    prev = step_list[0]
                    end = 0
                    for j in range(len(step_list)):
                        if int(step_list[j]) == int(now_best[2][i]):
                            if j + 1 < len(step_list):
                                end = int(step_list[j + 1])
                            else:
                                end = int(step_list[j])
                            break
                        else:
                            prev = int(step_list[j])
                    sub_data_list.append(GridStepInt().add_par([now_step]).gen_data([prev, end]))
                data_list=sub_data_list

        return data_dict

    def step(self, data: DataLaunchExample):
        return self
