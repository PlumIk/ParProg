from random import random

from Examples.conf.confexample import ConfExample
from Examples.conf.dataexample import DataExample
from Examples.selfsearch.datadict import DataDict
from datawork.datagen.typeother.allvalues_int import AllValuesInt
from other import GlobalValues as GValues
from programlaunching.programlauncher import LaunchSome
from selfsearch.fullrandomsearch import FullRandomSearch


class GradSearch:
    def __init__(self):
        self._data_dict = DataDict()
        print('Start gradient search')

    def work(self, conf: ConfExample) -> DataDict:
        self._data_dict = FullRandomSearch().work(conf)
        now_best = self._data_dict.get_better()

        still_work = True

        if conf.get_time_limit() != 0 and conf.get_time_limit() <= self._data_dict.get_time():
            still_work = False

        while still_work:

            sub_data_dict = DataDict()

            sub_data_list = list()
            now = 0

            for one in conf.get_data_set():
                now_data = one.get_range()
                if one.get_type() == GValues.INT:
                    new_rang = [0, 0]
                    if int(now_best[0][now]) > now_data[0]:
                        new_rang[0] = int(now_best[0][now]) - 1
                    else:
                        new_rang[0] = int(now_best[0][now])
                    if int(now_best[0][now]) < now_data[1]:
                        new_rang[1] = int(now_best[0][now]) + 1
                    else:
                        new_rang[1] = int(now_best[0][now])
                    one = DataExample().set_type(GValues.INT).set_range(new_rang)
                    sub_data_list.append(AllValuesInt().gen_data(one))
                elif one.get_type() == GValues.STR:
                    index = now_data.index(now_best[0][now])

                    new_rang = [0, 0]
                    if index - 1 >= 0:
                        new_rang[0] = now_data[index - 1]
                    else:
                        new_rang[0] = now_data[index]
                    if index + 1 < len(now_data):
                        new_rang[1] = now_data[index + 1]
                    else:
                        new_rang[1] = now_data[index]
                    datas = conf.get_data_set()[now].get_range()
                    stat = datas.index(new_rang[0])
                    end = datas.index(new_rang[1])
                    new_rang = list()
                    for j in range(stat, end + 1):
                        new_rang.append(datas[j])
                    one = DataExample().set_type(GValues.STR).set_range(new_rang)
                    sub_data_list.append(AllValuesInt().gen_data(one))
                    now += 1
                else:
                    new_rang = [0, 0]
                    if float(now_best[0][now]) > now_data[0]:
                        new_rang[0] = float(now_best[0][now]) - random()
                    else:
                        new_rang[0] = float(now_best[0][now])
                    if float(now_best[0][now]) < now_data[1]:
                        new_rang[1] = float(now_best[0][now]) + random()
                    else:
                        new_rang[1] = float(now_best[0][now])
                    sub_data_list.append(new_rang)

            data_list = sub_data_list
            data = conf.gen_launch()
            data.set_data_in(data_list)
            data = LaunchSome(data)
            sub_data_dict.add_data_from_list(data.get_data_out())
            self._data_dict.add_data_from_dict(sub_data_dict.get_dict())
            now_p_better = self._data_dict.get_better()
            if now_best[1] > now_p_better[1]:
                now_best = now_p_better
            else:
                still_work = False
            if conf.get_time_limit() != 0 and conf.get_time_limit() <= self._data_dict.get_time():
                still_work = False

        return self._data_dict
