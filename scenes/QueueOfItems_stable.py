from lib.Controller import Controller
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

        self.entry_conveyor.Value = False
        self.buffer_conveyor.Value = False

        # these variables are used for counting
        self.prev_entry = True
        self.prev_exit = True

        self.loading = True
        self.unloading = False

    def execute(self, elapsed_milliseconds):

        if self.loading:
            self.entry_conveyor.Value = True

        if self.unloading:
            self.entry_conveyor.Value = False
            self.buffer_conveyor.Value = True

        # run buffer conveyor whenever object is detected
        if not self.at_entry.Value:
            self.buffer_conveyor.Value = True

        if self.at_entry.Value and (not self.unloading):
            self.buffer_conveyor.Value = False

        # change from loading to unloading
        if self.counter == 3:
            self.loading = False
            self.unloading = True

        # count items in the buffer area
        if (not self.prev_entry) and self.at_entry.Value:
            self.counter += 1

        # count items at exit area
        if (not self.prev_exit) and self.at_exit.Value:
            self.counter -= 1

            # change states when buffer is unloaded
            if self.counter == 0:
                self.loading = True
                self.unloading = False

        self.prev_entry = self.at_entry.Value
        self.prev_exit = self.at_exit.Value
