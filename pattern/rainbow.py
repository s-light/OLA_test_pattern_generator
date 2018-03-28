#!/usr/bin/env python2
# coding=utf-8

"""
rainbow pattern.

    generates a test pattern:
    rainbow

    history:
        see git commits

    todo:
        ~ all fine :-)
"""


import sys
import array
# import colorsys

import pattern

##########################################
# globals


##########################################
# functions


##########################################
# classes


class Rainbow(pattern.Pattern):
    """Rainbow Pattern Class."""

    def __init__(self, config, config_global):
        """Init pattern."""
        self.config_defaults = {
            "cycle_duration": 10,
            "position_current": 0,
        }
        # python3 syntax
        # super().__init__()
        # python2 syntax
        # super(Pattern, self).__init__()
        # explicit call
        pattern.Pattern.__init__(self, config, config_global)

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

        # get current positon
        position_current = self.config["position_current"]

        # in milliseconds
        cycle_duration = self.config["cycle_duration"] * 1000

        # calculate stepsize
        # step_count = cycle_duration / update_interval
        # cycle_duration = 1.0
        # update_interval = position_stepsize
        position_stepsize = 1.0 * self.update_interval / cycle_duration

        # calculate new position
        position_current = position_current + position_stepsize
        # check for upper bound
        if position_current >= 1:
            position_current -= 1
        # write position_current back:
        self.config["position_current"] = position_current
        # print("position_current", position_current)

        # generate color values for all pixels
        for pixel_index in range(0, self.pixel_count):
            # map hue to pixel position
            pixel_position_step = 1.0 * pixel_index / self.pixel_count
            pixel_position = position_current + pixel_position_step
            # check for wrap around
            if pixel_position > 1.0:
                pixel_position -= 1.0
                # print("handle wrap around")

            # print("pixel_position", pixel_position)

            # set all channels
            # for color_name in self.color_channels:

            # print(debug_string)

            hue = pixel_position
            saturation = 1
            value = pattern.map_16bit_to_01(self.values['high'])
            # print("hue: {}".format(hue))
            # print("value: {}".format(value))

            rgb = self._hsv_01_to_rgb_16bit(
                hue, saturation, value
            )

            # r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            #
            # r_hb, r_lb = self._calculate_16bit_values(
            #     pattern.map_01_to_16bit(r)
            # )
            # g_hb, g_lb = self._calculate_16bit_values(
            #     pattern.map_01_to_16bit(g)
            # )
            # b_hb, b_lb = self._calculate_16bit_values(
            #     pattern.map_01_to_16bit(b)
            # )

            for repeate_index in range(0, self.repeat_count):
                pixel_offset = (
                    self.pixel_count *
                    self.color_channels_count *
                    repeate_index
                )
                local_pixel_index = pixel_offset + (
                    pixel_index * self.color_channels_count
                )
                if self.repeat_snake:
                    # every odd index
                    if ((repeate_index % 2) > 0):
                        # total_pixel_channel_count = (
                        #     self.pixel_count * self.color_channels_count
                        # )
                        # local_pixel_index = local_pixel_index
                        local_pixel_index = pixel_offset + (
                            ((self.pixel_count - 1) - pixel_index) *
                            self.color_channels_count
                        )
                        # print("local_pixel_index", local_pixel_index)

                # set colors to pixel:
                if self.mode_16bit:
                    data_output[local_pixel_index + 0] = rgb['red']['high']
                    data_output[local_pixel_index + 1] = rgb['red']['low']
                    data_output[local_pixel_index + 2] = rgb['green']['high']
                    data_output[local_pixel_index + 3] = rgb['green']['low']
                    data_output[local_pixel_index + 4] = rgb['blue']['high']
                    data_output[local_pixel_index + 5] = rgb['blue']['low']
                    # we have no values for white...
                    # data_output[local_pixel_index + 6] = b_hb
                    # data_output[local_pixel_index + 7] = b_lb
                else:
                    data_output[local_pixel_index + 0] = rgb['red']['high']
                    data_output[local_pixel_index + 1] = rgb['green']['high']
                    data_output[local_pixel_index + 2] = rgb['blue']['high']

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
