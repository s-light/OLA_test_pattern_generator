#!/usr/bin/env python
# coding=utf-8

"""
color multi universe pattern.

    generates a test pattern:


    history:
        see git commits

    todo:
        ~ all fine :-)
"""

import sys
import array

import pattern

##########################################
# globals


##########################################
# functions


##########################################
# classes


class ColorsMultiuninverse(pattern.Pattern):
    """ColorsMultiuninverse Pattern Class."""

    def __init__(self, config, config_global):
        """Init pattern."""
        self.config_defaults = {
            'update_interval': 5000,
            'colors': {},
        }
        # python3 syntax
        # super().__init__()
        # python2 syntax
        # super(Pattern, self).__init__()
        # explicit call
        pattern.Pattern.__init__(self, config, config_global)

        # inits for this pattern
        self.strobe_state = False
        self.colors = self.config['colors']
        self.colors_rgb_high = {}
        self.colors_rgb_low = {}

    def _update_colors(self):
        start_universe = self.config_global['universe']['output']
        universe_list = range(
            start_universe,
            start_universe + self.config_global['universe']['count']
        )

        hue_step = 360 / self.config_global['universe']['count']

        for universe in universe_list:
            hue = hue_step * (universe - start_universe)
            saturation = 1
            value_high = pattern.map_16bit_to_01(self.values['high'])
            value_low = pattern.map_16bit_to_01(self.values['low'])
            # self.colors[universe] = {
            #     'hue': hue,
            #     'saturation': saturation,
            #     'value': value,
            # }
            self.colors_rgb_high[universe] = self._hsv_01_to_rgb_16bit(
                hue, saturation, value_high
            )
            self.colors_rgb_high[universe] = self._hsv_01_to_rgb_16bit(
                hue, saturation, value_low
            )

    def _calculate_step(self, universe):
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
        #
        # self.colors_rgb_high
        # self.colors_rgb_low

        if universe == self.config_global['universe']['output']:
            self.update_config()
            self._update_colors()
            # toggle strobe_state
            self.strobe_state = not self.strobe_state

        # prepare temp array
        data_output = array.array('B')
        # data_output.append(0)
        # # multiply so we have a array with total_channel_count zeros in it:
        # # this is much faster than a for loop!
        # data_output *= self.total_channel_count

        # fill array with meaningfull data according to the pattern :-)
        # .....

        color = self.colors_rgb_high[universe]
        if not self.strobe_state:
            color = self.colors_rgb_low[universe]

        if self.mode_16bit:
            data_output.append(color['red']['high'])
            data_output.append(color['red']['low'])
            data_output.append(color['green']['high'])
            data_output.append(color['green']['low'])
            data_output.append(color['blue']['high'])
            data_output.append(color['blue']['low'])
        else:
            data_output.append(color['red']['high'])
            data_output.append(color['green']['high'])
            data_output.append(color['blue']['high'])

        # copy for all pixels
        data_output *= self.pixel_count

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
