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

        # print("")

        position_current = self.config["position_current"]

        color_channels_count = len(self.color_channels)

        # in milliseconds
        cycle_duration = self.config["cycle_duration"] * 1000

        # calculate stepsize
        # step_count = cycle_duration / update_interval
        # cycle_duration = 1
        # update_interval = position_stepsize
        position_stepsize = 1.0 * self.update_interval / cycle_duration

        # initilaize our data array to the maximal possible size:
        for index in range(
            0,
            self.pixel_count * self.repeate_count * color_channels_count
        ):
            data_output.append(0)

        # calculate new position
        position_current = position_current + position_stepsize
        # check for upper bound
        if position_current >= 1:
            position_current = 0.0
        # write position_current back:
        self.config["position_current"] = position_current
        # print("position_current", position_current)

        # ?? needed for what?
        # channel_stepsize = color_channels_count
        # if self.mode_16bit:
        #     channel_stepsize = color_channels_count*2

        # print("****")

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

            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)

            r_hb, r_lb = self._calculate_16bit_values(
                pattern.map_01_to_16bit(r)
            )
            g_hb, g_lb = self._calculate_16bit_values(
                pattern.map_01_to_16bit(g)
            )
            b_hb, b_lb = self._calculate_16bit_values(
                pattern.map_01_to_16bit(b)
            )

            for repeate_index in range(0, self.repeate_count):
                pixel_offset = (
                    self.pixel_count *
                    color_channels_count *
                    repeate_index
                )
                local_pixel_index = pixel_offset + pixel_index
                # set colors to pixel:
                if self.mode_16bit:
                    data_output[local_pixel_index + 0] = r_hb
                    data_output[local_pixel_index + 1] = r_lb
                    data_output[local_pixel_index + 2] = g_hb
                    data_output[local_pixel_index + 3] = g_lb
                    data_output[local_pixel_index + 4] = b_hb
                    data_output[local_pixel_index + 5] = b_lb
                    # we have no values for white...
                    # data_output[local_pixel_index + 6] = b_hb
                    # data_output[local_pixel_index + 7] = b_lb
                else:
                    data_output[local_pixel_index + 0] = r_hb
                    data_output[local_pixel_index + 1] = g_hb
                    data_output[local_pixel_index + 2] = b_hb

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
