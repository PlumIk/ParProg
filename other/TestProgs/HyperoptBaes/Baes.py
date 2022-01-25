from hyperopt import tpe, hp
from hyperopt import Trials
from hyperopt import fmin


def fun(x):
    print(x)
    x = x / 4
    x = x - 1
    return x


class mypar:
    m = 10
    l = list()
    iter = 0

    def __init__(self, x: int):
        self.m = x
        for i in range(self.m):
            self.l.append(i)

    def get(self):
        self.iter += 1
        if self.iter >= self.m:
            self.iter = 0
        return self.l[self.iter]


tpe_algo = tpe.suggest
tpe_trials = Trials()
space = mypar(100)
tpe_best = fmin(fn=fun, space=space.get,
                algo=tpe_algo, trials=tpe_trials,
                max_evals=100)

print(tpe_best)
