#!/usr/bin/env python2
# coding=utf-8

"""
ola test pattern generator.

    generates some test patterns.
    todo:
        ~ all fine :-)
"""


# import sys
import os
# import time
# import array
# import struct
# import re
# import readline
import json

from configdict import ConfigDict
from olathreaded import OLAThread
# from olathreaded import OLAThread_States

import pattern

##########################################
# classes


class OLAPattern(OLAThread):
    """Class that extends on OLAThread and generates the patterns."""

    default_config = {
        'system': {
            # 'update_interval': 30,
            'update_interval': 500,
            'pattern_interval': 5000,
            'mode_16bit': False,
            'use_pixel_dimming': False,
            'global_dimmer': 65535,
            'value': {
                'high': 1000,
                'low': 256,
                'off': 0,
            },
            'pattern_running': True,
            'pattern_name': 'colors_multiuniverse',
            'channel_count': 512,
            'pixel_count': 170,
            'repeat_count': 4,
            'repeat_snake': True,
            "color_channels": [
                "red",
                "green",
                "blue",
            ],
            'universe': {
                'output': 1,
                'count': 1,
            },
        },
        'pattern': {
            'channelcheck': {},
            'rainbow': {},
            'gradient': {},
            'gradient_integer': {},
            'strobe': {},
            'static': {},
            'colors_multiuniverse': {},
        },
    }

    path_script = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, filename, verbose=False):
        """Init mapper things."""
        # super(OLAThread, self).__init__()
        OLAThread.__init__(self)

        # check for filename
        if not os.path.exists(filename):
            # print(
            #     "filename does not exists.. "
            #     "so we creating a hopefully valid path"
            # )
            # remember config file name
            config_name = os.path.basename(filename)
            # create path on base of script dir.
            # path_to_config = os.path.join(self.path_script, "config")
            path_to_config = self.path_script
            filename = os.path.join(path_to_config, config_name)

        # read config file:
        self.my_config = ConfigDict(self.default_config, filename)
        # print("my_config.config: {}".format(self.my_config.config))
        self.config = self.my_config.config
        # print("config: {}".format(self.config))

        self.verbose = verbose
        if self.verbose:
            print("config: {}".format(
                json.dumps(
                    self.config,
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')
                )
            ))

        # generate absolute path to config files
        path_to_config = os.path.dirname(filename)
        self.config["path_to_config"] = path_to_config

        # this does not work. the link to main config is lost..
        # self.update_interval = self.config['system']['update_interval']
        # self.universe = self.config['system']['universe']['output']
        # self.channel_count = 512
        # self.channel_count = 50
        # self.channel_count = self.config['system']['channel_count']

        self.init_patterns()

        if self.verbose:
            print("--> finished.")
            print("config: {}".format(self.config))

        # high and low values:
        # value_low_hb, value_low_lb = self.calculate_16bit_values(
        #     self.config['system']['value']['low']
        # )
        # value_high_hb, value_high_lb = self.calculate_16bit_values(
        #     self.config['system']['value']['high']
        # )

    def add_pattern(self, pattern_name, pattern_class):
        """Add (create) pattern object to internal pattern list."""
        if pattern_name not in self.config['pattern']:
            self.config['pattern'][pattern_name] = {}
        self.pattern[pattern_name] = pattern_class(
            self.config['pattern'][pattern_name],
            self.config['system']
        )

    def init_patterns(self):
        """Load and initialize all available patterns."""
        ##########################################
        # load patterns
        if self.verbose:
            print("init patterns:")

        self.pattern_list = []
        self.pattern_list.append('stop')
        self.pattern_list.extend(pattern.load_all_submodules())

        # init all patterns:
        self.pattern = {}
        for pattern_class in pattern.Pattern.__subclasses__():
            full_module_name = pattern_class.__module__
            pattern_name = full_module_name.replace("pattern.", "")
            self.add_pattern(pattern_name, pattern_class)

    def ola_connected(self):
        """Register update event callback and switch to running mode."""
        self.wrapper.AddEvent(
            self.config['system']['update_interval'],
            self._calculate_step
        )
        # python3 syntax
        # super().ola_connected()
        # python2 syntax
        # super(OLAThread, self).ola_connected()
        # explicit call
        OLAThread.ola_connected(self)

    def _handle_repeat(self, channels):
        """Handle all pattern repeating things."""
        # this does not work. we have to use the pixel information.
        # otherwiese color-order will get mixed up..
        # pixel_count = self.config['system']['pixel_count']
        repeat_count = self.config['system']['repeat_count']
        repeat_snake = self.config['system']['repeat_snake']
        channels_count = len(channels)
        # print("pixel_count:", pixel_count)
        # print("repeat_snake:", repeat_snake)
        # print("repeat_count:", repeat_count)

        if repeat_count > 0:
            for repeate_index in range(1, repeat_count):
                # print("repeate_index:", repeate_index)
                # normal direction
                # = snake forward
                pixel_range = range(0, channels_count)
                # if repeat_snake and ((repeate_index % 2) > 0):
                if repeat_snake:
                    # print("repeat_snake:", repeat_snake)
                    if ((repeate_index % 2) > 0):
                        # print("(repeate_index % 2):", (repeate_index % 2))
                        # snake back
                        pixel_range = range(channels_count - 1, -1, -1)
                # print("pixel_range:", pixel_range)
                for channel_index in pixel_range:
                    # print("append:", channel_index)
                    try:
                        value = channels[channel_index]
                    except Exception as e:
                        print('error:', e)
                    else:
                        channels.append(value)
        return channels

    def _apply_global_dimmer(self, channels):
        """Apply the global dimmer factor."""
        # print("")
        global_dimmer_16bit = self.config['system']['global_dimmer']
        # print("global_dimmer_16bit", global_dimmer_16bit)
        # 65535 = 255
        #  gd   = gd8
        # global_dimmer_8bit = 255 * global_dimmer_16bit / 65535
        # print("global_dimmer_8bit", global_dimmer_8bit)
        global_dimmer_norm = 1.0 * global_dimmer_16bit / 65535
        # print("global_dimmer_norm", global_dimmer_norm)
        # print("")
        # print(channels)
        for i, ch in enumerate(channels):
            # channels[i] = ch * global_dimmer_8bit
            channels[i] = int(ch * global_dimmer_norm)
        # print(channels)
        return channels

    def _apply_pixel_dimmer(self, channels):
        """Apply the pixel dimmer for APA102."""
        # print("")
        global_dimmer_16bit = self.config['system']['global_dimmer']
        # print("global_dimmer_16bit", global_dimmer_16bit)
        # 65535 = 255
        #  gd   = gd8
        # global_dimmer_8bit = 255 * global_dimmer_16bit / 65535
        global_dimmer_8bit = pattern.map_16bit_to_8bit(global_dimmer_16bit)
        # print("global_dimmer_8bit", global_dimmer_8bit)
        # global_dimmer_norm = 1.0 * global_dimmer_16bit / 65535
        # print("global_dimmer_norm", global_dimmer_norm)
        # print("")
        # print(len(channels))
        # print(channels)
        new_length = (len(channels) / 3) * 4
        for i in range(0, new_length, 4):
            channels.insert(i, global_dimmer_8bit)
            # channels.insert(i + (i * 3), global_dimmer_8bit)
        # print(len(channels))
        # print(channels)
        return channels

    def _send_universe(self, pattern_name, universe):
        """Send one universe of data."""
        if pattern_name:
            if pattern_name in self.pattern:
                # calculate channel values for pattern
                channels = self.pattern[pattern_name]._calculate_step(universe)
                # print(42 * '*')
                # temp_channel_len = len(channels)
                # print('channels len', len(channels))
                # print('channels', channels)
                # channels_rep = self._handle_repeat(channels)
                # print('channels_rep len', len(channels_rep))
                # print('channels_rep', channels_rep)
                # print("channels len: {:5>}; {:5>}".format(
                #     temp_channel_len,
                #     len(channels)
                # ))
                if self.config['system']['use_pixel_dimming']:
                    channels = self._apply_pixel_dimmer(channels)
                else:
                    channels = self._apply_global_dimmer(channels)
                # send frame
                self.dmx_send_frame(universe, channels)

    def _calculate_step(self):
        """Generate test pattern."""
        # register new event (for correct timing as first thing.)
        self.wrapper.AddEvent(
            self.config['system']['update_interval'],
            self._calculate_step
        )
        # print(
        #     "self.config['system']['update_interval']",
        #     self.config['system']['update_interval']
        # )
        # print(
        #     "self.update_interval",
        #     self.update_interval
        # )

        running_state = self.config['system']['pattern_running']
        pattern_name = self.config['system']['pattern_name']
        # print("pattern_name: {}".format(pattern_name))
        # if self.verbose:
        #     print("config: {}".format(
        #         json.dumps(
        #             self.config['system'],
        #             sort_keys=True,
        #             indent=4,
        #             separators=(',', ': ')
        #         )
        #     ))
        #     print("pattern_name: {}".format(pattern_name))
        if running_state:
            if pattern_name:
                start_universe = self.config['system']['universe']['output']
                universe_list = range(
                    start_universe,
                    start_universe + self.config['system']['universe']['count']
                )
                for universe in universe_list:
                    self._send_universe(pattern_name, universe)


##########################################
if __name__ == '__main__':
    import sys
    print(42 * '*')
    print('Python Version: ' + sys.version)
    print(42 * '*')
    print(__doc__)
    print(42 * '*')
    print("This Module has no stand alone functionality.")
    print(42 * '*')

    ##########################################
