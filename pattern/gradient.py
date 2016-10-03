#!/usr/bin/env python2
# coding=utf-8

"""
gradient pattern.

    generates a test pattern:
    gradient

    logic:
        start at: _calculate_step()
            calc (new) current position. (position means time)
            calls: _calculate_pixels_for_position()
                for every pixel:
                    calc pixel_position
                    call _calculate_current_pixel_channel_values()
                        find stops
                            interpolate between stops
                    separate 16bit to 2x8bit
                    set output array with repeating




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

    def _interpolate_hsv(self, pixel_position, stop_start, stop_end):
        """Interpolate with hsv."""
        print("interpolate_hsv")
        result = {}
        # check for exact match
        if pixel_position == stop_start["position"]:
            print("exact")
            red, green, blue = colorsys.hsv_to_rgb(
                stop_start["hue"],
                stop_start["saturation"],
                stop_start["value"]
            )
            result["red"] = red
            result["green"] = green
            result["blue"] = blue
            result["position"] = pixel_position
        else:
            # interpolate all colors
            print("interpolate")
            hsv_values = {}
            for hsv_name in ["hue", "saturation", "value"]:
                hsv_values[hsv_name] = pattern.map(
                    pixel_position,
                    stop_start["position"],
                    stop_end["position"],
                    stop_start[hsv_name],
                    stop_end[hsv_name],
                )
            # multiply with global brightness value:
            global_value = pattern.map_16bit_to_01(self.values['high'])
            hsv_values["value"] = hsv_values["value"] * global_value
            red, green, blue = colorsys.hsv_to_rgb(
                hsv_values["hue"],
                hsv_values["saturation"],
                hsv_values["value"]
            )
            result["red"] = red
            result["green"] = green
            result["blue"] = blue
            result["position"] = pixel_position

        return result

    def _calculate_current_pixel_channel_values(self, pixel_position):
        """Calculate current pixel values."""
        # calculate value:
        # input:
        #     current position
        #     list of way points
        stops_list = self.stops_list

        result = {}
        # print("_calculate_current_pixel_channel_values:")
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
            result = self.interpolation_function(
                pixel_position,
                stop_start,
                stop_end
            )

        return result

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

    def _set_data_output_w_repeat(
        self,
        data_output,
        pixel_index,
        pixel_values_16bit
    ):
        mode_16bit = self.mode_16bit

        for repeate_index in xrange(0, self.repeate_count):
            local_pixel_index = self._calculate_repeat_pixel_index(
                pixel_index,
                repeate_index
            )

            # set colors for pixel:
            for pixel_values_index in xrange(self.color_channels_count):
                color_offset = pixel_values_index
                if mode_16bit:
                    color_offset = color_offset * 2
                # print("color_offset", color_offset)
                output_channel_index = local_pixel_index + color_offset
                # write data
                if mode_16bit:
                    data_output[output_channel_index + 0] = (
                        pixel_values_16bit[pixel_values_index][0]
                    )
                    data_output[output_channel_index + 1] = (
                        pixel_values_16bit[pixel_values_index][1]
                    )
                else:
                    data_output[output_channel_index + 0] = (
                        pixel_values_16bit[pixel_values_index][0]
                    )

    def _calculate_pixels_for_position(
        self,
        data_output,
        position_current
    ):
        pixel_count = self.pixel_count
        color_channels = self.color_channels
        for pixel_index in xrange(0, pixel_count):
            # map gradient to pixel position
            pixel_position_step = 1.0 * pixel_index / pixel_count
            pixel_position = position_current + pixel_position_step
            # check for wrap around
            if pixel_position > 1.0:
                pixel_position -= 1.0
                # print("handle wrap around")

            # print("pixel_position", pixel_position)

            # calculate current values
            pixel_values = self._calculate_current_pixel_channel_values(
                pixel_position
            )

            # pixel_values_16bit = []
            # # pre calculate 16bit values
            # for color_name in color_channels:
            #     # calculate high and low byte
            #     value = pattern.calculate_16bit_parts(
            #         pattern.map_01_to_16bit(
            #             pixel_values[color_name]
            #         )
            #     )
            #     pixel_values_16bit.append(value)

            # is list-comprehension faster?:
            # https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
            # pixel_values_16bit = [pattern.calculate_16bit_parts(
            #     pattern.map_01_to_16bit(
            #         pixel_values[color_name]
            #     )
            # ) for color_name in color_channels]
            # try without the function call
            pixel_values_16bit = [pattern.calculate_16bit_parts(
                int(65535 * pixel_values[color_name])
            ) for color_name in color_channels]

            # print(debug_string)
            # print("0:", data_output)
            self._set_data_output_w_repeat(
                data_output,
                pixel_index,
                pixel_values_16bit
            )
            # print("1:", data_output)

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

        self.update_config()

        # pattern specific updates:
        interpolation_type = self.config['type']
        if interpolation_type.startswith("hsv"):
            self.interpolation_function = self._interpolate_hsv
        elif interpolation_type.startswith("channels"):
            self.interpolation_function = self._interpolate_channels
        else:
            self.interpolation_function = self._interpolate_channels

        self.stops_list = self.config["stops"]

        # prepare temp array
        data_output = array.array('B')
        data_output.append(0)
        # multiply so we have a array with total_channel_count zeros in it:
        # this is much faster than a for loop!
        data_output *= self.total_channel_count

        # fill array with meaningfull data according to the pattern :-)

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
        # print("****")

        # generate values for every pixel
        self._calculate_pixels_for_position(
            data_output,
            position_current
        )

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
