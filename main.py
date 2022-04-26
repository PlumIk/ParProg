import json
import sys

from Examples.conf.confexample import ConfExample
from conf.confcreator import start_work
from preparation.preparationforlaunch import preparation

if __name__ == "__main__":
    print("I Work1")
    if len(sys.argv) == 2:
        conf = ConfExample()
        with open(sys.argv[1], "r") as read_file:
            conf.encode_me(json.load(read_file))
        preparation(conf)
    else:
        conf = start_work()
        print("Valid: " + str(conf.get_valid()))
        preparation(conf)

