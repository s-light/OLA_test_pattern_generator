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
            "color_channels": [
                "red",
                "green",
                "blue",
            ],
            "stops": [
                {
                    "position": 0,
                    "red": 1,
                    "green": 1,
                    "blue": 1,
                },
                {
                    "position": 0.25,
                    "red": 1,
                    "green": 0,
                    "blue": 0,
                },
                {
                    "position": 0.5,
                    "red": 0,
                    "green": 1,
                    "blue": 0,
                },
                {
                    "position": 0.75,
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

    def _calculate_current_channel_values(self, pixel_position):
        """Calculate current channel values."""
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
                for color_name in self.config["color_channels"]:
                    result[color_name] = pattern.map(
                        pixel_position,
                        0,
                        1,
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

        channel_stepsize = color_channels_count
        if self.mode_16bit:
            channel_stepsize = color_channels_count*2

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

            # calculate current values
            channel_values = self._calculate_current_channel_values(
                pixel_position
            )

            # set all channels
            for color_name in self.config["color_channels"]:

                # calculate high and low byte
                hb, lb = self._calculate_16bit_values(
                    pattern.map_01_to_16bit(
                        channel_values[color_name]
                    )
                )
                # write data
                if self.mode_16bit:
                    data_output.append(hb)
                    data_output.append(lb)
                else:
                    data_output.append(hb)

            # old easy rainbow :-)
            # saturation = 1
            # value = pattern.map_16bit_to_01(self.values['high'])
            # # print("hue: {}".format(hue))
            # # print("value: {}".format(value))
            #
            # r, g, b = colorsys.hsv_to_rgb(pixel_hue, saturation, value)
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
            #
            # if self.mode_16bit:
            #     data_output.append(r_hb)
            #     data_output.append(r_lb)
            #     data_output.append(g_hb)
            #     data_output.append(g_lb)
            #     data_output.append(b_hb)
            #     data_output.append(b_lb)
            #     data_output.append(0)
            #     data_output.append(0)
            # else:
            #     data_output.append(r_hb)
            #     data_output.append(g_hb)
            #     data_output.append(b_hb)

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
