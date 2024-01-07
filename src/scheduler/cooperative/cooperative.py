from typing import List

from src.scheduler.Schedular import Schedular, RunInfo
from src.utils.task import Task, read_tasks


class Cooperative_Scheduler(Schedular):
    def __init__(self, path: str | None = None, tasks: List[Task] | None = None):
        super().__init__(path=path, tasks=tasks)

    def run(self) -> None:
        """
        dedicate all available core to each tasks

        :return:
        """

        timer = 0.0

        for index, task in enumerate(self.tasks):
            info = [timer, .0, self.core_num, index + 1]
            task_exe_time = task.exe_time(self.core_num)
            self.plotter.plot_task(index, timer, timer + task_exe_time)
            timer += task_exe_time
            info[1] = timer
            self.run_intervals.append(tuple(info))

    def plot_schedule(self):
        self.plotter.show()

    def log(self, path: str | None = None):
        log: str = ""

        for interval in self.run_intervals:
            start_time: float = interval[0]
            finish_time: float = interval[1]
            log += f"From {start_time} To {finish_time}:\n"
            log += f"RUN Task {interval[3]} With {interval[2]} Cores \n"
            log += ("-" * 20 + "\n")

        if path is None:
            print(log)


if __name__ == '__main__':
    test = Cooperative_Scheduler(path="../../task-gen/tasks.csv")
    test.run()
    test.plot_schedule()
    test.log()
