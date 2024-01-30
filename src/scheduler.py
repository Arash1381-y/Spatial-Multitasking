from abc import ABC, abstractmethod
from typing import List

from utils.plotter import TaskPlotter
from task import Task, read_tasks



class Scheduler(ABC):

    @abstractmethod
    def __init__(self, path: str | None, tasks: List | None, core_num: int, method_name: str):
        self.tasks: List[Task] = []
        self.scheduling_time = 0.0

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
            max_exe_time += task.exe_time(1)

        self.plotter = TaskPlotter(max_exe_time, len(self.tasks), self.core_num, method_name)

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

    def get_make_span(self):
        make_span = 0
        make_span = max([interval[1] for interval in self.run_intervals])
        return make_span
    def get_scheduling_time(self):
        return self.scheduling_time