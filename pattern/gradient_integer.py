#!/usr/bin/env python2
# coding=utf-8

"""
gradient pattern.

    generates a test pattern:
    gradient
    this version only used integer values.
    position values 0..1000000 (*A)
    color values 0..655535 (16bit)

    *A: this is enough for about 5h fade duration at 20ms/50Hz updaterate
    for some more information see 'resolution_helper.ods'

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


class Gradient_Integer(pattern.Pattern):
    """Gradient Pattern Class."""

    def __init__(self, config, config_global):
        """Init pattern."""
        self.config_defaults = {
            "cycle_duration": 10000,
            "position_current": 0,
            "type": "channel",
            "stops": [
                {
                    "position": 0,
                    "red": 65535,
                    "green": 65535,
                    "blue": 65535,
                },
                {
                    "position": 300000,
                    "red": 65535,
                    "green": 0,
                    "blue": 0,
                },
                {
                    "position": 700000,
                    "red": 0,
                    "green": 65535,
                    "blue": 0,
                },
                {
                    "position": 1000000,
                    "red": 0,
                    "green": 0,
                    "blue": 65535,
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

    def _interpolate_hsv(self, pixel_position, stop_start, stop_end):
        """Interpolate with hsv."""
        print("interpolate_hsv -- TODO....")
        result = {}
        # check for exact match
        result["red"] = 8000
        result["green"] = 0
        result["blue"] = 20000
        result["position"] = pixel_position
        return result

    def _calculate_current_channel_values(self, pixel_position):
        """Calculate current pixel values."""
        # calculate value:
        # input:
        #     current position
        #     list of way points
        stops_list = self.config["stops"]

        result = {}
        # print("_calculate_current_channel_values:")
        # print("pixel_position:", pixel_position)
        # check bounds
        if pixel_position <= stops_list[0]["position"]:
            # print("min.")
            result = stops_list[0].copy()
        elif pixel_position >= stops_list[len(stops_list)-1]["position"]:
            # print("max.")
            result = stops_list[len(stops_list)-1].copy()
        else:
            # print("search:")
            # we search for the correct stops
            list_index = 1
            while pixel_position > stops_list[list_index]["position"]:
                list_index += 1

            # now list_index contains the first stop
            # where position is < pixel_position

            # interpolate between stops:
            stop_start = stops_list[list_index-1]
            stop_end = stops_list[list_index]
            interpolation_type = self.config['type']
            if interpolation_type.startswith("hsv"):
                result = self._interpolate_hsv(
                    pixel_position,
                    stop_start,
                    stop_end
                )
            elif interpolation_type.startswith("channels"):
                result = self._interpolate_channels(
                    pixel_position,
                    stop_start,
                    stop_end
                )
            else:
                result = self._interpolate_channels(
                    pixel_position,
                    stop_start,
                    stop_end
                )

        return result

    def _calculate_repeat_pixel_index(
        self,
        pixel_index,
        repeate_index,
        color_channels_count
    ):
        pixel_offset = (
            self.pixel_count *
            color_channels_count *
            repeate_index
        )
        local_pixel_index = pixel_offset + (
            pixel_index * color_channels_count
        )
        if self.repeat_snake:
            # every odd index
            if ((repeate_index % 2) > 0):
                # total_pixel_channel_count = (
                #     self.pixel_count * color_channels_count
                # )
                # local_pixel_index = local_pixel_index
                local_pixel_index = pixel_offset + (
                    ((self.pixel_count - 1) - pixel_index) *
                    color_channels_count
                )
                # print("local_pixel_index", local_pixel_index)
        return local_pixel_index

    def _set_data_output_w_repeat(
        self,
        data_output,
        pixel_index,
        channel_values_16bit,
        color_channels_count
    ):

        for repeate_index in range(0, self.repeat_count):
            local_pixel_index = self._calculate_repeat_pixel_index(
                pixel_index,
                repeate_index,
                color_channels_count
            )

            # set colors for pixel:
            for color_name in self.color_channels:
                # get high and low byte
                hb = channel_values_16bit[color_name]['hb']
                lb = channel_values_16bit[color_name]['lb']
                # debug output
                # if color_name.startswith("blue"):
                #     debug_string += (
                #         "{:>6}: "
                #         "h {:>3} "
                #         "l {:>3}".format(
                #             color_name,
                #             hb,
                #             lb
                #         )
                #     )

                # get channel index with color offset
                color_offset = self.color_channels.index(color_name)
                if self.mode_16bit:
                    color_offset = color_offset * 2
                # print("color_offset", color_offset)
                channel_index = local_pixel_index + color_offset
                # write data
                if self.mode_16bit:
                    data_output[channel_index + 0] = hb
                    data_output[channel_index + 1] = lb
                else:
                    data_output[channel_index + 0] = hb

    def _calculate_pixels_for_position(
        self,
        data_output,
        position_current,
        color_channels_count
    ):
        for pixel_index in range(0, self.pixel_count):
            # map gradient to pixel position
            pixel_position_step = 1000000 * pixel_index / self.pixel_count
            pixel_position = position_current + pixel_position_step
            # check for wrap around
            if pixel_position > 1000000:
                pixel_position -= 1000000
                # print("handle wrap around")

            # print("pixel_position", pixel_position)

            # calculate current values
            channel_values = self._calculate_current_channel_values(
                pixel_position
            )
            # print(channel_values)
            # print(
            #     "pixel_position {:<19}"
            #     " -> "
            #     # "channel_values", channel_values
            #     "pos {:<19}"
            #     "red {:<19}"
            #     "green {:<19}"
            #     "blue {:<19}".format(
            #         pixel_position,
            #         channel_values["position"],
            #         channel_values["red"],
            #         channel_values["green"],
            #         channel_values["blue"]
            #     )
            # )

            # debug_string = (
            #     "pixel_position {:<19}"
            #     " -> "
            #     # "channel_values", channel_values
            #     # "pos {:<19}"
            #     # "red {:<19}"
            #     # "green {:<19}"
            #     "blue {:<19}".format(
            #         pixel_position,
            #         # channel_values["position"],
            #         # channel_values["red"],
            #         # channel_values["green"],
            #         channel_values["blue"]
            #     )
            # )

            channel_values_16bit = {}
            # pre calculate 16bit values
            for color_name in self.color_channels:
                # calculate high and low byte
                hb, lb = self._calculate_16bit_values(
                        channel_values[color_name]
                )
                values = {}
                values['hb'] = hb
                values['lb'] = lb
                channel_values_16bit[color_name] = values

            # print(debug_string)
            # print("0:", data_output)
            self._set_data_output_w_repeat(
                data_output,
                pixel_index,
                channel_values_16bit,
                color_channels_count
            )
            # print("1:", data_output)

    def _calculate_step(self, universe):
        """Calculate single step."""
        # prepare temp array
        data_output = array.array('B')
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
        # fill array with meaningfull data according to the pattern :-)
        # .....

        # print("")

        position_current = self.config["position_current"]

        color_channels_count = len(self.color_channels)
        if self.mode_16bit:
            color_channels_count = color_channels_count * 2

        # in milliseconds
        cycle_duration = self.config["cycle_duration"]

        # calculate stepsize
        # step_count = cycle_duration / update_interval
        # cycle_duration = 1000000
        # update_interval = position_stepsize
        position_stepsize = 1000000 * self.update_interval / cycle_duration

        # initilaize our data array to the maximal possible size:
        total_channel_count = (
            self.pixel_count *
            color_channels_count *
            self.repeat_count
        )

        for index in range(0, total_channel_count):
            data_output.append(0)

        # calculate new position
        position_current = position_current + position_stepsize
        # check for upper bound
        if position_current >= 1000000:
            position_current = 0
        # write position_current back:
        self.config["position_current"] = position_current
        # print("position_current", position_current)

        # channel_stepsize = color_channels_count
        # if self.mode_16bit:
        #     channel_stepsize = color_channels_count*2

        # print("****")

        # generate values for every pixel
        # this function manipulates data_output.
        self._calculate_pixels_for_position(
            data_output,
            position_current,
            color_channels_count
        )

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
