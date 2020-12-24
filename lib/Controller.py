import time
from abc import ABC, abstractmethod
import clr

from lib.StopWatch import StopWatch

clr.AddReference('./lib/EngineIO')
import EngineIO


class Controller(ABC):
    def __init__(self, cycle_time=8 / 1000):
        # cycle time in milliseconds
        self.cycle_time = cycle_time

        # MemoryBit used to switch Factory I/O between edit and run mode
        self.start = EngineIO.MemoryMap.Instance.GetBit(EngineIO.MemoryMap.BitCount - 16, EngineIO.MemoryType.Output)

        # MemoryBit used to detect if Factory I/O is edit or run mode
        self.running = EngineIO.MemoryMap.Instance.GetBit(EngineIO.MemoryMap.BitCount - 16, EngineIO.MemoryType.Input)

    def switch_to_run(self):
        self.start.Value = False
        EngineIO.MemoryMap.Instance.Update()
        time.sleep(0.5)

        self.start.Value = True
        EngineIO.MemoryMap.Instance.Update()
        time.sleep(0.5)

    def run(self):

        stopwatch = StopWatch()

        # forcing a rising edge on the start MemoryBit so FACTORY I/O can detect it
        self.switch_to_run()

        stopwatch.start()

        time.sleep(self.cycle_time)

        try:
            print('Press Ctrl-C to terminate.')
            while True:
                self.update()

                if self.running.Value:
                    stopwatch.stop()

                    self.execute(int(stopwatch.elapsed_milliseconds))

                    stopwatch.restart()

                time.sleep(self.cycle_time)
        except KeyboardInterrupt:
            print('Bye')
            self.shutdown()

    def shutdown(self):
        self.start.Value = False

        EngineIO.MemoryMap.Instance.Update()
        EngineIO.MemoryMap.Instance.Dispose()

    @staticmethod
    def get_input_bit(address):
        return EngineIO.MemoryMap.Instance.GetBit(address, EngineIO.MemoryType.Input)

    @staticmethod
    def get_output_bit(address):
        return EngineIO.MemoryMap.Instance.GetBit(address, EngineIO.MemoryType.Output)

    @staticmethod
    def update():
        # update the memory map before executing the controller
        EngineIO.MemoryMap.Instance.Update()

    @abstractmethod
    def execute(self, elapsed_milliseconds):
        # implement scene execution
        pass
