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
from __future__ import division

import sys
import importlib
import os
import pkgutil
import collections
import array
import struct
import colorsys

import configdict

##########################################
# globals

pattern_list = []


##########################################
# special functions

def _load_all_modules(path, names):
    """Load all modules in path.

    usage:
        # Load all modules in the current directory.
        load_all_modules(__file__,__name__)

    based on
        http://stackoverflow.com/a/25459405/574981
        from Daniel Kauffman

    """
    module_names = []
    # For each module in the current directory...
    for importer, module_name, is_package in pkgutil.iter_modules(
        [os.path.dirname(path)]
    ):
        # print("importing:", names + '.' + module_name)
        # Import the module.
        importlib.import_module(names + '.' + module_name)
        module_names.append(module_name)

    return module_names


##########################################
# package init

# Load all modules in the current directory.
# load_all_modules(__file__, __name__)

def load_all_submodules():
    """Load all submodules in this directory."""
    # Load all modules in the current directory.
    pattern_list = _load_all_modules(__file__, __name__)
    return pattern_list


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
    # # without clamping - reworded
    # result = (
    #     (
    #         ((value - in_low) / (in_high - in_low)) *
    #         (out_high - out_low)
    #     ) + out_low
    # )

    result = None

    # based on http://arduino.cc/en/Reference/Map
    # and http://stackoverflow.com/a/5650012/574981
    result = (
        (
            ((value - in_low) * (out_high - out_low)) /
            (in_high - in_low)
        ) + out_low
    )

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
            result = out_low + (
                (out_high - out_low) * (value - in_low) / (in_high - in_low)
            )
    return result


def map_01_to_8bit(value):
    """Map value from 0-1 range to 0-255 range."""
    result = None
    result = int(map_bound(value, 0.0, 1.0, 0, 255))
    return result


def map_01_to_16bit(value):
    """Map value from 0-1 range to 0-65535 range."""
    # result = None
    # result = int(map_bound(value, 0.0, 1.0, 0, 65535))
    # return result
    # return int(map_bound(value, 0.0, 1.0, 0, 65535))
    # result = None
    # if value <= 0:
    #     # result = 0
    #     return 0
    # else:
    #     if value >= 1:
    #         # result = 65535
    #         return 65535
    #     else:
    #         # simplified
    #         # result = 65535 * value / 1
    #         return int(65535 * value)
    # return result
    return int(65535 * value)


def map_16bit_to_01(value):
    """Map value from 0-65535 range to 0-1 range."""
    result = None
    result = map_bound(value, 0, 65535, 0.0, 1.0)
    return result


def map_16bit_to_8bit(value):
    """Map value from 0-65535 range to 0-255 range."""
    if not (0 <= value < 65535):
        value = min(max(value, 0), 65535)
    return value >> 8


def calculate_16bit_parts(value):
    """Calculate the low and high part representations of value."""
    if not (0 <= value < 65535):
        value = min(max(value, 0), 65535)
    # high_byte = value // 256
    # low_byte = value % 256
    # return high_byte, low_byte
    # faster:
    # return value // 256, value % 256
    # faster again:
    return value >> 8, value & 255


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


def calculate_16bit_values_as_dict(value, mode_16bit=False):
    """
    Calculate the low and high part representations of value.

    returns these as dict
    """
    high_byte, low_byte = calculate_16bit_values(value, mode_16bit)
    result = {
        'high': high_byte,
        'low': low_byte,
    }
    return result


def hsv_01_to_rgb_16bit(hue, saturation, value, mode_16bit):
    """
    Convert hsv 0-1 floating values to rgb 16bit representations.

    and returns this as dict with named attributes.
    """
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)

    rgb16bit = {
        'red': calculate_16bit_values_as_dict(
            map_01_to_16bit(r),
            mode_16bit
        ),
        'green': calculate_16bit_values_as_dict(
            map_01_to_16bit(g),
            mode_16bit
        ),
        'blue': calculate_16bit_values_as_dict(
            map_01_to_16bit(b),
            mode_16bit
        )
    }
    return rgb16bit


##########################################
# classes


Value_16bit = collections.namedtuple('Value_16bit', ['hb', 'lb'])


class Pattern(object):
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
        self.update_config()

    def update_config(self):
        """Update all internal values from config_global."""
        self.channel_count = self.config_global['channel_count']
        self.pixel_count = self.config_global['pixel_count']
        self.pixel_index_max = self.pixel_count - 1
        self.repeat_count = self.config_global['repeat_count']
        self.repeat_snake = self.config_global['repeat_snake']

        self.update_interval = self.config_global['update_interval']
        self.mode_16bit = self.config_global['mode_16bit']

        self.color_channels = self.config_global['color_channels']
        # self.color_channels = collections.namedtuple(
        #     'color_channels',
        #     **self.color_channels_dict
        # )
        self.color_channels_count = len(self.color_channels)
        if self.mode_16bit:
            self.color_channels_count = self.color_channels_count * 2

        self.total_channel_count = (
            self.pixel_count *
            self.color_channels_count
        )
        if self.repeat_count > 0:
            self.total_channel_count *= self.repeat_count

    def _calculate_16bit_values(self, value):
        """Calculate the low and high part representations of value."""
        high_byte = 0
        low_byte = 0
        high_byte, low_byte = calculate_16bit_values(value, self.mode_16bit)
        return high_byte, low_byte

    def _hsv_01_to_rgb_16bit(self, hue, saturation, value):
        """Calculate the low and high part representations of value."""
        rgb16bit = hsv_01_to_rgb_16bit(hue, saturation, value, self.mode_16bit)
        return rgb16bit

    def _calculate_step(self, universe):
        """Calculate single step."""
        # pattern.Pattern._calculate_step(self)
        # available attributes:
        # global things (readonly)
        # self.channel_count
        # self.pixel_count
        # self.repeat_count
        # self.repeat_snake
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
        data_output.append(0)
        # multiply so we have a array with total_channel_count zeros in it:
        # this is much faster than a for loop!
        data_output *= self.total_channel_count

        # fill array with meaningfull data according to the pattern :-)
        # .....
        return data_output


##########################################
if __name__ == '__main__':

    print(42 * '*')
    print('Python Version: ' + sys.version)
    print(42 * '*')
    print(__doc__)
    print(42 * '*')
    print("This Module has no stand alone functionality.")
    print(42 * '*')

    ##########################################
