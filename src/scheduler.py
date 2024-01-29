from abc import ABC, abstractmethod
from typing import List

from utils.plotter import TaskPlotter
from task import Task, read_tasks



class Scheduler(ABC):

    @abstractmethod
    def __init__(self, path: str | None, tasks: List | None, core_num: int):
        self.tasks: List[Task] = []

        if path is None and tasks is None:
            raise RuntimeError("No data is given for schedular")
        elif path is not None:
            self.tasks = read_tasks(path)
        else:
            self.tasks = tasks

        self.core_num = core_num
        self.run_intervals: List[RunInfo] = []

        # get max exe time
        max_exe_time = 0
        for task in self.tasks:
            max_exe_time += task.exe_time(core_num)

        self.plotter = TaskPlotter(max_exe_time, len(self.tasks), self.core_num)

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
