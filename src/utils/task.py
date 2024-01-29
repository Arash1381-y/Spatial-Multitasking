import csv
import os
from typing import List


class Task:
    def __init__(self, N: int, *data):
        """
        initialize a task based on a given data
        :param N: number of cores (data cols)
        :param data: exec, power and energy estimations of the task
        :raise ValueError: if data len is not matched with N
        """
        err = ValueError("insufficient data!")

        if len(data) % (N * 3) != 0:
            raise err

        try:
            self.execution_time: List[float] = list(map(float, data[:N]))
            self.power: List[float] = list(map(float, data[N: 2 * N]))
            self.energy: List[float] = list(map(float, data[N * 2: N * 3]))
        except ValueError:
            raise err

    def exe_time(self, core_num):
        return self.execution_time[core_num - 1]


def read_tasks(path: str):
    """
    read csv and create tasks based on it

    :param path: path of csv
    :return: tasks
    """

    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)

        # count number of cols
        N = 0
        num_cols = len(next(reader))
        if (num_cols - 1) % 3 != 0:
            raise ValueError("invalid data")
        else:
            N = int((num_cols - 1) / 3)

        tasks = []
        for row in reader:
            tasks.append(
                Task(N, *row[1:])
            )

        return tasks
