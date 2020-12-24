import time


class StopWatch:
    def __init__(self):
        self.start_time = -1
        self.elapsed_milliseconds = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time == -1:
            raise Exception('StopWatch should be started first!')

        self.elapsed_milliseconds = int((time.time() - self.start_time)*1000)
        self.start_time = -1

    def restart(self):
        self.elapsed_milliseconds = 0
        self.start_time = time.time()
