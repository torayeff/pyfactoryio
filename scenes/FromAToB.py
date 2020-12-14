from lib.Controller import Controller
import clr
clr.AddReference('./lib/EngineIO')
import EngineIO


class SceneController(Controller):
    def __init__(self):
        super().__init__()
        self.conveyor = EngineIO.MemoryMap.Instance.GetBit(0, EngineIO.MemoryType.Output)
        self.sensor = EngineIO.MemoryMap.Instance.GetBit(1, EngineIO.MemoryType.Input)
        self.conveyor.Value = False

    def execute(self, elapsed_milliseconds):
        self.conveyor.Value = self.sensor.Value
