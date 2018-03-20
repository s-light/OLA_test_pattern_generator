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
import colorsys

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
        # print("_update_colors")
        start_universe = self.config_global['universe']['output']
        universe_list = range(
            start_universe,
            start_universe + self.config_global['universe']['count']
        )
        # print("universe_list:{}".format(universe_list))

        hue_step = 1.0 / self.config_global['universe']['count']
        # print("hue_step:{}".format(hue_step))

        for universe in universe_list:
            # print("universe:{}".format(universe))
            hue_section = (universe - start_universe)
            # hue = hue_step * hue_section
            hue = (hue_step * hue_section) + (0.5 * (hue_section % 2))
            if hue > 1:
                hue = hue - 1
            # hue = random.random(0, 1)
            saturation = 1
            value_high = pattern.map_16bit_to_01(self.values['high'])
            value_low = pattern.map_16bit_to_01(self.values['low'])
            # self.colors[universe] = {
            #     'hue': hue,
            #     'saturation': saturation,
            #     'value': value,
            # }
            # print("hue:{}".format(hue))
            # print(
            #     "hue:{}, "
            #     "saturation:{}, "
            #     "value_high:{}".format(
            #         hue,
            #         saturation,
            #         value_high
            #     )
            # )
            self.colors_rgb_high[universe] = self._hsv_01_to_rgb_16bit(
                hue, saturation, value_high
            )
            self.colors_rgb_low[universe] = self._hsv_01_to_rgb_16bit(
                hue, saturation, value_low
            )
        # debug output
        # print(
        #     "resulting arrays:\n"
        #     " colors_rgb_high:{}\n"
        #     " colors_rgb_low:{}".format(
        #         self.colors_rgb_high,
        #         self.colors_rgb_low
        #     )
        # )

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

        if not universe:
            universe = self.config_global['universe']['output']

        if universe == self.config_global['universe']['output']:
            self.update_config()
            self._update_colors()

        # prepare temp array
        data_output = array.array('B')
        # data_output.append(0)
        # # multiply so we have a array with total_channel_count zeros in it:
        # # this is much faster than a for loop!
        # data_output *= self.total_channel_count

        # fill array with meaningfull data according to the pattern :-)
        # .....

        # color = {
        #     'red': {
        #         'high': 0,
        #         'low': 0,
        #     },
        #     'green': {
        #         'high': 0,
        #         'low': 0,
        #     },
        #     'blue': {
        #         'high': 0,
        #         'low': 0,
        #     },
        # }
        # if universe in self.colors_rgb_high:
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

        # toggle strobe_state after last universe
        if (
            universe ==
            self.config_global['universe']['output'] +
            self.config_global['universe']['count'] - 1
        ):
            self.strobe_state = not self.strobe_state

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
