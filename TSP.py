import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import os.path as osp

class TSP(object):
    def __init__(self, solution, data, metric):
        """
        A warpper for solving TSP
        :param solution: specific solution applied
        :param data: city position list
        :param metric: metric for distance metric
        :param savepath: file save path
        """
        super(TSP, self).__init__()

        self.solution = solution
        self.city_pos_arr = np.array(data, np.float32)
        self.city_pos_xs = self.city_pos_arr[:, 0]
        self.city_pos_ys = self.city_pos_arr[:, 1]
        self.city_num = len(data)
        self.order = list(range(self.city_num))
        random.shuffle(self.order)
        self.metric_func = metric

        self.solution.init(self.order, self.eval_func)
        self.dist = self.eval_func(self.order)

    def eval_func(self, order):
        distance = 0.0
        for i in range(-1, len(order) - 1):
            idx1, idx2 = order[i], order[i + 1]
            p1, p2 = self.city_pos_arr[idx1], self.city_pos_arr[idx2]
            distance += self.metric_func(p1, p2)

        return distance

    def run(self, threshhold, savepath, save_freq=500, print_freq=1000, max_iteration=500000):
        if (savepath is not None) and (not osp.exists(savepath)):
            os.makedirs(savepath)

        iteration = 0
        dist_record = [self.dist]
        while True:
            if (iteration % save_freq == 0 or self.dist <= threshhold) and savepath is not None:
                img_name = osp.join(savepath, str(iteration)+'.png')
                self.draw(img_name)

            if self.dist <= threshhold or iteration >= max_iteration:
                break

            self.solution.run()
            dist = self.solution.get_score()
            iteration = iteration + 1

            if iteration % print_freq == 0:
                print('Distance of TSP at Iteration {}: {}'.format(iteration, dist))

            if dist < self.dist:
                self.order = self.solution.get_stat()
                self.dist = dist

            dist_record.append(self.dist)

        if savepath is None:
            self.draw()

        if savepath is not None:
            record_path = osp.join(savepath, 'dist.txt')
            with open(record_path, 'w') as fp:
                for item in dist_record:
                    fp.write(str(item)+'\r\n')

    def draw(self, img_name=None):
        plt.figure(figsize=(12, 6), facecolor='#D9D4CF')
        plt.scatter(self.city_pos_xs, self.city_pos_ys, color='#E53A40', marker='*', s=100, linewidths=3)
        for i in range(self.city_num-1):
            plt.plot([self.city_pos_xs[self.order[i]], self.city_pos_xs[self.order[i+1]]],
                     [self.city_pos_ys[self.order[i]], self.city_pos_ys[self.order[i+1]]], color='#008C9E', linewidth=2)
        plt.plot([self.city_pos_xs[self.order[self.city_num-1]], self.city_pos_xs[self.order[0]]],
                 [self.city_pos_ys[self.order[self.city_num-1]], self.city_pos_ys[self.order[0]]], color='#008C9E', linewidth=2)
        plt.axis('off')
        if img_name is not None:
            plt.savefig(img_name)
        else:
            plt.show()
        plt.close()

