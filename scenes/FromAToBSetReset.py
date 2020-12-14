from lib.Controller import Controller


class SceneController(Controller):
    def __init__(self):
        super().__init__()

        self.conveyor = self.get_output_bit(0)
        self.conveyor.Value = False

        self.sensor_A = self.get_input_bit(0)
        self.sensor_B = self.get_input_bit(1)

    def execute(self, elapsed_milliseconds):
        if not self.sensor_A.Value:
            self.conveyor.Value = True

        if not self.sensor_B.Value:
            self.conveyor.Value = False
