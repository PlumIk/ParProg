from Examples.launching.datalauchexample import DataLaunchExample
from Examples.selfsearch.datadict import DataDict


class SearchInterface:

    def work(self, data: DataLaunchExample) -> DataDict:
        pass

    def step(self, data: DataLaunchExample):
        pass