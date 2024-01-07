from random import random

import numpy as np
from matplotlib import pyplot as plt


def generate_random_hex_color():
    return '#' + ''.join([np.random.choice('0123456789ABCDEF') for _ in range(6)])


def get_cmap(n, name='hsv'):
    """Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name."""
    return plt.cm.get_cmap(name, n)


class TaskPlotter:

    def __init__(self, finish_time, n):
        default_figsize = plt.rcParams.get('figure.figsize')
        default_figsize[1] /= 4
        fig, ax = plt.subplots()
        ax.set_xlim(0, finish_time)
        self.fig = fig
        self.ax = ax
        self.ax.set_ybound(lower=0, upper=2)
        ax.set_ylim(0, 1)
        ax.tick_params(axis='x', which='both', bottom=True, top=True, direction='inout')
        ax.yaxis.set_tick_params(labelleft=False, which="both", left=False, right=False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        self.color_mapper = get_cmap(n + 1)
        plt.subplots_adjust(bottom=0.3, )

    def add_task(self, task_i, st, ft):
        self.ax.fill_between([st, ft], 0, 1, color=self.color_mapper(task_i))


if __name__ == '__main__':
    p = TaskPlotter(10, 3)
    p.add_task(task_i=0, st=2, ft=4)
    p.add_task(task_i=1, st=5, ft=6)
    p.add_task(task_i=2, st=7, ft=9)
    plt.show()
