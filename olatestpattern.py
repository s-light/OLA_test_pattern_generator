#!/usr/bin/env python
# coding=utf-8

"""
ola test pattern generator.

    generates some test patterns.

    history:
        see git commits

    todo:
        ~ all fine :-)
"""


import sys
import os
import array

from configdict import ConfigDict
from olathreaded import OLAThread, OLAThread_States


version = """08.03.2016 12:30 stefan"""


##########################################
# globals


##########################################
# functions


##########################################
# classes


class OLAPattern(OLAThread):
    """Class that extends on OLAThread and generates the patterns."""

    def __init__(self, config):
        """init mapper things."""
        # super(OLAThread, self).__init__()
        OLAThread.__init__(self)

        self.config = config
        # print("config: {}".format(self.config))

        self.update_interval = self.config['system']['update_interval']

        self.universe = self.config['universe']['output']
        # self.channel_count = 512
        # self.channel_count = 50
        self.channel_count = self.config['universe']['channel_count']

        self.strobe_state = False

    def ola_connected(self):
        """register update event callback and switch to running mode."""
        self.wrapper.AddEvent(self.update_interval, self._calculate_step)
        # python3 syntax
        # super().ola_connected()
        # python2 syntax
        # super(OLAThread, self).ola_connected()
        # explicit call
        OLAThread.ola_connected(self)

    def _calculate_step(self):
        """generate test pattern."""
        # register new event (for correct timing as first thing.)
        self.wrapper.AddEvent(self.update_interval, self._calculate_step)
        # self._calculate_step_strobe(
        #     self.config['pattern']['strobe']
        # )
        self._calculate_step_channelcheck(
            self.config['pattern']['channelcheck']
        )

    def _calculate_step_strobe(self, config):
        """generate test pattern 'strobe'."""
        # prepare temp array
        data_output = array.array('B')
        # calculate device_count
        device_count = self.channel_count / 12
        # get value set
        channel_values = {}
        if self.strobe_state:
            channel_values = config['high']
        else:
            channel_values = config['low']
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
                data_output.append(int(channel_value))
        # switch strobe_state
        self.strobe_state = not self.strobe_state
        # send frame
        self.dmx_send_frame(
            self.config['universe']['output'],
            data_output
        )

    def _calculate_step_channelcheck(self, config):
        """generate test pattern 'channelcheck'."""
        # prepare temp array
        data_output = array.array('B')

        if not hasattr(config, 'channel_current'):
            config['channel_current'] = 0

        # for devices generate pattern
        for index in range(0, self.config['universe']['channel_count']):
            channel_value = 0
            if index is config['channel_current']:
                channel_value = config['on']
            data_output.append(channel_value)

        if (
            config['channel_current'] <
            self.config['universe']['channel_count']
        ):
            config['channel_current'] = config['channel_current'] + 1
        else:
            config['channel_current'] = 0

        # send frame
        self.dmx_send_frame(
            self.config['universe']['output'],
            data_output
        )


##########################################
if __name__ == '__main__':

    print(42*'*')
    print('Python Version: ' + sys.version)
    print(42*'*')
    print(__doc__)
    print(42*'*')

    # parse arguments
    filename = "pattern.json"
    # only use args after script name
    arg = sys.argv[1:]
    if not arg:
        print("using standard values.")
        print(" Allowed parameters:")
        print("   filename for config file       (default='map.json')")
        print("")
    else:
        filename = arg[0]
        # if len(arg) > 1:
        #     pixel_count = int(arg[1])
    # print parsed argument values
    print('''values:
        filename :{}
    '''.format(filename))

    default_config = {
        'system': {
            # 'update_interval': 30,
            'update_interval': 2000,
            '16bitMode': False,
        },
        'universe': {
            'output': 2,
            'channel_count': 512,
        },
        'pattern': {
            'channelcheck': {
                'on': 255,
                '16bit': True,
                'wrapp_around_count': 64,
            },
            'strobe': {
                'high': [
                    # 1
                    255,
                    0,
                    0,
                    0,
                    # 2
                    0,
                    255,
                    0,
                    0,
                    # 3
                    0,
                    0,
                    255,
                    0,
                    # 4
                    0,
                    0,
                    0,
                    255,
                ],
                'low': [
                    # 1
                    10000,
                    0,
                    0,
                    0,
                    # 2
                    0,
                    10000,
                    0,
                    0,
                    # 3
                    0,
                    0,
                    10000,
                    0,
                    # 4
                    0,
                    0,
                    0,
                    10000,
                ],
            },
        },
        # pattern with variable channel ids
        # 'pattern': {
        #     'high': {
        #         # rgb 1
        #         '0': 0,
        #         '1': 255,
        #         '2': 0,
        #         '3': 255,
        #         '4': 0,
        #         '5': 255,
        #         # rgb 2
        #         '6': 0,
        #         '7': 255,
        #         '8': 0,
        #         '9': 255,
        #         '10': 0,
        #         '11': 255,
        #         # rgb 3
        #         '12': 0,
        #         '13': 255,
        #         '14': 0,
        #         '15': 255,
        #         '16': 0,
        #         '17': 255,
        #         # rgb 3
        #         '18': 0,
        #         '19': 255,
        #         '20': 0,
        #         '21': 255,
        #         '22': 0,
        #         '23': 255,
        #         # white 1
        #         '24': 0,
        #         '25': 255,
        #         '26': 0,
        #         '27': 0,
        #         '28': 0,
        #         '29': 0,
        #         # white 2
        #         '30': 0,
        #         '31': 255,
        #         '32': 0,
        #         '33': 0,
        #         '44': 0,
        #         '45': 0,
        #         # white 3
        #         '46': 0,
        #         '47': 255,
        #         '48': 0,
        #         '49': 0,
        #         '50': 0,
        #         '51': 0,
        #         # white 3
        #         '52': 0,
        #         '53': 255,
        #         '54': 0,
        #         '55': 0,
        #         '56': 0,
        #         '57': 0,
        #     },
        #     'low': {
        #         # rgb 1
        #         '0': 0,
        #         '1': 1,
        #         '2': 0,
        #         '3': 1,
        #         '4': 0,
        #         '5': 1,
        #         # rgb 2
        #         '6': 0,
        #         '7': 1,
        #         '8': 0,
        #         '9': 1,
        #         '10': 0,
        #         '11': 1,
        #         # rgb 3
        #         '12': 0,
        #         '13': 1,
        #         '14': 0,
        #         '15': 1,
        #         '16': 0,
        #         '17': 1,
        #         # rgb 3
        #         '18': 0,
        #         '19': 1,
        #         '20': 0,
        #         '21': 1,
        #         '22': 0,
        #         '23': 1,
        #         # white 1
        #         '24': 0,
        #         '25': 1,
        #         '26': 0,
        #         '27': 0,
        #         '28': 0,
        #         '29': 0,
        #         # white 2
        #         '30': 0,
        #         '31': 1,
        #         '32': 0,
        #         '33': 0,
        #         '44': 0,
        #         '45': 0,
        #         # white 3
        #         '46': 0,
        #         '47': 1,
        #         '48': 0,
        #         '49': 0,
        #         '50': 0,
        #         '51': 0,
        #         # white 3
        #         '52': 0,
        #         '53': 1,
        #         '54': 0,
        #         '55': 0,
        #         '56': 0,
        #         '57': 0,
        #     },
        # },
    }
    my_config = ConfigDict(default_config, filename)
    print("my_config.config: {}".format(my_config.config))

    my_pattern = OLAPattern(my_config.config)

    my_pattern.start_ola()

    # wait for user to hit key.
    try:
        raw_input(
            "\n\n" +
            42*'*' +
            "\nhit a key to stop the pattern generator\n" +
            42*'*' +
            "\n\n"
        )
    except KeyboardInterrupt:
        print("\nstop.")

    # blocks untill thread has joined.
    my_pattern.stop_ola()

    # as last thing we save the current configuration.
    print("\nwrite config.")
    my_config.write_to_file()

    ##########################################
