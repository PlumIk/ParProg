from Examples.conf.confexample import ConfExample
from Examples.conf.dataexample import DataExample
from Examples.selfsearch.datadict import DataDict
from datawork.datagen.typegrid.gridstep_int import GridStepInt
from other import GlobalValues as GValues
from programlaunching.programlauncher import LaunchSome


def max_step(data: list, conf: ConfExample) -> int:
    step = 0
    for i in range(len(data)):
        sub_step = 0
        if len(data[i]) == 1:
            sub_step = 1
        else:
            if conf.get_data_set()[i].get_type() == GValues.INT:
                sub_step = int(data[i][1]) - int(data[i][0])
            elif conf.get_data_set()[i].get_type() == GValues.STR:
                sub_step = conf.get_data_set()[i].get_range().index(data[i][1]) - \
                           conf.get_data_set()[i].get_range().index(data[i][0])

        if sub_step > step:
            step = sub_step

    return step


class GridSearch:

    def __init__(self):
        self._data_dict = DataDict()
        print('Start grid search')

    def work(self, conf: ConfExample) -> DataDict:
        still_work = True
        data_list = list()
        now_step = conf.get_find_condition()
        for one in conf.get_data_set():
            data_list.append(GridStepInt().add_par([now_step]).gen_data(one))

        while still_work:
            sub_data_dict = DataDict()

            data = conf.gen_launch()
            data.set_data_in(data_list)
            data = LaunchSome(data)
            sub_data_dict.add_data_from_list(data.get_data_out())
            self._data_dict.add_data_from_dict(sub_data_dict.get_dict())

            sub_data_list = list()
            if max_step(data_list, conf) <= 1:
                still_work = False
            else:
                p_step = now_step
                now_step = int(now_step / 5)
                if now_step < 1:
                    now_step = 1
                now_best = sub_data_dict.get_better()
                for i in range(len(data_list)):
                    now_data = data_list[i]
                    if str(now_data[0]).isdigit():
                        index = now_data.index(now_best[0][i])
                        new_rang = [0, 0]
                        if index > 0:
                            new_rang[0] = int(now_data[index - 1])
                        else:
                            new_rang[0] = int(now_data[index])
                        if index < len(now_data):
                            new_rang[1] = int(now_data[index + 1])
                        else:
                            new_rang[1] = int(now_data[index])
                        one = DataExample().set_type(GValues.INT).set_range(new_rang)
                        sub_data_list.append(GridStepInt().add_par([now_step]).gen_data(one))
                    else:
                        index = now_data.index(now_best[0][i])

                        new_rang = [0, 0]
                        if index - p_step > 0:
                            new_rang[0] = now_data[index - p_step]
                        else:
                            new_rang[0] = now_data[index]
                        if index + p_step < len(now_data):
                            new_rang[1] = now_data[index + p_step]
                        else:
                            new_rang[1] = now_data[index]
                        datas = conf.get_data_set()[i].get_range()
                        stat = datas.index(new_rang[0])
                        end = datas.index(new_rang[1])
                        new_rang = list()
                        for j in range(stat, end+1):
                            new_rang.append(datas[j])
                        one = DataExample().set_type(GValues.STR).set_range(new_rang)
                        sub_data_list.append(GridStepInt().add_par([now_step]).gen_data(one))
                data_list = sub_data_list

        return self._data_dict
