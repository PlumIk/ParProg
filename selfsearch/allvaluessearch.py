from Examples.conf.confexample import ConfExample
from Examples.launching.datalauchexample import DataLaunchExample
from Examples.selfsearch.datadict import DataDict
from programlaunching.programlauncher import LaunchSome
from datawork.datagen.typeother.allvalues_int import AllValuesInt
from other import GlobalFunction as GFunction


class AllValuesSearch:
    def __init__(self):
        print('Start searching by use all parameters')

    def work(self, conf: ConfExample) -> DataDict:
        data_dict = DataDict()

        data_list = list()

        for one in conf.get_data_set():
            data_list.append(AllValuesInt().gen_data(one))

        print('data is', end='')
        print(data_list)
        data = conf.gen_launch()
        data.set_data_in(data_list)
        data = LaunchSome(data)
        print(data.get_data_out())
        data_dict.add_data_from_list(data.get_data_out())
        data_dict.print()

        print('asdsa ', data_dict.get_better())

        return data_dict

    def step(self, data: DataLaunchExample):
        return self
