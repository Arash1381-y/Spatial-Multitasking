import os
import pandas as pd
from typing import List, Dict

class Task:
    def __init__(self, id: int, name: str, avg_ms: Dict, min_ms: Dict, max_ms: Dict, power: Dict, energy: Dict, energy_in_window: Dict):
        self.id = id
        self.name = name
        self.avg_ms = avg_ms
        self.min_ms = min_ms
        self.max_ms = max_ms
        self.power = power
        self.energy = energy
        self.energy_in_window = energy_in_window

    def calculate_speed_up(self, core_count):
        base = self.max_ms[1]
        self.speed_up = {i : base/self.max_ms[i] for i in range(1, core_count+1)}
        
    def exe_time(self, core_num):
        return self.max_ms[core_num]

    def get_energy(self, core_num):
        return self.energy[core_num]
    
    def get_speed_up(self, core_num):
        return self.speed_up[core_num]
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.id)
        
def read_csv_files_in_directory(directory_path):
    # Get a list of all files in the specified directory
    file_list = os.listdir(directory_path)

    # Filter the list to include only CSV files
    csv_files = [file for file in file_list if file.endswith('.csv')]

    # Initialize an empty dictionary to store DataFrames
    dataframes = {}

    # Read each CSV file into a DataFrame and store it in the dictionary
    for csv_file in csv_files:
        file_path = os.path.join(directory_path, csv_file)
        dataframe = pd.read_csv(file_path)
        dataframes[csv_file] = dataframe

    return dataframes


def read_tasks(directory_path):
    tasks = []
    # Call the function and get a dictionary of DataFrames
    csv_dataframes = read_csv_files_in_directory(directory_path)

    # Now you can access individual DataFrames using their file names as keys
    index = 0
    for file_name, dataframe in csv_dataframes.items():
        # print(f"Data from file '{file_name}':")
        # print(dataframe)
        task = Task(
            id = index,
            name = file_name[:-4],
            avg_ms = dataframe.set_index('SM')['Average(ms)'].to_dict(),
            min_ms = dataframe.set_index('SM')['Min(ms)'].to_dict(),
            max_ms = dataframe.set_index('SM')['Max(ms)'].to_dict(),
            power = dataframe.set_index('SM')['Power(W)'].to_dict(),
            energy = dataframe.set_index('SM')['energy'].to_dict(),
            energy_in_window = dataframe.set_index('SM')['energy_in_window'].to_dict()
        )
        index+=1
        tasks.append(task)

    return tasks

