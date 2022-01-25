def data_swapper(data: list) -> list:
    if data[1] < data[0]:
        swap = data[0]
        data[0] = data[1]
        data[1] = swap
    return data
