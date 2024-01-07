from abc import ABC, abstractmethod
from typing import List

from scheduler.utils.plotter import TaskPlotter
from scheduler.utils.task import Task, read_tasks

RunInfo = (float, float, int, int)


class Schedular(ABC):

    @abstractmethod
    def __init__(self, path: str | None, tasks: List | None):
        self.tasks: List[Task] = []

        if path is None and tasks is None:
            raise RuntimeError("No data is given for schedular")
        elif path is not None:
            self.tasks = read_tasks(path)
        else:
            self.tasks = tasks

        self.core_num = len(self.tasks[0].execution_time)
        self.run_intervals = [RunInfo]

        # get max exe time
        max_exe_time = 0
        for task in self.tasks:
            max_exe_time += task.execution_time[0]

        self.plotter = TaskPlotter(max_exe_time, len(self.tasks))

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def plot_schedule(self):
        pass

    @abstractmethod
    def plot_save(self, path):
        pass

    @abstractmethod
    def log(self, path: str | None = None):
        pass
