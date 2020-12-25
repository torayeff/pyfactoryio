from lib.Controller import Controller
from lib.FunctionBlocks import RTRIG, FTRIG
from lib.State import State


class SceneController(Controller):
    def __init__(self):
        super().__init__()

        # output bits
        self.buffer_conveyor = self.get_output_bit(0)
        self.entry_conveyor = self.get_output_bit(1)

        # input bits
        self.at_entry = self.get_input_bit(0)
        self.at_exit = self.get_input_bit(1)
        self.item_ready = self.get_input_bit(2)

        # states
        self.watch_state = State.State0
        self.loading_state = State.State0
        self.unloading_state = State.State0

        self.loading = False
        self.unloading = False

        self.counter = 0

        # triggers
        self.rt_at_entry = RTRIG()
        self.ft_at_entry = FTRIG()
        self.ft_at_exit = FTRIG()

        self.entry_conveyor.Value = False
        self.buffer_conveyor.Value = False

    def execute(self, elapsed_milliseconds):
        self.rt_at_entry.CLK(not self.at_entry.Value)
        self.ft_at_entry.CLK(not self.at_entry.Value)
        self.ft_at_exit.CLK(not self.at_exit.Value)

        # master controller
        if self.watch_state == State.State0:
            self.loading = True
            self.unloading = False

            if self.counter == 3:
                self.watch_state = State.State1

        elif self.watch_state == State.State1:
            self.loading = False
            self.unloading = True

            if self.counter == 0:
                self.watch_state = State.State0

        # loading controller
        if self.loading:
            if self.loading_state == State.State0:
                self.entry_conveyor.Value = True
                self.buffer_conveyor.Value = False

                if (not self.item_ready.Value) or (not self.at_entry.Value):
                    self.loading_state = State.State1

            elif self.loading_state == State.State1:
                self.entry_conveyor.Value = True
                self.buffer_conveyor.Value = False

                if self.rt_at_entry.get_q():
                    self.loading_state = State.State2

            elif self.loading_state == State.State2:
                self.entry_conveyor.Value = True
                self.buffer_conveyor.Value = True

                if self.ft_at_entry.get_q():
                    self.loading_state = State.State3

            elif self.loading_state == State.State3:
                self.counter += 1
                self.loading_state = State.State0

        # unloading controller
        if self.unloading:
            if self.unloading_state == State.State0:
                self.entry_conveyor.Value = False
                self.buffer_conveyor.Value = True

                if self.ft_at_exit.get_q():
                    self.unloading_state = State.State1

            elif self.unloading_state == State.State1:
                self.counter -= 1
                self.unloading_state = State.State0
