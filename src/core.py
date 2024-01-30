class Core:
    def __init__(self, id, core_count):
        self.id = id
        self.core_count = core_count
        self.timer = 0.0
        self.last_task = 0
    def run_task(self, exe_time):
        self.last_task = exe_time
        self.timer += exe_time
        return self.timer
    def revert(self):
        self.timer -= self.last_task
    
    def reset(self):
        self.timer = 0