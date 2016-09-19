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

# https://docs.python.org/2.7/howto/pyporting.html#division
# from __future__ import division

import array
import struct

import configdict

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
    result = int(map_bound(value, 0.0, 1.0, 0, 255))
    return result


def map_01_to_16bit(value):
    """Map value from 0-1 range to 0-65535 range."""
    result = None
    result = int(map_bound(value, 0.0, 1.0, 0, 65535))
    return result


def map_16bit_to_01(value):
    """Map value from 0-65535 range to 0-1 range."""
    result = None
    result = map_bound(value, 0, 65535, 0.0, 1.0)
    return result


def calculate_16bit_parts(value):
    """Calculate the low and high part representations of value."""
    if not (0 <= value < 65535):
        value = min(max(value, 0), 65535)
    # high_byte = value // 256
    # low_byte = value % 256
    # return high_byte, low_byte
    return value // 256, value % 256


def calculate_16bit_values(value, mode_16bit=False):
    """Calculate the low and high part representations of value."""
    high_byte = 0
    low_byte = 0
    # if mode_16bit:
    if value > 65535:
        value = 65535
    low_byte, high_byte = struct.unpack(
        "<BB",
        struct.pack("<H", value)
    )
    # else:
    #     if value > 255:
    #         # convert 16bit range to 8bit range
    #         value = value / 256
    #     # check for bounds
    #     if value > 255:
    #         value = 255
    #     if value < 0:
    #         value = 0
    #     high_byte = value
    return high_byte, low_byte

##########################################
# classes


class Pattern():
    """Base Pattern Class."""

    def __init__(self, config, config_global):
        """Init pattern."""
        # merge config with defaults
        if not self.config_defaults:
            self.config_defaults = {}
        # extend config with defaults
        self.config = config
        configdict.extend_deep(self.config, self.config_defaults.copy())
        # print("config: {}".format(self.config))

        self.config_global = config_global
        # print("config_global: {}".format(self.config_global))
        # self.channel_count = config_global['channel_count']
        # self.pixel_count = config_global['pixel_count']
        # self.mode_16bit = config_global['mode_16bit']
        self.values = config_global['value']

    @property
    def channel_count(self):
        """Shortcut to channel_count."""
        return self.config_global['channel_count']

    @property
    def pixel_count(self):
        """Shortcut to pixel_count."""
        return self.config_global['pixel_count']

    @property
    def repeate_count(self):
        """Shortcut to repeate_count."""
        return self.config_global['repeate_count']

    @property
    def repeate_snake(self):
        """Shortcut to repeate_snake."""
        return self.config_global['repeate_snake']

    @property
    def color_channels(self):
        """Shortcut to color_channels."""
        return self.config_global['color_channels']

    @property
    def update_interval(self):
        """Shortcut to update_interval."""
        return self.config_global['update_interval']

    @property
    def mode_16bit(self):
        """Shortcut to mode_16bit."""
        return self.config_global['mode_16bit']

    def _calculate_16bit_values(self, value):
        """Calculate the low and high part representations of value."""
        high_byte = 0
        low_byte = 0
        high_byte, low_byte = calculate_16bit_values(value, self.mode_16bit)
        return high_byte, low_byte

    def _calculate_step(self):
        """Calculate single step."""
        # prepare temp array
        data_output = array.array('B')
        # available attributes:
        # global things
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
        return data_output

##########################################
if __name__ == '__main__':

    print(42*'*')
    print('Python Version: ' + sys.version)
    print(42*'*')
    print(__doc__)
    print(42*'*')
    print("This Module has no stand alone functionality.")
    print(42*'*')

    ##########################################
