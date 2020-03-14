import os.path as osp


def data_reader(path):
    if not osp.exists(path):
        raise Exception('Target File Not Exist.')

    data = open(path, 'r').read().splitlines()
    data_list = list()
    for item in data:
        splits = item.split()
        pos_x = float(splits[1])
        pos_y = float(splits[2])

        data_list.append((pos_x, pos_y))

    return data_list
