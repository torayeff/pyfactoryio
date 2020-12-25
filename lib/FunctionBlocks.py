from lib.StopWatch import StopWatch


class FTRIG:
    """Falling edge detection"""

    def __init__(self):
        self.__clk = False
        self.__q = False

    def CLK(self, val):
        self.__q = self.__clk and (not val)
        self.__clk = val

    def get_q(self):
        return self.__q


class RTRIG:
    """Rising edge detection"""

    def __init__(self):
        self.__clk = True
        self.__q = True

    def CLK(self, val):
        self.__q = (not self.__clk) and val
        self.__clk = val

    def get_q(self):
        return self.__q


class TOF:
    """Off delay timer"""

    def __init__(self):
        self.sw = StopWatch()

        self.__input = False
        self.__q = False
        self.__et = 0
        self.__pt = 0

    def check_elapsed_time(self):
        self.__et = int(self.sw.elapsed_time())
        if self.__et > self.__pt:
            self.__q = False
            self.__et = self.__pt

    def get_pt(self):
        return self.__pt

    def set_pt(self, value):
        self.__pt = value

    def set_in(self, value):
        if (not self.__input) and value:
            self.sw.reset()
            self.__q = True

        if self.__input and (not value):
            self.sw.start()

        self.__input = value

    def get_q(self):
        self.check_elapsed_time()
        return self.__q

    def get_et(self):
        self.check_elapsed_time()
        return self.__et
