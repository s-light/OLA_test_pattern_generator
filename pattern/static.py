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


import pattern
import array

##########################################
# globals


##########################################
# functions


##########################################
# classes


class Static(pattern.Pattern):
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
        pattern.Pattern.__init__(self, config, config_global)

        # inits for this pattern

        # setup pattern wide data_output array
        self.channel_count_for_pixel = (
            self.pixel_count * len(self.color_channels)
        )
        if self.mode_16bit:
            self.channel_count_for_pixel = self.channel_count_for_pixel * 2

        self.data_output = array.array('B')
        for index in range(0, self.channel_count_for_pixel):
            self.data_output.append(0)

    def set_data_output(
        self,
        high_byte,
        low_byte,
        mode_16bit
    ):
        """TODO:write docstring."""
        if mode_16bit:
            for index in xrange(0, self.channel_count_for_pixel, 2):
                self.data_output[index] = high_byte
                self.data_output[index + 1] = low_byte
        else:
            for index in xrange(0, self.channel_count_for_pixel):
                self.data_output[index] = high_byte

    def add_data_output(
        self,
        data_output,
        channel_count_for_pixel,
        high_byte,
        low_byte,
        mode_16bit
    ):
        """TODO:write docstring."""
        if mode_16bit:
            data_output.append(high_byte)
            data_output.append(low_byte)
        else:
            data_output.append(high_byte)
        data_output *= channel_count_for_pixel

    def _calculate_step(self):
        """Calculate single step."""
        # pattern.Pattern._calculate_step(self)
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

        self.update_config()

        # # prepare temp array
        # data_output = array.array('B')
        # data_output.append(0)
        # # multiply so we have a array with total_channel_count zeros in it:
        # # this is much faster than a for loop!
        # data_output *= self.total_channel_count

        # fill array with meaningfull data according to the pattern :-)

        # get this as local to speed up.
        mode_16bit = self.mode_16bit

        value_high_hb, value_high_lb = pattern.calculate_16bit_parts(
            self.values['high']
        )

        # for devices generate pattern
        high_byte = value_high_hb
        low_byte = value_high_lb

        # generate array on every calculation step
        data_output = array.array('B')

        channel_count_for_pixel = self.pixel_count * len(self.color_channels)
        # this is not needed for the current append mechanisem.
        # if mode_16bit is  active the array of both values will be multiplyed.
        # if mode_16bit:
        #     channel_count_for_pixel = channel_count_for_pixel * 2

        self.add_data_output(
            data_output,
            channel_count_for_pixel,
            high_byte,
            low_byte,
            mode_16bit
        )
        return data_output

        # use pregenerated array
        # self.set_data_output(
        #     high_byte,
        #     low_byte,
        #     mode_16bit
        # )
        # return self.data_output


##########################################
if __name__ == '__main__':
    import sys
    print(42*'*')
    print('Python Version: ' + sys.version)
    print(42*'*')
    print(__doc__)
    print(42*'*')
    print("This Module has now stand alone functionality.")
    print(42*'*')

    ##########################################
