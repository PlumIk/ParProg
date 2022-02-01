from Examples.conf.confexample import ConfExample
from Examples.launching.datalauchexample import DataLaunchExample
from Examples.selfsearch.datadict import DataDict
from programlaunching.programlauncher import LaunchSome
from selfsearch.searchinter import SearchInterface
from datawork.datagen.typeother.allvalues_int import AllValuesInt
from other import GlobalFunction as GFunction


class AllValuesSearch(SearchInterface):
    def __init__(self):
        super(AllValuesSearch, self).__init__()


    def work(self, conf: ConfExample) -> DataDict:

        data_dict = DataDict()

        data_list = list()
        for item in conf.get_data_set().items():
            data_list.append(AllValuesInt().gen_data(item[1].get_range()))

        print('data is', end='')
        print(data_list)
        data = conf.gen_launch()
        data.set_data_in(data_list)
        data = LaunchSome(data)
        print(data.get_data_out())
        GFunction.print_data_out(data.get_data_out())
        data_dict.add_data_from_dict(data.get_data_out())
        data_dict.print()

        return data_dict

    def step(self, data: DataLaunchExample):
        return self