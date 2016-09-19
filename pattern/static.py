#!/usr/bin/env python
# coding=utf-8

"""
static pattern.

    generates a test pattern:
    sets all channels to high value

    history:
        see git commits

    todo:
        ~ all fine :-)
"""


from pattern import Pattern
import array

##########################################
# globals


##########################################
# functions


##########################################
# classes


class Static(Pattern):
    """Static Pattern Class."""

    def __init__(self, config, config_global):
        """Init pattern."""
        self.config_defaults = {
            "channels": [],
        }
        # python3 syntax
        # super().__init__()
        # python2 syntax
        # super(Pattern, self).__init__()
        # explicit call
        Pattern.__init__(self, config, config_global)

        # inits for this pattern

        # setup pattern wide data_output array
        self.channel_count_for_pixel = (
            self.pixel_count * len(self.color_channels)
        )
        if self.mode_16bit:
            self.channel_count_for_pixel = channel_count_for_pixel * 2

        self.data_output = array.array('B')
        for index in range(0, self.channel_count_for_pixel):
            self.data_output.append(0)

    def set_data_output(
        self,
        high_byte,
        low_byte,
        mode_16bit
    ):
        channel_stepsize = 1
        if mode_16bit:
            channel_stepsize = 2

        for index in range(0, self.channel_count_for_pixel, channel_stepsize):

            if mode_16bit:
                self.data_output[index] = high_byte
                self.data_output[index + 1] = low_byte
            else:
                self.data_output[index] = high_byte

    def add_data_output(
        self,
        data_output,
        channel_count_for_pixel,
        high_byte,
        low_byte,
        mode_16bit
    ):
        for index in range(0, channel_count_for_pixel):

            if mode_16bit:
                data_output.append(high_byte)
                data_output.append(low_byte)
            else:
                data_output.append(high_byte)

    def _calculate_step(self):
        """Calculate single step."""
        # prepare temp array
        # data_output = array.array('B')
        # available attributes:
        # global things (readonly)
        # self.channel_count
        # self.pixel_count
        # self.repeate_count
        # self.repeate_snake
        # self.color_channels
        # self.update_interval
        # self.mode_16bit
        # self.values['off']
        # self.values['low']
        # self.values['high']
        # self.config_global[]
        # fill array with meaningfull data according to the pattern :-)
        # .....

        # get this as local to speed up.
        mode_16bit = self.mode_16bit

        value_high_hb, value_high_lb = self._calculate_16bit_values(
            self.values['high']
        )

        # channel_count_for_pixel = self.pixel_count * len(self.color_channels)
        # if mode_16bit:
        #     channel_count_for_pixel = channel_count_for_pixel * 2

        # for devices generate pattern
        high_byte = value_high_hb
        low_byte = value_high_lb
        # self.add_data_output(
        #     data_output,
        #     channel_count_for_pixel,
        #     high_byte,
        #     low_byte,
        #     mode_16bit
        # )
        self.set_data_output(
            high_byte,
            low_byte,
            mode_16bit
        )
        return self.data_output

##########################################
if __name__ == '__main__':

    print(42*'*')
    print('Python Version: ' + sys.version)
    print(42*'*')
    print(__doc__)
    print(42*'*')
    print("This Module has now stand alone functionality.")
    print(42*'*')

    ##########################################
