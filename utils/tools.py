import os
import os.path as osp
import imageio
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt


def generate_gif(savepath):
    img_names = os.listdir(savepath)
    img_paths = list()
    for img_name in img_names:
        if img_name.find('.png') != -1 and img_name != 'dist.png':
            img_paths.append(osp.join(savepath, img_name))
    frames = [imageio.imread(img_path) for img_path in img_paths]

    gif_path = osp.join(savepath, 'progress.gif')
    imageio.mimsave(gif_path, frames, 'GIF', duration=0.3)


def plot(savepath):
    data_path = osp.join(savepath, 'dist.txt')
    data_list = open(data_path, 'r').read().splitlines()

    x = list(range(len(data_list)))
    y = data_list

    plt.figure(figsize=(12, 8), facecolor='#D4DFE6')
    plt.suptitle('Distance Trend Over Iteration', fontsize=20, fontweight='bold')
    plt.xlabel('Iteration', fontsize=15, fontweight='bold')
    plt.ylabel('Distance Overall', fontsize=15, fontweight='bold')
    plt.plot(x, y, color='#FFBC42', linewidth=5)
    plt.savefig(osp.join(savepath, 'dist.png'))
    plt.show()



