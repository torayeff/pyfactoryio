from lib.Controller import Controller


class SceneController(Controller):
    def __init__(self):
        super().__init__()
        self.conveyor = self.get_output_bit(0)
        self.sensor = self.get_input_bit(1)
        self.conveyor.Value = False

    def execute(self, elapsed_milliseconds):
        self.conveyor.Value = self.sensor.Value
