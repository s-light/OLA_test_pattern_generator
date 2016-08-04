#!/usr/bin/env python
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


import pattern
import array
import colorsys

##########################################
# globals


##########################################
# functions


##########################################
# classes


class Rainbow(pattern.Pattern):
    """Rainbow Pattern Class."""

    def __init__(self, config, config_global):
        """init pattern."""
        self.config_defaults = {
            'cycle_duration': 10,
            "color_channels": [
                "red",
                "green",
                "blue",
            ],
            "steps": [
                {
                    "position":0,
                    "red": 1,
                    "green": 1,
                    "blue": 1,
                },
                {
                    "position":0.25,
                    "red": 1,
                    "green": 0,
                    "blue": 0,
                },
                {
                    "position":0.5,
                    "red": 0,
                    "green": 1,
                    "blue": 0,
                },
                {
                    "position":0.75,
                    "red": 0,
                    "green": 0,
                    "blue": 1,
                },
            ],
        }
        # python3 syntax
        # super().__init__()
        # python2 syntax
        # super(Pattern, self).__init__()
        # explicit call
        pattern.Pattern.__init__(self, config, config_global)

        # inits for this pattern
        self.hue_current = 0.0

    def _calculate_step(self):
        """calculate single step."""
        # prepare temp array
        data_output = array.array('B')
        # available attributes:
        # global things (readonly)
        # self.mode_16bit
        # self.channel_count
        # self.pixel_count
        # self.values['off']
        # self.values['low']
        # self.values['high']
        # self.config_global[]
        # fill array with meaningfull data according to the pattern :-)
        # .....

        # print("")

        hue = self.hue_current
        saturation = 1
        value = 1
        # print("hue: {}".format(hue))

        # in seconds
        cycle_duration = self.config["cycle_duration"]
        # convert to ms
        cycle_duration = cycle_duration * 1000
        # in ms
        update_interval = self.config_global["update_interval"]

        # step_count = cycle_duration / update_interval
        # cycle_duration = 1
        # update_interval = hue_stepsize
        hue_stepsize = 1.0 * update_interval / cycle_duration

        self.hue_current = self.hue_current + hue_stepsize
        if self.hue_current >= 1:
            self.hue_current = 0.0

        channel_stepsize = 3
        if self.mode_16bit:
            channel_stepsize = 8

        # for devices generate pattern
        for pixel_index in range(0, self.pixel_count):
            # map hue to pixel position
            # pixel_count = 1
            # pixel_index = pixel_hue_step
            pixel_hue_step = 1.0 * pixel_index / self.pixel_count
            pixel_hue = hue + pixel_hue_step
            r, g, b = colorsys.hsv_to_rgb(pixel_hue, saturation, value)
            r_hb, r_lb = self.calculate_16bit_values(
                pattern.map_01_to_16bit(r)
            )
            g_hb, g_lb = self.calculate_16bit_values(
                pattern.map_01_to_16bit(g)
            )
            b_hb, b_lb = self.calculate_16bit_values(
                pattern.map_01_to_16bit(b)
            )

            if self.mode_16bit:
                data_output.append(r_hb)
                data_output.append(r_lb)
                data_output.append(g_hb)
                data_output.append(g_lb)
                data_output.append(b_hb)
                data_output.append(b_lb)
                data_output.append(0)
                data_output.append(0)
            else:
                data_output.append(r_hb)
                data_output.append(g_hb)
                data_output.append(b_hb)

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
