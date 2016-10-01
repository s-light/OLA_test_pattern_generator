#!/usr/bin/env python2
# coding=utf-8

"""
gradient pattern.

    generates a test pattern:
    gradient
    same output as gradient but with hopefully different calculation logic

    logic:
        start at _calculate_step
        - calculate (new) current position. (position means time)
        for every stop-pair
            for every pixel


    history:
        see git commits

    todo:
        ~ all fine :-)
"""

# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division

import array
import colorsys

import pattern

##########################################
# globals


##########################################
# functions


##########################################
# classes


class Gradient2(pattern.Pattern):
    """Gradient2 Pattern Class."""

    def __init__(self, config, config_global):
        """Init pattern."""
        self.config_defaults = {
            "cycle_duration": 10,
            "position_current": 0,
            "type": "channel",
            "stops": [
                {
                    "position": 0,
                    "red": 1,
                    "green": 1,
                    "blue": 1,
                },
                {
                    "position": 0.3,
                    "red": 1,
                    "green": 0,
                    "blue": 0,
                },
                {
                    "position": 0.7,
                    "red": 0,
                    "green": 1,
                    "blue": 0,
                },
                {
                    "position": 1,
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

    def _interpolate_channels(self, pixel_position, stop_start, stop_end):
        """Interpolate with channels."""
        # print("interpolate_channels")
        result = {}
        # check for exact match
        if pixel_position == stop_start["position"]:
            result = stop_start.copy()
        else:
            # interpolate all colors
            for color_name in self.color_channels:
                result[color_name] = pattern.map(
                    pixel_position,
                    stop_start["position"],
                    stop_end["position"],
                    stop_start[color_name],
                    stop_end[color_name],
                )
            result["position"] = pixel_position

        return result

    def _calculate_pixels_for_position(self, position_current):
        """Calculate pixels for all positions."""
        pixel_count = self.pixel_count
        pixel_index_max = self.pixel_count - 1

        stops_list = self.stops_list
        stops_count = len(stops_list)
        position_stepwidth_per_pixel = self.position_stepwidth_per_pixel

        # print("\n"*2)
        # print("_calculate_pixels_for_position()")
        # print("position_current {: <.9f}".format(position_current))
        #
        # print("pixel_count     {: <}".format(pixel_count))
        # print("pixel_index_max {: <}".format(pixel_index_max))

        color_channels = self.color_channels

        pixel_data = []
        pixel_data.append(0)
        pixel_data *= pixel_count

        # for every section in the stops_list
        for stop_index, stop_start in enumerate(stops_list):
            if stop_index < (stops_count-1):
                stop_end = stops_list[stop_index+1]
            else:
                stop_end = stops_list[0]

            stop_start_position = stop_start["position"]
            stop_end_position = stop_end["position"]
            # print("stop_index {}".format(stop_index))
            # print("stop_start {}".format(stop_start))
            # print("stop_end   {}".format(stop_end))

            # calculate first and last pixel position for this section
            pixel_position_start = stop_start_position + position_current
            # pixel_position_start = stop_start['position']
            # print("pixel_position_start {: <.3f}".format(
            #     pixel_position_start
            # ))
            # # check for wrap around
            # if pixel_position_start > 1.0:
            #     pixel_position_start -= 1.0

            # print("pixel_position_start {: <.3f}".format(
            #     pixel_position_start
            # ))

            pixel_position_end = stop_end_position + position_current
            # pixel_position_end = stop_end['position']
            # print("pixel_position_end   {: <.3f}".format(pixel_position_end))
            # # check for wrap around
            # if pixel_position_end > 1.0:
            #     pixel_position_end -= 1.0

            # print("pixel_position_end   {: <.3f}".format(pixel_position_end))

            # calculate pixel index from position:
            pixel_index_start = int(
                pixel_position_start * pixel_index_max
            )
            # print("pixel_index_start    {}".format(pixel_index_start))

            pixel_index_end = int(
                pixel_position_end * pixel_index_max
            )
            # print("pixel_index_end      {}".format(pixel_index_end))
            # # handle wrap around in value
            # if pixel_index_end < pixel_index_max:
            #     pixel_index_end -= pixel_index_max
            # print("pixel_index_end      {}".format(pixel_index_end))
            # handle wrap around for xrange
            if pixel_index_end < pixel_index_start:
                pixel_index_end += pixel_index_max

            # print("pixel_index_end      {}".format(pixel_index_end))

            # check if there are pixels in this section
            if (pixel_index_end - pixel_index_start) > 0:
                # precalculate for mapping
                position_diff = stop_end_position - stop_start_position
                pixel_index_diff = pixel_index_end - pixel_index_start
                factor_pixel_pos = position_diff / pixel_index_diff

                # for every pixel in this section do
                # pixel_position = pixel_position_start
                for pixel_index_raw in xrange(
                    pixel_index_start, pixel_index_end + 1
                ):
                    # handle wrap around for xrange
                    pixel_index = pixel_index_raw
                    if pixel_index > pixel_index_max:
                        pixel_index = pixel_index - pixel_count

                    # calculate position in section
                    # pixel_position = pattern.map(
                    #     pixel_index_raw,
                    #     pixel_index_start,
                    #     pixel_index_end,
                    #     stop_start["position"],
                    #     stop_end["position"]
                    # )
                    # optimized variant - (precalculate outside of loop)
                    pixel_position = (
                        (pixel_index_raw - pixel_index_start) *
                        factor_pixel_pos
                    ) + stop_start_position

                    # print(
                    #     "ir: {:< 4} "
                    #     "i: {:< 4} "
                    #     # "pr: {:< 7.6f} "
                    #     "p: {:< 7.6f}"
                    #     .format(
                    #         pixel_index_raw,
                    #         pixel_index,
                    #         # pixel_position_raw,
                    #         pixel_position
                    #         )
                    # )

                    # now we have
                    # pixel_index
                    # pixel_position
                    # stop_start
                    # stop_end
                    # so we can interpolate
                    pixel_data[pixel_index] = self.interpolation_function(
                        pixel_position,
                        stop_start,
                        stop_end
                    )

        return pixel_data

    def _set_data_output(self, data_output, pixel_data):
        color_channels = self.color_channels
        color_channels_count = len(color_channels)
        # print("output:")
        for pixel_index, pixel_values in enumerate(pixel_data):
            channel_index = (pixel_index * color_channels_count)
            # print(
            #     "i: {:< 4} "
            #     "p: {:< 7.6f}  "
            #     "r: {:< 7.6f}  "
            #     "g: {:< 7.6f}  "
            #     "b: {:< 7.6f}  "
            #     "ci: {:< 4} "
            #     .format(
            #         pixel_index,
            #         pixel_values['position'],
            #         pixel_values['red'],
            #         pixel_values['green'],
            #         pixel_values['blue'],
            #         channel_index
            #     )
            # )
            for color_index, color_name in enumerate(color_channels):
                color_value = pixel_values[color_name]
                # convert 0..1 to 0..65535 range
                value_16bit = int(65535 * color_value)
                # convert 16bit to 8 bit
                # check bounds
                # if not (0 <= value_16bit < 65535):
                #     value_16bit = min(max(value_16bit, 0), 65535)
                value_HighByte = value_16bit >> 8
                data_output[channel_index + color_index] = value_HighByte

    def _calculate_step(self):
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

        self.update_globals()

        # pattern specific updates:
        interpolation_type = self.config['type']
        self.interpolation_function = self._interpolate_channels
        # if interpolation_type.startswith("hsv"):
        #     self.interpolation_function = self._interpolate_hsv
        # elif interpolation_type.startswith("channels"):
        #     self.interpolation_function = self._interpolate_channels
        # else:
        #     self.interpolation_function = self._interpolate_channels

        # prepare temp array
        data_output = array.array('B')
        data_output.append(0)
        # multiply so we have a array with total_channel_count zeros in it:
        # this is much faster than a for loop!
        data_output *= self.total_channel_count

        # in milliseconds
        cycle_duration = self.config["cycle_duration"] * 1000

        # calculate stepsize
        # step_count = cycle_duration / update_interval
        # cycle_duration = 1.0
        # update_interval = position_stepsize
        position_stepsize = 1.0 * self.update_interval / cycle_duration

        stops_list = self.config["stops"]
        self.stops_list = stops_list
        stops_count = len(stops_list)
        position_min = stops_list[0]["position"]
        position_max = stops_list[stops_count-1]["position"]
        position_amount = position_max - position_min
        self.position_stepwidth_per_pixel = position_amount / self.pixel_count

        # print("stops_count", stops_count)
        # print("position_min", position_min)
        # print("position_max", position_max)
        # print("position_amount", position_amount)
        # print("position_stepwidth_per_pixel", position_stepwidth_per_pixel)

        ##########################################
        # fill array with meaningfull data according to the pattern :-)

        # calculate new position
        position_current = self.config["position_current"]
        position_current = position_current + position_stepsize
        # check for upper bound
        if position_current >= 1:
            position_current -= 1
        # write position_current back:
        self.config["position_current"] = position_current
        # print("position_current", position_current)
        # print("****")

        # generate values for every pixel
        pixel_data = self._calculate_pixels_for_position(
            position_current
        )

        self._set_data_output(data_output, pixel_data)

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
