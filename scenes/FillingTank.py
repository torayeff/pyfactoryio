from lib.Controller import Controller
from lib.FunctionBlocks import TOF


class SceneController(Controller):
    def __init__(self):
        super().__init__()

        self.filling_light = self.get_output_bit(0)
        self.discharging_light = self.get_output_bit(2)
        self.fill_valve = self.get_output_bit(3)
        self.discharge_valve = self.get_output_bit(4)

        self.fill_button = self.get_input_bit(0)
        self.discharge_button = self.get_input_bit(1)

        self.timer = self.get_output_int(0)

        self.tof_fill = TOF()
        self.tof_discharge = TOF()

        # initial values
        self.tof_fill.set_pt(8000)
        self.tof_discharge.set_pt(8000)

        self.fill_valve.Value = False
        self.discharge_valve.Value = False

        self.filling_light.Value = False
        self.discharging_light.Value = False

    def execute(self, elapsed_milliseconds):
        # fill
        self.tof_fill.set_in(self.fill_button.Value)

        self.fill_valve.Value = self.tof_fill.get_q()
        self.filling_light.Value = self.tof_fill.get_q()

        # discharge
        self.tof_discharge.set_in(not self.discharge_button.Value)

        self.discharge_valve.Value = self.tof_discharge.get_q()
        self.discharging_light.Value = self.tof_discharge.get_q()

        # HMI
        if self.tof_fill.get_q():
            self.timer.Value = 8 - self.tof_fill.get_et() / 1000
            print(self.timer.Value)
        else:
            self.timer.Value = 8 - self.tof_discharge.get_et() / 1000
