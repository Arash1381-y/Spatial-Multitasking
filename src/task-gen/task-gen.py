import argparse
import csv

import numpy as np

from src.config import CORE_NUMBER

# Create an ArgumentParser object
parser = argparse.ArgumentParser()
# Add arguments
parser.add_argument('-o', '--output', type=str, default='./src/tasks.csv', help='Path to output file')

parser.add_argument('-v', '--voltage', type=float, default=5, help='System Working Voltage')
parser.add_argument('-f', '--frequency', type=float, default=7e8, help='System Frequency')
parser.add_argument('-ts', '--time-scale', type=int, default=15, help='Max unit of a single task execution')
parser.add_argument('-sn', '--simple-number', required=True, type=int, help='Number of simple tasks to schedule')
parser.add_argument('-nn', '--normal-number', required=True, type=int, help='Number of normal tasks to schedule')
parser.add_argument('-cn', '--complex-number', required=True, type=int, help='Number of hard tasks to schedule')
parser.add_argument('-mp', '--max-parallel-portion', type=float, default=0.9,
                    help='Max possible parallel portion for a single task')


def formatter(f: float):
    return float(format(f, '.2f'))


def get_exe(base_exe, core_n, p):
    speed_up = 1 / ((1 - p) + p / core_n)
    return formatter(base_exe * (1.0 / speed_up))


def gen_dummy():
    # Parse arguments
    args = parser.parse_args()

    # Access parsed arguments
    output_file_path = args.output
    voltage = args.voltage
    frequency = args.frequency
    time_scale = args.time_scale
    simple_task_n = args.simple_number
    normal_task_n = args.normal_number
    complex_task_n = args.complex_number
    total_task = simple_task_n + normal_task_n + complex_task_n
    max_p = args.max_parallel_portion
    core_number = CORE_NUMBER

    interval_size = time_scale / 3  # Calculate the size of each interval
    interval_midpoints = [i * interval_size - interval_size / 2 for i in
                          range(1, 4)]  # Initialize a list to store midpoints

    # Generate random data for three normal distributions
    simple_task_dist = [formatter(f) for f in
                        np.random.normal(loc=interval_midpoints[0], scale=1, size=simple_task_n)]
    normal_task_dist = [formatter(f) for f in
                        np.random.normal(loc=interval_midpoints[1], scale=0.5, size=normal_task_n)]
    complex_task_dist = [formatter(f) for f in
                         np.random.normal(loc=interval_midpoints[0], scale=1, size=complex_task_n)]

    exec_time_sample = np.concatenate((simple_task_dist, normal_task_dist, complex_task_dist))
    np.random.shuffle(exec_time_sample)

    parallel_portion_sample = [formatter(f) for f in np.random.rand(total_task) * max_p]

    # for now, lets ignore the power and energy
    base_name = ['exe', 'power', 'energy']
    cols = ['parallel portion']
    for base in base_name:
        for i in range(core_number):
            cols.append(str(base) + "_" + str(i + 1))

    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # add cols name
        writer.writerow(cols)

        # add each task info
        for task in range(total_task):
            # gen the row
            row = [parallel_portion_sample[task], exec_time_sample[task]]
            for i in range(2, core_number + 1):
                row.append(get_exe(row[1], i, parallel_portion_sample[task]))

            # dummy power, energy
            row += [1] * 2 * core_number
            writer.writerow(row)


if __name__ == '__main__':
    gen_dummy()
