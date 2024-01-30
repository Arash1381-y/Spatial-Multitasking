import os
from random import random
import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib.axes import Axes


class ScatPlotter:
    def __init__(self):
        self.figure, self.ax = plt.subplots()
        self.legend_labels = []

    def plot(self, x, y, legend):
        self.ax.plot(x, y, '-o', label=legend)



        self.legend_labels.append(legend)

    def set_axes_labels(self, xlabel, ylabel):
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def set_axes_limits(self, xlim=None, ylim=None):
        if xlim:
            self.ax.set_xlim(xlim)
        if ylim:
            self.ax.set_ylim(ylim)

    def set_title(self, title):
        self.ax.set_title(title)

    def set_grid(self, show_grid=True):
        self.ax.grid(show_grid)

    def save_plot(self, filename='plot.png', legend_loc='upper left'):
        self.ax.legend(self.legend_labels, loc='upper left', bbox_to_anchor=(0.8,0.8))
        self.set_grid()
        self.figure.savefig(filename)
        plt.close()
    
class TaskPlotter:

    def __init__(self, finish_time, n, c, title):
        """
        create a subplots for `n` tasks and max finish time of `finish_time`

        :param c: number of cores
        :param finish_time: max finish time of tasks
        :param n: number of tasks
        """

        self.fig, self.ax = plt.subplots(nrows=c)
        if type(self.ax) is Axes:
            self.ax = [self.ax]
        self.__modify_plt_style(finish_time, title)
        self.colors = []
        self.__set_task_colors(8)

    def plot_interval(self, task_i: int, core_i: int, start_time: float, finish_time, task_name):
        """
        plot an interval from `start_time` to `finish_time` which is responsible for executing
        task with id equals to `task_i`

        :param task_i: task id
        :param core_i: core id
        :param start_time: start time of interval
        :param finish_time: finish_time of interval
        :raise V
        :return:
        """
        if start_time > finish_time:
            raise ValueError(f"Invalid interval: start = {start_time} finish = {finish_time} ")

        ax = self.ax[core_i]
        ax.fill_between([start_time, finish_time], 0, 1, color=self.colors[task_i])
        text_x = (start_time + finish_time) / 2
        ax.text(text_x, 0.5, f'{task_name}', ha='center', va='top', fontsize=5, rotation='horizontal')

        updated_ticks = np.append(self.ax[-1].get_xticks(), [start_time, finish_time])
        updated_labels = np.append(self.ax[-1].get_xticklabels(), [start_time, finish_time])
        self.ax[-1].set_xticks(updated_ticks)
        self.ax[-1].set_xticklabels(updated_labels, rotation='vertical')

    def stdout_show(self):
        plt.show()

    def save_fig(self, path: str):
        if path is None:
            raise ValueError(f"path is not valid : {path}")

        plt.savefig(path)
        plt.close()

    def __modify_plt_style(self, finish_time, title):

        for index, ax in enumerate(self.ax):
            ax.set_xlim(0, finish_time)
            ax.set_ybound(lower=0, upper=2)
            ax.set_ylim(0, 1)
            ax.tick_params(axis='x', bottom=False, top=False, direction='inout')
            ax.set_xticklabels([], fontsize=6)
            ax.yaxis.set_tick_params(labelleft=False, which="both", left=False, right=False)
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.set_ylabel(f"C {index + 1}", fontsize=10)

        self.ax[-1].tick_params(axis='x', bottom=True, top=False, direction='inout')
        self.ax[-1].set_xticks([])
        self.ax[-1].set_xticklabels([])

        plt.xlabel('Time', fontsize=18)
        plt.suptitle(title)

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
