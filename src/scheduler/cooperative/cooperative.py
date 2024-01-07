import argparse
from typing import List

from src.scheduler.schedular import Schedular
from src.scheduler.utils.task import Task

# Create an ArgumentParser object
parser = argparse.ArgumentParser()
# Add arguments
parser.add_argument('-ip', '--input-path', required=False, type=str, default='./src/tasks.csv',
                    help='Path to input file')
parser.add_argument('-op', '--output-path', required=False, type=str, default='./src/cooperative.png',
                    help='Path to output file')


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
            self.plotter.plot_interval(index, timer, timer + task_exe_time)
            timer += task_exe_time
            info[1] = timer
            self.run_intervals.append(tuple(info))

    def plot_schedule(self):
        self.plotter.stdout_show()

    def plot_save(self, path):
        self.plotter.save_fig(path)

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
        else:
            with open(path, 'w') as f:
                f.write(log)


if __name__ == '__main__':
    args = parser.parse_args()
    path = args.input_path
    save = args.output_path
    test = Cooperative_Scheduler(path=path)
    test.run()
    test.plot_save(save)
    test.log()
