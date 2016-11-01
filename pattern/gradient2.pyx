# coding=utf-8
# cython: profile=True

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

# import colorsys
from cython cimport view
from cpython cimport array
import array

import pattern

##########################################
# globals


##########################################
# functions


##########################################
# classes

class Gradient_Section(object):
    """Gradient_Section Helper Class."""

    def __init__(
        self, stop_start, stop_end, pixel_index_max, pixel_channels_count
    ):
        """Init section."""
        self.start_stop = stop_start
        self.start_position = stop_start['position']
        self.start_values = stop_start['values']
        self.end_stop = stop_end
        self.end_position = stop_end['position']
        self.end_values = stop_end['values']

        # precalculate
        self.position_diff = self.end_position - self.start_position

        # fake calculation for pixel count in section:
        # (not optimized... just copy&paste)
        position_current = 0
        stop_start_position = stop_start["position"]
        stop_end_position = stop_end["position"]
        pixel_position_start = stop_start_position + position_current
        pixel_position_end = stop_end_position + position_current
        pixel_index_start = int(
            pixel_position_start * pixel_index_max
        )
        pixel_index_end = int(
            pixel_position_end * pixel_index_max
        )
        if pixel_index_end < pixel_index_start:
            pixel_index_end += pixel_index_max

        self.pixel_diff = pixel_index_end - pixel_index_start

        self.factor_pixel_pos = None

        self.color_factors = []
        self.color_factors.append(0)
        self.color_factors *= pixel_channels_count
        # cdef float[:] color_factors_internal = array.array(
        #     "f",
        #     pixel_channels_count
        # )
        # cdef float[:] color_factors_internal = view.array(
        #     shape=(pixel_channels_count),
        #     itemsize=sizeof(float),
        #     format="f"
        # )
        # self.color_factors = color_factors_internal

        self.has_pixel = False
        if self.pixel_diff > 0:
            self.has_pixel = True
            # guarded by pixel_diff > 0
            # --> otherwise we could get a divide by zero execption
            self.factor_pixel_pos = self.position_diff / self.pixel_diff

            for color_index in xrange(pixel_channels_count):
                # self.color_diffs = {}
                # self.color_diffs[color_name] = (
                #     (stop_end[color_name] - stop_start[color_name])
                # )
                self.color_factors[color_index] = (
                    (
                        self.end_values[color_index] -
                        self.start_values[color_index]
                    ) /
                    self.position_diff
                )


class Gradient2(pattern.Pattern):
    """Gradient2 Pattern Class."""

    def __init__(self, config, config_global):
        """Init pattern."""
        self.config_defaults = {
            "cycle_duration": 10,
            "position_current": 0,
            "type": "channel",
            "pixel_channel_map": [
                "red",
                "green",
                "blue",
            ],
            # default = full rainbow
            "stops": [
                {
                    "position": 0,
                    "values": [
                        1,
                        0,
                        0,
                    ],
                },
                {
                    "position": 0.16,
                    "values": [
                        1,
                        1,
                        0,
                    ],
                },
                {
                    "position": 0.34,
                    "values": [
                        0,
                        1,
                        0,
                    ],
                },
                {
                    "position": 0.5,
                    "values": [
                        0,
                        1,
                        1,
                    ],
                },
                {
                    "position": 0.64,
                    "values": [
                        0,
                        0,
                        1,
                    ],
                },
                {
                    "position": 0.78,
                    "values": [
                        1,
                        0,
                        1,
                    ],
                },
                {
                    "position": 1,
                    "values": [
                        1,
                        0,
                        0,
                    ],
                }
            ],
        }
        # python3 syntax
        # super().__init__()
        # python2 syntax
        # super(pattern.Pattern, self).__init__()
        # explicit call
        pattern.Pattern.__init__(self, config, config_global)

        self.update_config()

    # update / precalculate helper

    def update_config(self):
        """Update all configuration things that can be precalculated."""
        # call parent class function:
        pattern.Pattern.update_config(self)

        # pattern specific precalculations
        self.pixel_channels = self.config['pixel_channel_map']
        self.pixel_channels_count = len(self.pixel_channels)

        self.total_channel_count = (
            self.pixel_count *
            self.pixel_channels_count
        )
        # this total_channel_count means 8 bit channels...
        if self.mode_16bit:
            self.total_channel_count *= 2

        if self.repeate_count > 0:
            self.total_channel_count *= self.repeate_count

        interpolation_type = self.config['type']
        self.interpolation_function = self._interpolate_channels
        # if interpolation_type.startswith("hsv"):
        #     self.interpolation_function = self._interpolate_hsv
        # elif interpolation_type.startswith("channels"):
        #     self.interpolation_function = self._interpolate_channels
        # else:
        #     self.interpolation_function = self._interpolate_channels

        # prepare temp array
        self.data_output = array.array('B')
        self.data_output.append(0)
        # multiply so we have a array with total_channel_count zeros in it:
        # this is much faster than a for loop!
        self.data_output *= self.total_channel_count

        # self.pixel_data = []
        # self.pixel_data.append(0)
        # self.pixel_data *= self.pixel_count

        # predefine pixel_data with sub elements:
        # https://docs.python.org/3/faq/programming.html#faq-multidimensional-list
        self.pixel_data = [
            [0] * self.pixel_channels_count for i in range(self.pixel_count)
        ]
        # setup pixel data as cython array
        # pixel_data_raw = view.array(
        #     shape=(self.pixel_count, self.pixel_channels_count),
        #     itemsize=sizeof(float),
        #     format="f"
        # )
        # init memoryview
        # http://docs.cython.org/en/latest/src/userguide/memoryviews.html#using-memoryviews
        # http://cython.readthedocs.io/en/latest/src/tutorial/array.html#safe-usage-with-memory-views
        # cdef float[:,:] pixel_data_view = pixel_data_raw
        # self.pixel_data = pixel_data_view
        # use in function definitions: float[:,:] pixel_data not None


        # in milliseconds
        cycle_duration = self.config["cycle_duration"] * 1000

        # calculate stepsize
        # step_count = cycle_duration / update_interval
        # cycle_duration = 1.0
        # update_interval = position_stepsize
        self.position_stepsize = 1.0 * self.update_interval / cycle_duration

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

        # localize for speed?!
        # pixel_channels_count = self.pixel_channels_count

        # precalculate sections:
        self.sections = []
        # for every section in the stops_list
        for stop_index, stop_start in enumerate(stops_list):
            if stop_index < (stops_count-1):
                stop_end = stops_list[stop_index+1]
            else:
                stop_end = stops_list[0]

            self.sections.append(
                Gradient_Section(
                    stop_start,
                    stop_end,
                    self.pixel_index_max,
                    self.pixel_channels_count
                )
            )

    # generator helper functions

    def _interpolate_channels(self, pixel_position, section, pixel_data_this):
        """Interpolate with channels."""
        # print("interpolate_channels")
        # result = {
        #     'position': -1,
        #     'values': []
        # }
        # result = []
        # result.append(0)
        # result *= self.pixel_channels_count

        # check for exact match
        # if pixel_position == section.start_position:
        #     # copy
        #     result = section.start_values[:]
        # else:
        # interpolate all colors
        for pixel_channel_index in xrange(self.pixel_channels_count):
            # result[pixel_channel_index] = pattern.map(
            #     pixel_position,
            #     section.start_position,
            #     section.end_position,
            #     stop_start[pixel_channel_index],
            #     stop_end[pixel_channel_index],
            # )
            pixel_data_this[pixel_channel_index] = (
                (
                    (pixel_position - section.start_position) *
                    section.color_factors[pixel_channel_index]
                ) + section.start_values[pixel_channel_index]
            )

        # result["position"] = pixel_position

        # return result

    def _calculate_pixels_for_position(self, float position_current):
        """Calculate pixels for all positions."""
        # print("\n"*2)
        # print("_calculate_pixels_for_position()")
        # print("position_current {: <.9f}".format(position_current))

        cdef unsigned int pixel_count
        cdef unsigned int pixel_index_max
        cdef unsigned int pixel_channels_count
        pixel_count = self.pixel_count
        pixel_index_max = self.pixel_index_max
        pixel_channels_count = self.pixel_channels_count

        pixel_data = self.pixel_data

        # definitions for inside section-loop:
        cdef float pixel_position_start
        cdef float pixel_position_end
        cdef unsigned int pixel_index_start
        cdef unsigned int pixel_index_end
        # section helper
        cdef float section_factor_pixel_pos
        cdef float section_start_position
        cdef float section_end_position
        cdef float[:] section_start_values
        cdef float[:] section_color_factors
        # section_start_values = None
        # section_color_factors = None

        # definitions for pixel-loop:
        cdef size_t pixel_index_raw
        cdef size_t pixel_index
        cdef float pixel_position

        # definitions for pixel_channel-loop:
        cdef size_t pixel_channel_index

        for section in self.sections:
            # skip sections without pixels.
            if section.has_pixel:
                # update global helpers
                section_factor_pixel_pos = section.factor_pixel_pos
                section_start_position = section.start_position
                section_end_position = section.end_position
                section_start_values = section.start_values
                section_color_factors = section.color_factors

                pixel_position_start = (
                    section_start_position + position_current
                )
                pixel_position_end = (
                    section_end_position + position_current
                )

                pixel_index_start = int(
                    pixel_position_start * pixel_index_max
                )
                pixel_index_end = int(
                    pixel_position_end * pixel_index_max
                )

                if pixel_index_end < pixel_index_start:
                    pixel_index_end += pixel_index_max



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
                    # optimized variant - (precalculate outside of loop)
                    pixel_position = (
                        (pixel_index_raw - pixel_index_start) *
                        section_factor_pixel_pos
                    ) + section_start_position

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

                    # so now we can interpolate
                    # self.interpolation_function(
                    #     pixel_position,
                    #     section,
                    #     pixel_data[pixel_index]
                    # )
                    for pixel_channel_index in xrange(pixel_channels_count):
                        # interpolate
                        pixel_data[pixel_index][pixel_channel_index] = (
                            (
                                (pixel_position - section_start_position) *
                                section_color_factors[pixel_channel_index]
                            ) + section_start_values[pixel_channel_index]
                        )

        return pixel_data

    # output writing

    def _set_data_output(self, data_output, float[:,:] pixel_data not None):
        cdef unsigned int pixel_channels_count
        pixel_channels_count = self.pixel_channels_count
        cdef unsigned int p_8bit_ch_count
        p_8bit_ch_count = pixel_channels_count
        if self.mode_16bit:
            p_8bit_ch_count *= 2

        # print("output:")
        # declare variables used inside loops:
        cdef size_t pixel_index
        cdef float[:] pixel_values

        cdef size_t channel_index
        cdef size_t pixel_channel_index

        cdef float value_float
        cdef unsigned int value_16bit
        cdef unsigned int value_HighByte

        for pixel_index in xrange(len(pixel_data)):
            pixel_values = pixel_data[pixel_index]
            channel_index = (pixel_index * p_8bit_ch_count)
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
            for pixel_channel_index in xrange(pixel_channels_count):
                value_float = pixel_values[pixel_channel_index]
                # convert 0..1 to 0..65535 range
                value_16bit = int(65535 * value_float)
                # convert 16bit to 8 bit
                # check bounds
                # if not (0 <= value_16bit < 65535):
                #     value_16bit = min(max(value_16bit, 0), 65535)
                value_HighByte = value_16bit >> 8
                data_output[
                    channel_index + pixel_channel_index
                ] = value_HighByte

    def _calculate_repeat_pixel_index(self, pixel_index, repeate_index):
        pixel_offset = (
            self.pixel_count *
            self.color_channels_count *
            repeate_index
        )
        local_pixel_index = pixel_offset + (
            pixel_index * self.color_channels_count
        )
        if self.repeate_snake:
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
        return local_pixel_index

    def _set_data_output_w_repeat(self, data_output, pixel_data):
        mode_16bit = self.mode_16bit
        pixel_channels_count = self.pixel_channels_count
        p_8bit_ch_count = pixel_channels_count
        if mode_16bit:
            p_8bit_ch_count *= 2

        color_channels = self.color_channels
        color_channels_count = len(color_channels)
        # print("output:")
        for pixel_index, pixel_values in enumerate(pixel_data):
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

            # for every color channel
            for pixel_channel_index in xrange(pixel_channels_count):
                p_ch_offset = pixel_channel_index
                if mode_16bit:
                    p_ch_offset *= 2

                # calculate 16bit parts
                value_float = pixel_values[pixel_channel_index]
                # convert 0..1 to 0..65535 range
                value_16bit = int(65535 * value_float)
                # convert 16bit to 8 bit
                # check bounds
                # if not (0 <= value_16bit < 65535):
                #     value_16bit = min(max(value_16bit, 0), 65535)
                value_HighByte = value_16bit >> 8
                value_LowByte = value_16bit & 255

                # for every repeate index
                for repeate_index in xrange(0, self.repeate_count):
                    local_pixel_index = self._calculate_repeat_pixel_index(
                        pixel_index,
                        repeate_index
                    )
                    output_channel_index = local_pixel_index + p_ch_offset
                    if mode_16bit:
                        data_output[output_channel_index + 0] = (
                            value_HighByte
                        )
                        data_output[output_channel_index + 1] = (
                            value_LowByte
                        )
                    else:
                        data_output[output_channel_index + 0] = (
                            value_HighByte
                        )

    # main generator funciton

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

        # now is called if config has changed from external
        # self.update_config()

        ##########################################
        # fill array with meaningfull data according to the pattern :-)

        # calculate new position
        position_current = self.config["position_current"]
        position_current = position_current + self.position_stepsize
        # check for upper bound
        if position_current >= 1:
            position_current -= 1
        # write position_current back:
        self.config["position_current"] = position_current
        # print("position_current", position_current)
        # print("****")

        # generate values for every pixel
        # fills self.pixel_data
        self._calculate_pixels_for_position(
            position_current
        )

        if self.repeate_count > 0:
            self._set_data_output_w_repeat(self.data_output, self.pixel_data)
        else:
            self._set_data_output(self.data_output, self.pixel_data)

        return self.data_output

##########################################
if __name__ == '__main__':
    import sys
    print(42*'*')
    print('Python Version: ' + sys.version)
    print(42*'*')
    print(__doc__)
    print(42*'*')
    print("This Module has no stand alone functionality.")
    print(42*'*')

    ##########################################
