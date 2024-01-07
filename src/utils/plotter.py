from random import random

import numpy as np
from matplotlib import pyplot as plt

import random


def get_random_color(pastel_factor=0.5):
    return [(x + pastel_factor) / (1.0 + pastel_factor) for x in [random.uniform(0, 1.0) for i in [1, 2, 3]]]


def color_distance(c1, c2):
    return sum([abs(x[0] - x[1]) for x in zip(c1, c2)])


def generate_new_color(existing_colors, pastel_factor=0.5):
    max_distance = None
    best_color = None
    for i in range(0, 100):
        color = get_random_color(pastel_factor=pastel_factor)
        if not existing_colors:
            return color
        best_distance = min([color_distance(color, c) for c in existing_colors])
        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color
    return best_color


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

        self.colors = []
        for i in range(n):
            self.colors.append(generate_new_color(self.colors, pastel_factor=0.8))

    def plot_task(self, task_i, st, ft):
        self.ax.fill_between([st, ft], 0, 1, color=self.colors[task_i])
        # Add text below the rectangle with the task index
        text_x = (st + ft) / 2  # Calculate the x-position for the text
        self.ax.text(text_x, 0.7, f'Task {task_i}', ha='center', va='top', fontsize=8, rotation='vertical')

    def show(self):
        plt.show()


if __name__ == '__main__':
    p = TaskPlotter(10, 3)
    p.plot_task(task_i=0, st=2, ft=4)
    p.plot_task(task_i=1, st=5, ft=6)
    p.plot_task(task_i=2, st=7, ft=9)
    plt.show()
