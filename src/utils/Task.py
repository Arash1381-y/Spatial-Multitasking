from typing import List


class Task:
    def __init__(self, N: int, *data):
        """
        initialize a task based on a given data

        :param N: number of cores (data cols)
        :param data: exec, power and energy estimations of the task

        :raise ValueError: if data len is not matched with N
        """
        err = ValueError("insufficient data!")

        if len(data) % (N * 3) != 0:
            raise err

        try:
            self.execution_time: List[float] = list(map(float, data[:N]))
            self.power: List[float] = list(map(float, data[N: 2 * N]))
            self.energy: List[float] = list(map(float, data[N * 2: N * 3]))
        except ValueError:
            raise err
