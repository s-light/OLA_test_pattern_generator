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
import struct

##########################################
# globals


##########################################
# functions

def map(value, in_low, in_high, out_low, out_high):
    """
    Map value from on range to another.

    ((value - in_low) * (out_high - out_low)) / (in_high - in_low) + out_low
    """
    # example from /animation_nodes/nodes/number/map_range.py
    # if inMin == inMax:
    #     newValue = 0
    # # with clamping
    #     if inMin < inMax:
    #         _value = min(max(value, inMin), inMax)
    #     else:
    #         _value = min(max(value, inMax), inMin)
    #     with interpolation
    #         newValue = outMin + interpolation(
    #             (_value - inMin) / (inMax - inMin)
    #         ) * (outMax - outMin)
    #     without interpolation
    #         newValue = outMin + (
    #             (_value - inMin) / (inMax - inMin)
    #         ) * (outMax - outMin)
    # # without clamping
    #     newValue = outMin + (
    #         (value - inMin) / (inMax - inMin)
    #     ) * (outMax - outMin)

    result = None

    # based on http://arduino.cc/en/Reference/Map
    result = ((value - in_low) * (out_high - out_low)) / \
        (in_high - in_low) + out_low

    # http://stackoverflow.com/a/5650012/574981
    # result = out_low + \
    #     ((out_high - out_low) * (value - in_low)) / \
    #     (in_high - in_low)

    return result


def map_bound(value, in_low, in_high, out_low, out_high):
    """Map value with high and low bound handling."""
    result = None

    if value <= in_low:
        result = out_low
    else:
        if value >= in_high:
            result = out_high
        else:
            # http://stackoverflow.com/a/5650012/574981
            result = out_low + \
                (out_high - out_low) * (value - in_low) / (in_high - in_low)
    return result


def map_01_to_8bit(value):
    """Map value from 0-1 range to 0-255 range."""
    result = None
    result = map_bound(value, 0.0, 1.0, 0, 255)
    return result


def map_01_to_16bit(value):
    """Map value from 0-1 range to 0-65535 range."""
    result = None
    result = map_bound(value, 0.0, 1.0, 0, 65535)
    return result


def map_16bit_to_01(value):
    """Map value from 0-65535 range to 0-1 range."""
    result = None
    result = map_bound(value, 0, 65535, 0.0, 1.0)
    return result


##########################################
# classes


class Pattern():
    """Base Pattern Class."""

    def __init__(self, config, config_global):
        """init pattern."""
        # merge config with defaults
        if not self.config_defaults:
            self.config_defaults = {}
        self.config = self.config_defaults.copy()
        merge_deep(self.config, config)
        # print("config: {}".format(self.config))

        self.config_global = config_global
        # print("config_global: {}".format(self.config_global))
        self.channel_count = config_global['channel_count']
        self.pixel_count = config_global['pixel_count']
        self.mode_16bit = config_global['mode_16bit']
        self.values = config_global['value']

    def calculate_16bit_values(self, value):
        """calculate the low and high part representations of value."""
        high_byte = 0
        low_byte = 0
        if self.mode_16bit:
            if value > 65535:
                value = 65535
            low_byte, high_byte = struct.unpack(
                "<BB",
                struct.pack("<H", value)
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
