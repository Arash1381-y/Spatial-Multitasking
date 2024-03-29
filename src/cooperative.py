from scheduler import Scheduler
import argparse
from typing import List
from task import Task
import time
# Create an ArgumentParser object
parser = argparse.ArgumentParser()
# Add arguments
parser.add_argument('-ip', '--input-path', required=False, type=str, default='./tasks',
                    help='Path to input file')
parser.add_argument('-op', '--output-path', required=False, type=str, default='./cooperative.png',
                    help='Path to output file')
parser.add_argument('-c', '--cores', required=False, type=int, default=3,
                    help='cores count')

class CooperativeScheduler(Scheduler):
    def __init__(self, path: str | None = None, tasks: List[Task] | None = None, core_num: int = 1):
        super().__init__(path=path, tasks=tasks, core_num=core_num, method_name='cooperative')

    def run(self) -> None:
        """
        dedicate all available core to each tasks

        :return:
        """
        start_time = time.time_ns()
        timer = 0.0
        for index, task in enumerate(self.tasks):
            task_exe_time = task.exe_time(self.core_num)
            end_time = timer + task_exe_time

            for c in range(self.core_num):
                info = [timer, .0, self.core_num, (task.name, task.id), c, task.get_speed_up(self.core_num)/self.core_num, task.get_energy(self.core_num)/self.core_num]
                info[1] = end_time
                self.run_intervals.append(tuple(info))
            timer += task_exe_time
                
        end_time = time.time_ns()
        self.scheduling_time = (end_time - start_time)/(10**6)
        intervals = sorted(self.run_intervals, key=lambda info: info[1])
        for interval in intervals:
            self.plotter.plot_interval(int(interval[3][1]), interval[4], interval[0], interval[1], interval[3][0])
        
        return self.run_intervals
    
    def get_energy_uasage(self):
        energy = 0
        for interval in self.run_intervals:
            energy += interval[-1]
        return energy
    
    def get_make_span(self):
        make_span = 0
        make_span = max([interval[1] for interval in self.run_intervals])
        return make_span
            
    
    def plot_schedule(self):
        self.plotter.stdout_show()

    def plot_save(self, path):
        self.plotter.save_fig(path)

    def log(self, path: str | None = None):
        log: str = ""

        for interval in self.run_intervals:
            start_time: float = interval[0]
            finish_time: float = interval[1]
            log += f"From {start_time:.2f} To {finish_time:.2f}:\n"
            log += f"RUN Task {interval[3]:.2f} With {interval[2]:.2f} Cores \n"
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
    cores = args.cores
    test = CooperativeScheduler(path=path, core_num=cores)
    test.run()
    test.plot_save(save)
    test.log()