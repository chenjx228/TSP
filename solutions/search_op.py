import random

def single_swap(input):
    swap_res = input.copy()
    input_len = len(swap_res)

    idx1, idx2 = random.sample(range(input_len), 2)
    if idx1 > idx2:
        idx1, idx2 = idx2, idx1

    if idx1 == 0 and idx2 == input_len-1:
        return swap_res
    while idx1 < idx2:
        swap_res[idx1], swap_res[idx2] = swap_res[idx2], swap_res[idx1]
        idx1 += 1
        idx2 -= 1

    return swap_res


def single_swap_bilateral(input):
    swap_res = input.copy()
    input_len = len(swap_res)

    idx1, idx2 = random.sample(range(input_len), 2)
    if idx1 > idx2:
        idx1, idx2 = idx2, idx1

    if (idx1 == 0 and idx2 == input_len-1) or idx1 == idx2:
        return swap_res

    swap_res[idx1], swap_res[idx2] = swap_res[idx2], swap_res[idx1]

    return swap_res


def double_swap(input):
    swap_res = input.copy()
    input_len = len(swap_res)

    sample_idxs = random.sample(range(input_len), 4)
    sample_idxs.sort()
    idx1, idx2, idx3, idx4 = sample_idxs

    while idx1 < idx2:
        swap_res[idx1], swap_res[idx2] = swap_res[idx2], swap_res[idx1]
        idx1 += 1
        idx2 -= 1

    while idx3 < idx4:
        swap_res[idx3], swap_res[idx4] = swap_res[idx4], swap_res[idx3]
        idx3 += 1
        idx4 -= 1

    return swap_res


idx2Op = {
    0: single_swap,
    1: single_swap_bilateral,
    2: double_swap
}
