from scheduler import Scheduler
import argparse
from typing import List
from task import Task
from core import Core
import time
# Create an ArgumentParser object
parser = argparse.ArgumentParser()
# Add arguments
parser.add_argument('-ip', '--input-path', required=False, type=str, default='./test',
                    help='Path to input file')
parser.add_argument('-op', '--output-path', required=False, type=str, default='./profile.png',
                    help='Path to output file')
parser.add_argument('-c', '--cores', required=False, type=int, default=3,
                    help='cores count')



class ProfileScheduler(Scheduler):
    def __init__(self, path: str | None = None, tasks: List[Task] | None = None, core_num: int = 1, cores: List[Core] | None = None):
        super().__init__(path=path, tasks=tasks, core_num=core_num, method_name='Profile')
        self.cores = cores
        for task in self.tasks:
            task.calculate_speed_up(self.core_num)

    def get_free_cores(self) -> List[Core]:
        cores = sorted(self.cores, key=lambda c: c.timer)
        c = cores[0]
        free_cores = []
        for item in cores:
            if item.timer <= c.timer:  
                free_cores.append(c)
        
        return free_cores      


    def run(self) -> None:
        """
        maximize target function

        :return:
        """
        start_time = time.time_ns()

        self.scheduling_time = 0.0
        tasks = self.tasks[:]
        free_cores = self.cores
        value, config = self.maximize_profiles(free_cores, tasks, len(free_cores))
        
        for task in config:
            assigned_cores_count = len(config[task])
            for c in config[task]:
                info = [c.timer, .0, assigned_cores_count, (task.name, task.id) ,c.id, value, task.get_speed_up(assigned_cores_count)/assigned_cores_count, task.get_energy(assigned_cores_count)/assigned_cores_count]
                info[1] = c.run_task(task.exe_time(assigned_cores_count))
                self.run_intervals.append(tuple(info))
        
            tasks.remove(task)
        
        while tasks:
            free_cores = self.get_free_cores()
            value, config = self.maximize_profiles(free_cores, tasks, len(free_cores))
            for task in config:
                assigned_cores_count = len(config[task])
                for c in config[task]:
                    info = [c.timer, .0, assigned_cores_count, (task.name, task.id), c.id, value, task.get_speed_up(assigned_cores_count)/assigned_cores_count, task.get_energy(assigned_cores_count)/assigned_cores_count]
                    info[1] = c.run_task(task.exe_time(assigned_cores_count))
                    self.run_intervals.append(tuple(info))
            tasks.remove(task)
        
        end_time = time.time_ns()
        self.scheduling_time = (end_time - start_time)/10**6
        intervals = sorted(self.run_intervals, key=lambda info: info[1])
        for interval in intervals:
            self.plotter.plot_interval(int(interval[3][1]), interval[4], interval[0], interval[1], interval[3][0])
        
        
        
    def maximize_profiles(self, free_cores: List[Core], tasks: List[Task], N:int):
        if not tasks or not free_cores:
            return 0, {}
        best = 0
        best_config = {}
        for index, task in enumerate(tasks):
            sum = 0
            for i in range(1, len(free_cores) + 1):
                sum = 0
                sum += ((task.get_speed_up(i))**(1/N))
                base_config = {task: free_cores[:i]}
                ans, config = self.maximize_profiles(free_cores[i:], tasks[:index] + tasks[index+1:], N)
                
                sum += ans
                
                config = config | base_config

                if sum > best:
                    best = sum
                    best_config = config
                    
        return best, best_config
    
    def get_energy_uasage(self):
        energy = 0
        for interval in self.run_intervals:
            energy += interval[-1]
        return energy
    
    def get_average_speed_up(self):
        speed_up = 0
        for interval in self.run_intervals:
            speed_up += interval[-2]
        
        return speed_up/len(self.tasks) 

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
            log += f"RUN Task {interval[3][0]}({interval[3][1]}) With {interval[2]:.2f} Cores: Core id {interval[4]} \n"
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
    core_num = args.cores
    cores = [Core(i, core_num) for i in range(core_num)]
    test = ProfileScheduler(path=path, core_num=core_num, cores=cores)    
    test.run()
    test.plot_save(save)
    test.log()