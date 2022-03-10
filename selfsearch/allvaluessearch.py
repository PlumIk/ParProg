from Examples.conf.confexample import ConfExample
from Examples.selfsearch.datadict import DataDict
from datawork.datagen.typeother.allvalues_int import AllValuesInt
from programlaunching.programlauncher import LaunchSome


class AllValuesSearch:
    def __init__(self):
        self._data_dict = DataDict()
        print('Start searching by use all parameters')

    def work(self, conf: ConfExample) -> DataDict:

        data_list = list()

        for one in conf.get_data_set():
            data_list.append(AllValuesInt().gen_data(one))

        data = conf.gen_launch()
        data.set_data_in(data_list)
        data = LaunchSome(data)
        self._data_dict.add_data_from_list(data.get_data_out())
        self._data_dict.print()

        return self._data_dict
