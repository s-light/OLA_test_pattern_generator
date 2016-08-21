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
            'wrapp_around_count': 40
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
        # prepare temp array
        data_output = array.array('B')
        # available attributes:
        # global things
        # self.mode_16bit
        # self.channel_count
        # self.values['off']
        # self.values['low']
        # self.values['high']
        # self.config_global[]
        # fill array with meaningfull data according to the pattern :-)
        # .....

        value_low_hb, value_low_lb = self._calculate_16bit_values(
            self.values['low']
        )
        value_high_hb, value_high_lb = self._calculate_16bit_values(
            self.values['high']
        )

        # for devices generate pattern
        # for index in range(0, self.channel_count):
        for index in range(0, self.pixel_count):
            # if index is channel_current:
            high_byte = value_low_hb
            low_byte = value_low_lb
            if index is self.channel_current:
                high_byte = value_high_hb
                low_byte = value_high_lb
            if self.mode_16bit:
                data_output.append(high_byte)
                data_output.append(low_byte)
            else:
                data_output.append(high_byte)

        if (
            self.channel_current <
            self.config['wrapp_around_count']-1
        ):
            self.channel_current = self.channel_current + 1
        else:
            self.channel_current = 0

        return data_output

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
