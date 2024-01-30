from itertools import combinations
from cooperative import CooperativeScheduler
from best import BestScheduler
from profile_ import ProfileScheduler
from task import Task, read_tasks
from core import Core
from typing import List
from utils.plotter import ScatPlotter
import argparse


# Create an ArgumentParser object
parser = argparse.ArgumentParser()
# Add arguments
parser.add_argument('-ip', '--input-path', required=False, type=str, default='./test/tasks',
                    help='Path to input file')
parser.add_argument('-op', '--output-path', required=False, type=str, default='./outputs',
                    help='Path to output file')
parser.add_argument('-c', '--cores', required=False, type=int, default=3,
                    help='cores count')


def get_n_member_combinations(input_list, n):
    return list(list(item) for item in combinations(input_list, n))


def tasks_to_str(tasks, alg, cores):
    # print(tasks)
    length = len(tasks)
    name = f"/scheduling/{cores}/{cores}_{length}_{alg}"    
    for task in tasks:
        name += f"_{task.name}"
    name += f".png"
    return name


def evaluate_alg(tasks_combs, core_num, save_path, alg_func):
    energy_sum = 0
    make_span_avg = 0
    scheduling_time_avg = 0
    for item in tasks_combs:
        data = alg_func(item, core_num, save_path)
        energy_sum += data[0]
        make_span_avg += data[1]
        scheduling_time_avg += data[2]
    make_span_avg /= len(tasks_combs)
    scheduling_time_avg /= len(tasks_combs)
    energy_avg = energy_sum / len(tasks_combs)
    return energy_avg, make_span_avg, scheduling_time_avg

def coop_schedule(tasks, core_num, save_path):
    coop = CooperativeScheduler(tasks=tasks, core_num=core_num)
    coop.run()
    name = tasks_to_str(tasks, 'coop', core_num)
    coop.plot_save(save_path + f"{name}")
    return coop.get_energy_uasage(), coop.get_make_span(), coop.get_scheduling_time()

def best_schedule(tasks, core_num, save_path):
    cores = [Core(i, core_num) for i in range(core_num)]
    best = BestScheduler(tasks=tasks, core_num=core_num, cores=cores)
    best_data = best.run()
    name = tasks_to_str(tasks, 'best', core_num)

    best.plot_save(save_path + f"{name}")
    return best.get_energy_uasage(), best.get_make_span(), best.get_scheduling_time()

def profile_schedule(tasks, core_num, save_path):
    cores = [Core(i, core_num) for i in range(core_num)]
    profile = ProfileScheduler(tasks=tasks, core_num=core_num, cores=cores)    
    profile.run()
    name = tasks_to_str(tasks, 'profile', core_num)
    profile.plot_save(save_path + f"{name}")
    return profile.get_energy_uasage(), profile.get_make_span(), profile.get_scheduling_time()


def main():
    args = parser.parse_args()
    in_path = args.input_path
    save_path = args.output_path
    cores = args.cores
    tasks = read_tasks(in_path)
    algs = {'cooperative' : coop_schedule, 'profile': profile_schedule, 'best': best_schedule}
    energy_data = {'cooperative':[], 'profile':[], 'best':[]}
    avg_speedup_data = {'cooperative':[], 'profile':[], 'best':[]}
    avg_scheduling_time_data = {'cooperative':[], 'profile':[], 'best':[]}
    # 2 member:
    task_count = [2, 3, 4]
    for count in task_count: 
        combinations = get_n_member_combinations(tasks, count)
        for item in algs:
            energy_sum, make_span, scheduling_time = evaluate_alg(combinations, cores, save_path, algs[item])
            energy_data[item].append(energy_sum)
            avg_speedup_data[item].append(make_span)
            avg_scheduling_time_data[item].append(scheduling_time)
    
    energy_plotter = ScatPlotter()
    for data in energy_data:
        energy_plotter.plot(task_count, energy_data[data], legend=data)
    energy_plotter.set_axes_labels("Task Count", "Energy Usage")
    energy_plotter.save_plot(save_path+f"/{cores}_energy_plot.png")
    
    base = 'cooperative'
    speedup_plotter = ScatPlotter()
    for data in avg_speedup_data:
        result = [y/x for x, y in zip(avg_speedup_data[data], avg_speedup_data[base])]    
        speedup_plotter.plot(task_count, result, legend=data)
    speedup_plotter.set_axes_labels("Task Count", "Average Speedup")
    speedup_plotter.save_plot(save_path+f"/{cores}_avg_speedup_plot.png")
    
    speedup_plotter = ScatPlotter()
    for data in avg_scheduling_time_data:
        speedup_plotter.plot(task_count, avg_scheduling_time_data[data], legend=data)
    speedup_plotter.set_axes_labels("Task Count", "Avg Scheduling Time(ms)")
    speedup_plotter.save_plot(save_path+f"/{cores}_scheduling_time_plot.png")



if __name__ == "__main__":
    main()