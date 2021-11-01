def input_set1() -> list:
    ret = list()
    for i in range(4, 20):
        ret.append(i * 100)
    return ret


def input_set2() -> list:
    ret = list()
    for i in range(4, 20):
        for j in all_del_50(i * 100):
            ret.append([i * 100, j])
    return ret


def cur_set() -> list:
    ret = input_set1() + input_set2()
    return ret


def all_del_50(k) -> list:
    ret = list()
    i = 50
    while i <= k // 2:
        if k % i == 0:
            ret.append(i)
        i += 50
    return ret
