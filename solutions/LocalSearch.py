from __future__ import absolute_import
from __future__ import division

from .search_op import idx2Op

class LocalSearch(object):
    def __init__(self, op_idx):
        super(LocalSearch, self).__init__()
        self.serach_op = idx2Op[op_idx]

    def init(self, init_stat, eval_func):
        self.stat = init_stat
        self.eval_func = eval_func
        self.score = self.eval_func(self.stat)

    def run(self):
        tmp_stat = self.serach_op(self.stat)
        tmp_score = self.eval_func(tmp_stat)
        if tmp_score < self.score:
            self.stat = tmp_stat
            self.score = tmp_score

    def get_score(self):
        return self.score

    def get_stat(self):
        return self.stat

class VariableLocalSearch(object):
    def __init__(self, op_idx1, op_idx2, keep_invariant, keep_invariant_max):
        super(VariableLocalSearch, self).__init__()
        self.op_idx1, self.op_idx2 = op_idx1, op_idx2
        self.search_op = idx2Op[self.op_idx1]
        self.keep_invariant = keep_invariant
        self.keep_invariant_max = keep_invariant_max
        self.keep_invariant_cnt = 0

    def init(self, init_stat, eval_func):
        self.stat = init_stat
        self.eval_func = eval_func
        self.score = self.eval_func(self.stat)

    def run(self):
        if self.keep_invariant_cnt > self.keep_invariant:
            self.search_op = idx2Op[self.op_idx2]
        if self.keep_invariant_cnt > self.keep_invariant_max:
            self.search_op = idx2Op[self.op_idx1]

        tmp_stat = self.search_op(self.stat)
        tmp_score = self.eval_func(tmp_stat)
        if tmp_score < self.score:
            self.stat = tmp_stat
            self.score = tmp_score
            self.keep_invariant_cnt = 0

        self.keep_invariant_cnt += 1

    def get_score(self):
        return self.score

    def get_stat(self):
        return self.stat
