from __future__ import absolute_import
from __future__ import division

import math
import random

from .search_op import idx2Op


def _cal_expectation(delta, temp):
    # print(delta, temp)
    return math.exp(-delta / temp)


class SA(object):
    def __init__(self, op_idx, init_coeff, init_inner_time, stop_temp, alpha):
        """
        A warper of Simulated Annealing Algorithm
        :param op_idx:  operation id of local search operation
        :param init_coeff:  param for determine initial temperature
        :param base_inner_time: base inner circle times
        :param stop_temp:   temperature threshold to stop circulation
        :param alpha:   temperature descending coefficient
        """
        super(SA, self).__init__()
        self.serach_op = idx2Op[op_idx]
        self.init_coeff = init_coeff
        self.inner_time = init_inner_time
        self.stop_temp = stop_temp
        self.alpha = alpha
        self.inner_cnt = 0

    def init(self, init_stat, eval_func):
        self.stat = init_stat
        self.eval_func = eval_func
        self.score = self.eval_func(self.stat)

        self.curr_temp = self._init_temp()

    def _init_temp(self):
        test_time = 300
        init_temp = 50

        print('Start iterating for an appropriate initial temperature...')
        while True:
            cnt = 0
            for _ in range(test_time):
                tmp_stat = self.serach_op(self.stat)
                tmp_score = self.eval_func(tmp_stat)

                delta = tmp_score - self.score
                if delta < 0 or random.random() <= _cal_expectation(delta, init_temp):
                    cnt += 1

            rate = cnt * 1.0 / test_time
            if rate > self.init_coeff:
                break
            else:
                init_temp *= 1.05

        return init_temp

    def run(self):
        if self.inner_cnt >= self.inner_time:
            self.inner_time = int(self.inner_time * 1.01)
            self.inner_cnt = 0
            self.curr_temp *= self.alpha

        tmp_stat = self.serach_op(self.stat)
        tmp_score = self.eval_func(tmp_stat)

        delta = tmp_score - self.score
        if delta < 0 or random.random() <= _cal_expectation(delta, self.curr_temp):
            self.stat = tmp_stat
            self.score = tmp_score

        self.inner_cnt += 1

    def get_score(self):
        return self.score

    def get_stat(self):
        return self.stat
