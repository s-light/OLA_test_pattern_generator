#!/usr/bin/env python
# coding=utf-8

"""
strobe pattern.

    generates a test pattern:
    strobes all channels between high and low

    history:
        see git commits

    todo:
        ~ all fine :-)
"""


import pattern
import array

##########################################
# globals


##########################################
# functions


##########################################
# classes


class Strobe(Pattern):
    """strobe Pattern Class."""

    def __init__(self, config, config_global):
        """init pattern."""
        self.config_defaults = {
            'xxx': 0
        }
        # python3 syntax
        # super().__init__()
        # python2 syntax
        # super(Pattern, self).__init__()
        # explicit call
        Pattern.__init__(self, config, config_global)

        # inits for this pattern
        self.strobe_state

    def _calculate_step(self):
        """calculate single step."""
        # prepare temp array
        data_output = array.array('B')
        # available attributes:
        # global things
        # self.mode_16bit
        # self.channel_count
        # self.values['off']
        # self.values['low']
        # self.values['high']
        # self.config_global[]
        # fill array with meaningfull data according to the pattern :-)
        # .....

        value_off_hb, value_off_lb = self.calculate_16bit_values(
            self.values['off']
        )
        value_low_hb, value_low_lb = self.calculate_16bit_values(
            self.values['low']
        )
        value_high_hb, value_high_lb = self.calculate_16bit_values(
            self.values['high']
        )

        # calculate device_count
        device_count = self.channel_count / 12

        # get value set
        channel_values = {}
        if self.strobe_state:
            channel_values = config[0]
        else:
            channel_values = config[1]

        # for devices generate pattern
        for index in range(0, device_count):
            # for channel_id, channel_value in channel_values.items():
            # for index in range(0, len(channel_values)):
            #     channel_id = str(index)
            #     channel_value = channel_values[channel_id]
            #     print("ch{}:{}".format(channel_id, channel_value))
            #     data_output.append(channel_value)
            for channel_index, channel_value in enumerate(channel_values):
                # print("ch{}:{}".format(channel_index, channel_value))
                # print(channel_value)
                high_byte = value_off_hb
                low_byte = value_off_lb

                if channel_value is -1:
                    high_byte = value_off_hb
                    low_byte = value_off_lb
                if channel_value is 0:
                    high_byte = value_low_hb
                    low_byte = value_low_lb
                elif channel_value is 1:
                    high_byte = value_high_hb
                    low_byte = value_high_lb

                if self.mode_16bit:
                    data_output.append(high_byte)
                    data_output.append(low_byte)
                else:
                    data_output.append(high_byte)

        # switch strobe_state
        self.strobe_state = not self.strobe_state


        return data_output

##########################################
if __name__ == '__main__':

    print(42*'*')
    print('Python Version: ' + sys.version)
    print(42*'*')
    print(__doc__)
    print(42*'*')
    print("This Module has now stand alone functionality.")
    print(42*'*')

    ##########################################
