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

            # check for exact match
            if pixel_position == stops_list[list_index]["position"]:
                result = stops_list[list_index].copy()
            else:
                # interpolate all colors
                for color_name in self.color_channels:
                    result[color_name] = pattern.map(
                        pixel_position,
                        stops_list[list_index-1]["position"],
                        stops_list[list_index]["position"],
                        stops_list[list_index-1][color_name],
                        stops_list[list_index][color_name],
                    )
                result["position"] = pixel_position

        return result

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
        if self.mode_16bit:
            color_channels_count = color_channels_count * 2

        # in milliseconds
        cycle_duration = self.config["cycle_duration"] * 1000

        # calculate stepsize
        # step_count = cycle_duration / update_interval
        # cycle_duration = 1
        # update_interval = position_stepsize
        position_stepsize = 1.0 * self.update_interval / cycle_duration

        # initilaize our data array to the maximal possible size:
        total_channel_count = (
            self.pixel_count *
            color_channels_count *
            self.repeate_count
        )

        for index in range(0, total_channel_count):
            data_output.append(0)

        # calculate new position
        position_current = position_current + position_stepsize
        # check for upper bound
        if position_current >= 1:
            position_current = 0.0
        # write position_current back:
        self.config["position_current"] = position_current
        # print("position_current", position_current)

        # channel_stepsize = color_channels_count
        # if self.mode_16bit:
        #     channel_stepsize = color_channels_count*2

        # print("****")

        # generate values for every pixel
        for pixel_index in range(0, self.pixel_count):
            # map gradient to pixel position
            pixel_position_step = 1.0 * pixel_index / self.pixel_count
            pixel_position = position_current + pixel_position_step
            # check for wrap around
            if pixel_position > 1.0:
                pixel_position -= 1.0
                # print("handle wrap around")

            # print("pixel_position", pixel_position)

            # calculate current values
            channel_values = self._calculate_current_channel_values(
                pixel_position
            )
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
            for repeate_index in range(0, self.repeate_count):
                pixel_offset = (
                    self.pixel_count *
                    color_channels_count *
                    repeate_index
                )
                local_pixel_index = pixel_offset + (
                    pixel_index * color_channels_count
                )

                # set colors for pixel:
                for color_name in self.color_channels:
                    # calculate high and low byte
                    hb, lb = self._calculate_16bit_values(
                        pattern.map_01_to_16bit(
                            channel_values[color_name]
                        )
                    )
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

            # print(debug_string)

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
