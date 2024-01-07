import os
from random import random
import numpy as np
import random
from matplotlib import pyplot as plt


class TaskPlotter:

    def __init__(self, finish_time, n):
        """
        create a subplots for `n` tasks and max finish time of `finish_time`

        :param finish_time: max finish time of tasks
        :param n: number of tasks
        """

        self.fig, self.ax = plt.subplots()
        self.__modify_plt_style(finish_time)
        self.colors = []
        self.__set_task_colors(n)

    def plot_interval(self, task_i: int, start_time: float, finish_time):
        """
        plot an interval from `start_time` to `finish_time` which is responsible for executing
        task with id equals to `task_i`

        :param task_i: task id
        :param start_time: start time of interval
        :param finish_time: finish_time of interval
        :raise V
        :return:
        """
        if start_time > finish_time:
            raise ValueError(f"Invalid interval: start = {start_time} finish = {finish_time} ")

        self.ax.fill_between([start_time, finish_time], 0, 1, color=self.colors[task_i])
        text_x = (start_time + finish_time) / 2
        self.ax.text(text_x, 0.7, f'Task {task_i + 1}', ha='center', va='top', fontsize=8, rotation='vertical')

    def stdout_show(self):
        plt.show()

    def save_fig(self, path: str):
        if path is None:
            raise ValueError(f"path is not valid : {path}")

        plt.savefig(path)

    def __modify_plt_style(self, finish_time):
        self.ax.set_xlim(0, finish_time)
        self.ax.set_ybound(lower=0, upper=2)
        self.ax.set_ylim(0, 1)
        self.ax.tick_params(axis='x', which='both', bottom=True, top=True, direction='inout')
        self.ax.yaxis.set_tick_params(labelleft=False, which="both", left=False, right=False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        plt.subplots_adjust(bottom=0.3, )

    def __set_task_colors(self, n):
        for i in range(n):
            self.colors.append(generate_new_color(self.colors, pastel_factor=0.8))


def get_random_color(pastel_factor=0.5):
    return [(x + pastel_factor) / (1.0 + pastel_factor) for x in [random.uniform(0, 1.0) for _ in [1, 2, 3]]]


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
