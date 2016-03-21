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
        # prepare temp array
        data_output = array.array('B')
        # calculate device_count
        device_count = self.channel_count / 12
        # for devices generate pattern
        for index in range(0, device_count):
            if self.strobe_state:
                data_output.append(10)
                data_output.append(10)
                data_output.append(0)
                data_output.append(0)
                data_output.append(10)
                data_output.append(10)
                data_output.append(0)
                data_output.append(0)
                data_output.append(10)
                data_output.append(10)
                data_output.append(0)
                data_output.append(0)
            else:
                data_output.append(0)
                data_output.append(0)
                data_output.append(10)
                data_output.append(10)
                data_output.append(0)
                data_output.append(0)
                data_output.append(10)
                data_output.append(10)
                data_output.append(0)
                data_output.append(0)
                data_output.append(10)
                data_output.append(10)
        # switch strobe_state
        self.strobe_state = not self.strobe_state
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
            'high': {
                '0': 0,
                '1': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0,
                '6': 0,
                '7': 0,
                '8': 0,
                '9': 0,
                '10': 0,
                '11': 0,
            },
            'low': {
                '0': 0,
                '1': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0,
                '6': 0,
                '7': 0,
                '8': 0,
                '9': 0,
                '10': 0,
                '11': 0,
            },
        },
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
            "\nhit a key to stop the mapper\n" +
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
