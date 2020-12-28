from lib.Controller import Controller
from lib.FunctionBlocks import FTRIG, RTRIG
from lib.State import State


class SceneController(Controller):
    def __init__(self):
        super().__init__()

        # outputs
        self.lids_conveyor = self.get_output_bit(11)
        self.move_x = self.get_output_bit(1)
        self.move_z = self.get_output_bit(0)
        self.grab = self.get_output_bit(2)
        self.bases_conveyor = self.get_output_bit(13)
        self.clamp_lid = self.get_output_bit(19)
        self.pos_raise_lid = self.get_output_bit(18)
        self.clamp_base = self.get_output_bit(17)
        self.pos_raise_base = self.get_output_bit(16)
        self.counter = self.get_output_int(0)

        # inputs
        self.lid_at_place = self.get_input_bit(8)
        self.base_at_place = self.get_input_bit(0)
        self.part_leaving = self.get_input_bit(15)
        self.item_detected = self.get_input_bit(7)
        self.moving_z = self.get_input_bit(1)
        self.moving_x = self.get_input_bit(6)
        self.lid_clamped = self.get_input_bit(13)
        self.pos_at_limit_lids = self.get_input_bit(10)
        self.base_clamped = self.get_input_bit(12)
        self.pos_at_limit_bases = self.get_input_bit(11)

        self.ft_lid_at_place = FTRIG()
        self.ft_base_at_place = FTRIG()
        self.ft_moving_z = FTRIG()
        self.ft_moving_x = FTRIG()
        self.rt_Mxmz = RTRIG()
        self.ft_part_leaving = FTRIG()

        self.state_lids = State.State0
        self.state_bases = State.State0

        # initialize
        self.lids_conveyor.Value = False
        self.bases_conveyor.Value = True
        self.move_z.Value = False
        self.move_x.Value = False
        self.grab.Value = False
        self.clamp_lid.Value = False
        self.pos_raise_lid.Value = False
        self.clamp_base.Value = False
        self.pos_raise_base.Value = False

        self.counter.Value = 0

    def execute(self, elapsed_milliseconds):
        self.ft_lid_at_place.CLK(self.lid_at_place.Value)
        self.ft_moving_z.CLK(self.moving_z.Value)
        self.ft_moving_x.CLK(self.moving_x.Value)
        self.rt_Mxmz.CLK(self.moving_z.Value and self.moving_x.Value)

        # Lids
        if self.state_lids == State.State0:
            self.lids_conveyor.Value = True

            if self.ft_lid_at_place.get_q():
                self.state_lids = State.State1

        elif self.state_lids == State.State1:
            self.lids_conveyor.Value = False
            self.clamp_lid.Value = True

            if self.lid_clamped:
                self.state_lids = State.State2

        elif self.state_lids == State.State2:
            self.move_z.Value = True

            if self.ft_moving_z.get_q():
                self.state_lids = State.State3

        elif self.state_lids == State.State3:
            if self.item_detected.Value:
                self.state_lids = State.State4

        elif self.state_lids == State.State4:
            self.grab.Value = True
            self.move_z.Value = False
            self.clamp_lid.Value = False

            if self.ft_moving_z.get_q():
                self.state_lids = State.State5

        elif self.state_lids == State.State5:
            self.move_x.Value = True
            if self.ft_moving_x.get_q():
                self.state_lids = State.State6

        elif self.state_lids == State.State6:
            self.move_z.Value = True

            if self.ft_moving_z.get_q():
                self.state_lids = State.State7

        elif self.state_lids == State.State7:
            self.grab.Value = False
            self.move_z.Value = False

            self.state_bases = State.State2

            if self.ft_moving_z.get_q() and (not self.item_detected.Value):
                self.counter.Value += 1
                self.state_lids = State.State8

        elif self.state_lids == State.State8:
            if not self.item_detected.Value:
                self.state_lids = State.State9

        elif self.state_lids == State.State9:
            self.move_x.Value = False

            if self.ft_moving_x.get_q():
                self.state_lids = State.State0

        # bases
        self.ft_base_at_place.CLK(self.base_at_place.Value)
        self.ft_part_leaving.CLK(self.part_leaving.Value)

        if self.state_bases == State.State0:
            self.bases_conveyor.Value = True
            self.pos_raise_base.Value = False

            if self.ft_base_at_place.get_q():
                self.state_bases = State.State1

        elif self.state_bases == State.State1:
            self.bases_conveyor.Value = False
            self.clamp_base.Value = True

        elif self.state_bases == State.State2:
            self.bases_conveyor.Value = True
            self.clamp_base.Value = False
            self.pos_raise_base.Value = True

            if self.ft_part_leaving.get_q() or self.base_at_place.Value:
                self.state_bases = State.State0
