#!/usr/bin/env python2
# coding=utf-8

"""
gradient pattern.

    generates a test pattern:
    gradient

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


class Gradient(pattern.Pattern):
    """Gradient Pattern Class."""

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

    def _calculate_step(self):
        """Calculate single step."""
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

        position_current = self.config["position_current"]

        color_channels = self.config["color_channels"]
        color_channels_count = len(color_channels)

        # in seconds
        cycle_duration = self.config["cycle_duration"]
        # convert to ms
        cycle_duration = cycle_duration * 1000
        # in ms
        update_interval = self.config_global["update_interval"]

        # step_count = cycle_duration / update_interval
        # cycle_duration = 1
        # update_interval = position_stepsize
        position_stepsize = 1.0 * update_interval / cycle_duration

        position_current = position_current + position_stepsize

        if position_current >= 1:
            position_current = 0.0

        # write position_current back:
        self.config["position_current"] = position_current

        # print("position_current", position_current)

        channel_stepsize = color_channels_count
        if self.mode_16bit:
            channel_stepsize = color_channels_count*2

        # print("****")

        # for devices generate pattern
        for pixel_index in range(0, self.pixel_count):
            # map hue to pixel position
            # pixel_count = 1
            # pixel_index = pixel_position_step
            pixel_position_step = 1.0 * pixel_index / self.pixel_count
            pixel_position = position_current + pixel_position_step
            # check for wrap around
            if pixel_position > 1.0:
                pixel_position -= 1.0
                # print("handle wrap around")

            # print("pixel_position", pixel_position)

            # set all channels
            # for color_name in self.config["color_channels"]:

            # print(debug_string)

            # old easy rainbow :-)
            saturation = 1
            value = pattern.map_16bit_to_01(self.values['high'])
            # print("hue: {}".format(hue))
            # print("value: {}".format(value))

            r, g, b = colorsys.hsv_to_rgb(pixel_hue, saturation, value)

            r_hb, r_lb = self._calculate_16bit_values(
                pattern.map_01_to_16bit(r)
            )
            g_hb, g_lb = self._calculate_16bit_values(
                pattern.map_01_to_16bit(g)
            )
            b_hb, b_lb = self._calculate_16bit_values(
                pattern.map_01_to_16bit(b)
            )

            if self.mode_16bit:
                data_output.append(r_hb)
                data_output.append(r_lb)
                data_output.append(g_hb)
                data_output.append(g_lb)
                data_output.append(b_hb)
                data_output.append(b_lb)
                # data_output.append(0)
                # data_output.append(0)
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
