#!/usr/bin/env python
# coding=utf-8

"""
pattern base class.

    generates a test pattern.

    history:
        see git commits

    todo:
        ~ all fine :-)
"""

from configdict import merge_deep
import array

##########################################
# globals


##########################################
# functions


##########################################
# classes


class Pattern(Object):
    """Base Pattern Class."""

    def __init__(self, config, config_global):
        """init pattern."""
        # merge config with defaults
        self.config_defaults = {}
        self.config = self.config_defaults.copy()
        merge_deep(self.config, config)

        self.config_global = config_global
        # print("config: {}".format(self.config))
        self.channel_count = config_global['channel_count']
        self.mode_16bit = config_global['mode_16bit']
        self.values = config_global['value']

    def calculate_16bit_values(self, value):
        """calculate the low and high part representations of value."""
        high_byte = 0
        low_byte = 0
        if self.mode_16bit:
            high_byte, low_byte = struct.unpack(
                "<BB",
                struct.pack("<h", value)
            )
        else:
            if value > 255:
                # convert 16bit range to 8bit range
                value = value / 256
            # check for bounds
            if value > 255:
                value = 255
            if value < 0:
                value = 0
            high_byte = value
        return high_byte, low_byte

    def _calculate_step(self):
        """calculate single step."""
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
