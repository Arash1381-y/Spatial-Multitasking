from scheduler import Scheduler
import argparse
from typing import List, Tuple
from task import Task
from core import Core
import sys
# Create an ArgumentParser object
parser = argparse.ArgumentParser()
# Add arguments
parser.add_argument('-ip', '--input-path', required=False, type=str, default='./test',
                    help='Path to input file')
parser.add_argument('-op', '--output-path', required=False, type=str, default='./best.png',
                    help='Path to output file')
parser.add_argument('-c', '--cores', required=False, type=int, default=3,
                    help='cores count')

        
        
class BestScheduler(Scheduler):
    def __init__(self, path: str | None = None, tasks: List[Task] | None = None, core_num: int = 1, cores: List[Core] | None = None):
        super().__init__(path=path, tasks=tasks, core_num=core_num, method_name='best')
        self.cores = cores
    
    def get_k_idle_cores(self, k: int) -> List[Core]:
        sorted_cores = sorted(self.cores, key=lambda core: core.timer)
        return sorted_cores[:k]

    
    def run(self) -> None:
        """
        find best permutation


        :return:
        """
        self.run_intervals = self.find_best_scheduling(self.tasks, True)
        intervals = sorted(self.run_intervals, key=lambda info: info[1])

        for interval in intervals:
            self.plotter.plot_interval(int(interval[3][1]), interval[4], interval[0], interval[1], interval[3][0])
        
    
    
    def get_best_intervals(self, intervals1: List[Tuple], intervals2: List[Tuple]):
            if not intervals1:
                return intervals2
            if not intervals2:
                return intervals1
            
            one = max([item[1] for item in intervals1])
            two = max([item[1] for item in intervals2])
            if one == two:
                energy_one = sum(item[-1] for item in intervals1)
                energy_two = sum(item[-1] for item in intervals2)
                if energy_one < energy_two:
                    return intervals1
                elif energy_two < energy_one:
                    return intervals2
                else:
                    # TODO compare powers
                    pass
            
            if one < two:
                return intervals1
            return intervals2  

    def find_best_scheduling(self, tasks: List[Task], flag: bool) -> List[Tuple]:
        if not tasks:
            return [] 
        timer = 0.0
        run_intervals = []
        for index, task in enumerate(tasks):
            for i in range(1, self.core_num + 1):
                cores_to_use = self.get_k_idle_cores(i)
                intervals_on_i_cores = self.schedule_with_i_cores(task, cores_to_use)
                intervals = self.find_best_scheduling(tasks[:index] + tasks[index+1:], False)
                intervals += intervals_on_i_cores

                run_intervals = self.get_best_intervals(run_intervals, intervals)
                
                if flag:
                    # print(tasks[index].name)
                    # self.log_intervals(intervals)
                    # print("---------------- next round -----------")
                    self.reset_cores(self.cores)
                else:
                    self.revert_cores(task, cores_to_use)

            # if flag:
            #         print(index, tasks[index].name)
            #         self.log_intervals(intervals)
            #         print("---------------- next round -----------")
        # print(f"alive")

        return run_intervals        
                
            
    def schedule_with_i_cores(self, task: Task, cores: List[Core]) -> List[Tuple]:
        run_intervals = []
        for core in cores:
            info = [core.timer, .0, len(cores), (task.name, task.id), core.id, task.get_energy(len(cores))/len(cores)]
            info[1] = core.run_task(task.exe_time(len(cores)))
            run_intervals.append(tuple(info))
            
        return run_intervals
    
    def revert_cores(self, task: Task, cores: List[Core]) -> None:
        for core in cores:
            core.timer -= task.exe_time(len(cores))
    
    def reset_cores(self, cores : List[Core]) -> None:
        for core in cores:
            core.reset()
        
    def log_intervals(self, intervals, path: str | None = None):
        intervals = sorted(intervals, key=lambda info: info[1])
        log: str = ""

        for interval in intervals:
            start_time: float = interval[0]
            finish_time: float = interval[1]
            log += f"From {start_time:.2f} To {finish_time:.2f}:\n"
            log += f"RUN Task {interval[3]} With {interval[2]:.2f} Cores: Core id {interval[4]} \n"
            log += ("-" * 20 + "\n")

        if path is None:
            print(log)
        else:
            with open(path, 'w') as f:
                f.write(log)

    def plot_schedule(self):
        self.plotter.stdout_show()

    def plot_save(self, path):
        self.plotter.save_fig(path)

    def log(self, path: str | None = None):
        intervals = sorted(self.run_intervals, key=lambda info: info[1])
        log: str = ""

        for interval in intervals:
            start_time: float = interval[0]
            finish_time: float = interval[1]
            log += f"From {start_time:.2f} To {finish_time:.2f}:\n"
            log += f"RUN Task {interval[3][0]}({interval[3][1]}) With {interval[2]:.2f} Cores: Core id {interval[4]} \n"
            log += ("-" * 20 + "\n")

        if path is None:
            print(log)
        else:
            with open(path, 'w') as f:
                f.write(log)
                
if __name__ == '__main__':
    sys.setrecursionlimit(1000000)
    args = parser.parse_args()
    path = args.input_path
    save = args.output_path
    core_num = args.cores
    cores = [Core(i, core_num) for i in range(core_num)]
    test = BestScheduler(path=path, core_num=core_num, cores=cores)
    test.run()
    test.plot_save(save)
    test.log()