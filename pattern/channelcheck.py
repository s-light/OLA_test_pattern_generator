#!/usr/bin/env python
# coding=utf-8

"""
channel check pattern.

    generates a test pattern:
    go throu all channels one after one..

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


class Channelcheck(pattern.Pattern):
    """Channelcheck pattern Class."""

    def __init__(self, config, config_global):
        """Init pattern."""
        self.config_defaults = {
            'x': 42
        }
        # python3 syntax
        # super().__init__()
        # python2 syntax
        # super(Pattern, self).__init__()
        # explicit call
        pattern.Pattern.__init__(self, config, config_global)

        # inits for this pattern
        self.channel_current = 0

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

        # prepare temp array
        data_output = array.array('B')
        # data_output.append(0)
        # # multiply so we have a array with total_channel_count zeros in it:
        # # this is much faster than a for loop!
        # data_output *= self.total_channel_count

        # fill array with meaningfull data according to the pattern :-)

        value_low_hb, value_low_lb = self._calculate_16bit_values(
            self.values['low']
        )
        value_high_hb, value_high_lb = self._calculate_16bit_values(
            self.values['high']
        )

        # prefill with low value:
        if self.mode_16bit:
            data_output.append(value_low_hb)
            data_output.append(value_low_lb)
        else:
            data_output.append(value_low_hb)
        # multiply so we have a array with total_channel_count zeros in it:
        # this is much faster than a for loop!
        data_output *= self.total_channel_count

        if self.mode_16bit:
            data_output[self.channel_current] = value_high_hb
            data_output[self.channel_current + 1] = value_high_lb
        else:
            data_output[self.channel_current] = value_high_hb

        # # for devices generate pattern
        # # for index in range(0, self.channel_count):
        # for index in range(0, self.pixel_count):
        #     # if index is channel_current:
        #     high_byte = value_low_hb
        #     low_byte = value_low_lb
        #     if index is self.channel_current:
        #         high_byte = value_high_hb
        #         low_byte = value_high_lb
        #     if self.mode_16bit:
        #         data_output.append(high_byte)
        #         data_output.append(low_byte)
        #     else:
        #         data_output.append(high_byte)

        if (
            self.channel_current <
            self.pixel_count-1
        ):
            if self.mode_16bit:
                self.channel_current = self.channel_current + 2
            else:
                self.channel_current = self.channel_current + 1
        else:
            self.channel_current = 0

        return data_output

##########################################
if __name__ == '__main__':

    print(42 * '*')
    print('Python Version: ' + sys.version)
    print(42 * '*')
    print(__doc__)
    print(42 * '*')
    print("This Module has now stand alone functionality.")
    print(42 * '*')

    ##########################################
