#!/usr/bin/env python2
# coding=utf-8

"""
ola test generator.

    generates test pattern for multiple universes.

    history:
        see git commits

    todo:
        ~ all fine :-)
"""


import sys
import os
import time
# import array
# import struct
import signal
import argparse
# import re
import readline
import json


from configdict import ConfigDict
from olathreaded import OLAThread
# from olathreaded import OLAThread_States

import pattern

version = """19.03.2018 12:15 stefan"""


##########################################
# globals


##########################################
# functions


##########################################
# classes

class OLAPattern(OLAThread):
    """Class that extends on OLAThread and generates the patterns."""

    default_config = {
        'system': {
            # 'update_interval': 30,
            'update_interval': 500,
            'mode_16bit': False,
            'use_pixel_dimming': False,
            'global_dimmer': 65535,
            'value': {
                'high': 1000,
                'low': 256,
                'off': 0,
            },
            'pattern_name': 'stop',
            'channel_count': 512,
            'pixel_count': 170,
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
            'update_interval': 5000,
            'colors': {},
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

        self.strobe_state = False

        self.channel_current = 0

        # high and low values:
        # value_low_hb, value_low_lb = self.calculate_16bit_values(
        #     self.config['system']['value']['low']
        # )
        # value_high_hb, value_high_lb = self.calculate_16bit_values(
        #     self.config['system']['value']['high']
        # )

    def init_patterns(self):
        """Load and initialize multi universe pattern."""
        ##########################################
        # load patterns
        if self.verbose:
            print("init patterns:")

        self.pattern = pattern.PatternStrobeUniverse(
            self.config['pattern'],
            self.config['system']
        )

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
        global_dimmer_8bit = 255 * global_dimmer_16bit / 65535
        # print("global_dimmer_8bit", global_dimmer_8bit)
        # global_dimmer_norm = 1.0 * global_dimmer_16bit / 65535
        # print("global_dimmer_norm", global_dimmer_norm)
        # print("")
        # print(len(channels))
        # print(channels)
        for i in range(0, len(channels), 4):
            channels.insert(i, global_dimmer_8bit)
            # channels.insert(i + (i * 3), global_dimmer_8bit)
        # print(len(channels))
        # print(channels)
        return channels

    def _send_universe(self, universe):
        """Send one universe of data."""
        # calculate channel values for pattern
        channels = self.pattern._calculate_step(universe)
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

        # pattern_name = 'strobe'
        # pattern_name = 'channelcheck'
        pattern_name = self.config['system']['pattern_name']

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

        if pattern_name:
            if pattern_name is "run":
                start_universe = self.config['system']['universe']['output']
                universe_list = range(
                    start_universe,
                    start_universe + self.config['system']['universe']['count']
                )
                for universe in universe_list:
                    self._send_universe(universe)


##########################################

def parse_ui__update_interval(user_input):
    """Parse update interval."""
    # try to extract new update interval value
    start_index = user_input.find(':')
    if start_index > -1:
        update_interval_new = \
            user_input[start_index + 1:]
        try:
            update_interval_new = \
                int(update_interval_new)
        except Exception as e:
            print("input not valid. ({})".format(e))
        else:
            my_pattern.config['system']['update_interval'] = (
                update_interval_new
            )
            print("set update_interval to {}.".format(
                my_pattern.config['system']
                ['update_interval']
            ))


def parse_ui__pattern_interval(user_input):
    """Parse patern interval."""
    # try to extract new update interval value
    start_index = user_input.find(':')
    if start_index > -1:
        pattern_interval_new = \
            user_input[start_index + 1:]
        try:
            pattern_interval_new = \
                int(pattern_interval_new)
        except Exception as e:
            print("input not valid. ({})".format(e))
        else:
            my_pattern.config['system']['pattern_interval'] = (
                pattern_interval_new
            )
            print("set pattern_interval to {}.".format(
                my_pattern.config['pattern']
                ['update_interval']
            ))


def parse_ui__universe_value(user_input):
    """Parse universe value."""
    # try to extract universe value
    start_index = user_input.find(':')
    if start_index > -1:
        universe_output_new = \
            user_input[start_index + 1:]
        try:
            universe_output_new = \
                int(universe_output_new)
        except Exception as e:
            print("input not valid. ({})".format(e))
        else:
            my_pattern.config['system']['universe']['output'] = (
                universe_output_new
            )
            print("set universe_output to {}.".format(
                my_pattern.config['system']['universe']['output']
            ))


def parse_ui__universe_count(user_input):
    """Parse universe count."""
    # try to extract universe count
    start_index = user_input.find(':')
    if start_index > -1:
        universe_count_new = \
            user_input[start_index + 1:]
        try:
            universe_count_new = \
                int(universe_count_new)
        except Exception as e:
            print("input not valid. ({})".format(e))
        else:
            my_pattern.config['system']['universe']['count'] = (
                universe_count_new
            )
            print("set universe_count to {}.".format(
                my_pattern.config['system']['universe']['count']
            ))


def parse_ui__pixel_count(user_input):
    """Parse pixel count."""
    # try to extract pixel count
    start_index = user_input.find(':')
    if start_index > -1:
        value_new = \
            user_input[start_index + 1:]
        try:
            value_new = \
                int(value_new)
        except Exception as e:
            print("input not valid. ({})".format(e))
        else:
            my_pattern.config['system']['pixel_count'] = (
                value_new
            )
            print("set pixel_count to {}.".format(
                my_pattern.config['system']['pixel_count']
            ))


def parse_ui__mode_16bit(user_input):
    """Parse mode 16bit."""
    # try to extract mode_16bit value
    start_index = user_input.find(':')
    if start_index > -1:
        mode_value_new = \
            user_input[start_index + 1:]
        try:
            try:
                mode_value_new = int(mode_value_new)
            except Exception as e:
                if mode_value_new.startswith("True"):
                    mode_value_new = True
                else:
                    mode_value_new = False
            else:
                mode_value_new = bool(mode_value_new)
        except Exception as e:
            print("input not valid. ({})".format(e))
        else:
            my_pattern.config['system']['mode_16bit'] = (
                mode_value_new
            )
            print("set mode_16bit to {}.".format(
                my_pattern.config['system']['mode_16bit']
            ))


def parse_ui__values(user_input):
    """Parse values."""
    # try to extract new high and low values
    start_index = user_input.find(':')
    if start_index > -1:
        value_new = user_input[start_index + 1:]
        try:
            value_new = int(value_new)
        except ValueError as e:
            print("input not valid. ({})".format(e))
            raise(e)
        else:
            # bound value
            if value_new > 65535:
                value_new = 65535
            # check for high low or off
            value_name = ''
            if user_input.startswith("vh"):
                value_name = 'high'
            elif user_input.startswith("vl"):
                value_name = 'low'
            elif user_input.startswith("vo"):
                value_name = 'off'
            try:
                my_pattern.config['system']['value'][value_name] = \
                    value_new
            except ValueError as e:
                print(
                    "input not valid. ({})".format(e)
                )
            else:
                print("set value {} to {}.".format(
                    value_name,
                    my_pattern.config['system']
                    ['value'][value_name]
                ))


def parse_ui__global_dimmer(user_input):
    """Parse global dimmer."""
    start_index = user_input.find(':')
    if start_index > -1:
        value_new = \
            user_input[start_index + 1:]
        try:
            value_new = \
                int(value_new)
        except Exception as e:
            print("input not valid. ({})".format(e))
        else:
            my_pattern.config['system']['global_dimmer'] = (
                value_new
            )
            print("set global_dimmer to {}.".format(
                my_pattern.config['system']['global_dimmer']
            ))


def parse_ui__use_pixel_dimming(user_input):
    """Parse use pixel dimming."""
    start_index = user_input.find(':')
    if start_index > -1:
        value_new = \
            user_input[start_index + 1:]
        try:
            value_new = \
                int(value_new)
        except Exception as e:
            print("input not valid. ({})".format(e))
        else:
            my_pattern.config['system']['use_pixel_dimming'] = (
                value_new
            )
            print("set use_pixel_dimming to {}.".format(
                my_pattern.config['system']['use_pixel_dimming']
            ))


def parse_ui__pattern_stop(user_input):
    """Parse pattern_stop."""
    my_pattern.config['system']['pattern_state'] = 'stop'
    print("stopped.")


def parse_ui__pattern_run(user_input):
    """Parse pattern_run."""
    my_pattern.config['system']['pattern_state'] = 'run'
    print("running.")


def parse_ui__quit(user_input):
    """Parse quit."""
    flag_run = False
    return flag_run


def parse_ui__save_config(user_input):
    """Parse save_config."""
    # save config to file
    print("\nwrite config.")
    my_pattern.my_config.write_to_file()


parser_functions = {
    "ui": {
        "info": "update interval",
        "example": "{update_interval} ({update_frequency}Hz)",
        "func": parse_ui__update_interval,
    },
    "pi": {
        "info": "update interval",
        "example": "{update_interval} ({update_frequency}Hz)",
        "func": parse_ui__update_interval,
    },
    "uo": {
        "info": "set universe output",
        "example": "{universe_output}",
        "func": parse_ui__universe_value,
    },
    "uc": {
        "info": "set universe count",
        "example": "{universe_count}",
        "func": parse_ui__universe_count,
    },
    "pc": {
        "info": "set pixel count",
        "example": "{pixel_count}",
        "func": parse_ui__pixel_count,
    },
    "mo": {
        "info": "set mode_16bit",
        "example": "{mode_16bit}",
        "func": parse_ui__mode_16bit,
    },
    "pd": {
        "info": "set use_pixel_dimming",
        "example": "{use_pixel_dimming}",
        "func": parse_ui__use_pixel_dimming,
    },
    "vh": {
        "info": "set value high",
        "example": "{vhigh}",
        "func": parse_ui__values,
    },
    "vl": {
        "info": "set value low",
        "example": "{vlow}",
        "func": parse_ui__values,
    },
    "vo": {
        "info": "set value off",
        "example": "{voff}",
        "func": parse_ui__values,
    },
    "gd": {
        "info": "set global_dimmer",
        "example": "{global_dimmer}",
        "func": parse_ui__global_dimmer,
    },
    "q": {
        "info": "Ctrl+C or 'q' to stop script",
        "example": None,
        "func": parse_ui__quit,
    },
    "s": {
        "info": "stop pattern generator 's'",
        "example": None,
        "func": parse_ui__pattern_stop,
    },
    "r": {
        "info": "run pattern generator 'r'",
        "example": None,
        "func": parse_ui__pattern_run,
    },
    "sc": {
        "info": "save config 'sc'",
        "example": None,
        "func": parse_ui__save_config,
    },
}

parser_functions_order = [
    "s",
    "r",
    "ui",
    "uo",
    "pc",
    "rc",
    "rs",
    "mo",
    "vh",
    "vl",
    "vo",
    "gd",
    "pd",
    "sc",
    "q",
]


def get_parser_function(user_input):
    """Get the parser funciton from the user_input."""
    parser_key = None
    parser_func = None
    for key, value in parser_functions.items():
        if user_input.startswith(key):
            parser_key = key
            parser_func = value['func']
    return (parser_key, parser_func)


def handle_userinput(user_input):
    """Handle userinput in interactive mode."""
    flag_run = True
    parser_key, parser_func = get_parser_function(user_input)
    # print(parser_key, parser_func)
    if parser_func:
        flag_run_temp = parser_func(user_input)
        if flag_run_temp is False:
            flag_run = False
    # else:
    #     parse_ui__pattern_id(user_input)
    return flag_run


def generate_parser_message():
    """Generate parser messages."""
    # print("generate parser message...")
    parser_message = ""
    # for parser_key, parser_obj in parser_functions.items():
    for parser_key in parser_functions_order:
        parser_obj = parser_functions[parser_key]

        # result entry:
        # "  'pc': set pixel count 'pc:{pixel_count}'\n"

        # print("parser_key: ", parser_key)
        # print("parser_obj: ", parser_obj)
        # print("parser_obj['example']: ", parser_obj['example'])
        message_entry = "  '{key}': {info}"
        # print("message_entry: ", message_entry)
        parser_example = None
        if 'example' in parser_obj:
            if parser_obj['example'] is not None:
                parser_example = parser_obj['example'].format(
                    update_frequency=(
                        1000.0 / my_pattern.config['system']['update_interval']
                    ),
                    update_interval=(
                        my_pattern.config['system']['update_interval']
                    ),
                    pixel_count=my_pattern.config['system']['pixel_count'],
                    # repeate_count=my_pattern.config['system']['repeate_count'],
                    # repeate_snake=my_pattern.config['system']['repeate_snake'],
                    universe_output=(
                        my_pattern.config['system']['universe']['output']
                    ),
                    universe_count=(
                        my_pattern.config['system']['universe']['count']
                    ),
                    mode_16bit=my_pattern.config['system']['mode_16bit'],
                    vhigh=my_pattern.config['system']['value']['high'],
                    vlow=my_pattern.config['system']['value']['low'],
                    voff=my_pattern.config['system']['value']['off'],
                    global_dimmer=my_pattern.config['system']['global_dimmer'],
                    use_pixel_dimming=(
                        my_pattern.config['system']['use_pixel_dimming']
                    ),
                )
                message_entry += (
                  " '{key}:{example}'"
                )

        message_entry += "\n"
        message_entry = message_entry.format(
            key=parser_key,
            info=parser_obj['info'],
            example=parser_example,
        )
        parser_message += message_entry
    # print("parser_message: ")
    # print(parser_message)

    # the exchange seems to only work at the first occurency :-?!
    # exchange formating strings in examples
    # print("run formating for examples.")
    # parser_message.format(
    #     update_frequency=(
    #         1000.0/my_pattern.config['system']['update_interval']
    #     ),
    #     update_interval=my_pattern.config['system']['update_interval'],
    #     pixel_count=my_pattern.config['system']['pixel_count'],
    #     repeate_count=my_pattern.config['system']['repeate_count'],
    #     repeate_snake=my_pattern.config['system']['repeate_snake'],
    #     universe_output=my_pattern.config['system']['universe']['output'],
    #     mode_16bit=my_pattern.config['system']['mode_16bit'],
    #     vhigh=my_pattern.config['system']['value']['high'],
    #     vlow=my_pattern.config['system']['value']['low'],
    #     voff=my_pattern.config['system']['value']['off'],
    # )
    # print("done.")
    return parser_message


def generate_menu_message():
    """Build String for menu message/info."""
    pattern_list = ""
    # for index, value in iter(pattern_list):
    for value in my_pattern.pattern_list:
        index = my_pattern.pattern_list.index(value)
        # print(index, value)
        selected = ' '
        if my_pattern.config['system']['pattern_name'] == value:
            selected = '>'
        pattern_list += " {}'{}' {}\n".format(selected, index + 1, value)

    message = (
        "\n" +
        42 * '*' + "\n"
        "select pattern: \n" +
        pattern_list +
        "  's': stop\n"
        "set option: \n" +
        generate_parser_message() +
        42 * '*' + "\n"
        "\n"
    )
    return message


##########################################

def request_userinput(message):
    """Request userinput."""
    flag_run = True
    try:
        if sys.version_info.major >= 3:
            # python3
            user_input = input(message)
        elif sys.version_info.major == 2:
            # python2
            user_input = raw_input(message)
        else:
            # no input methode found.
            user_input = "q"
    except KeyboardInterrupt:
        print("\nstop script.")
        flag_run = False
    except EOFError:
        print("\nstop script.")
        flag_run = False
    except Exception as e:
        print("unknown error: {}".format(e))
        flag_run = False
        print("stop script.")
    else:
        try:
            if len(user_input) > 0:
                flag_run = handle_userinput(user_input)
        except Exception as e:
            print("unknown error: {}".format(e))
            flag_run = False
            print("stop script.")
    return flag_run


def handle_interactive():
    """Handle all interactive running."""
    # wait for user to hit key.
    flag_run = True
    while flag_run:
        message = generate_menu_message()
        flag_run = request_userinput(message)
    return flag_run


def main():
    """Main handling."""
    print(42 * '*')
    print('Python Version: ' + sys.version)
    print(42 * '*')

    ##########################################
    # commandline arguments
    filename_default = "./multiuniverse_test.json"

    parser = argparse.ArgumentParser(
        description="generate test output for multiple universe"
    )
    parser.add_argument(
        "-c",
        "--config",
        help="specify a location for the config file (defaults to {})".format(
            filename_default
        ),
        metavar='FILENAME',
        default=filename_default
    )
    parser.add_argument(
        "-i",
        "--interactive",
        help="run in interactive mode",
        action="store_true"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="show advanced log information",
        action="store_true"
    )
    args = parser.parse_args()

    ##########################################
    # prepare:
    if args.interactive:
        print(42 * '*')
        print(__doc__)
        print(42 * '*')

    # init flag_run
    global flag_run_global
    flag_run_global = False

    # helper
    def _exit_helper(signal, frame):
        """Stop loop."""
        global flag_run_global
        flag_run_global = False

    # setup termination and interrupt handling:
    signal.signal(signal.SIGINT, _exit_helper)
    signal.signal(signal.SIGTERM, _exit_helper)

    global my_pattern
    my_pattern = OLAPattern(args.config, args.verbose)

    # overwritte with pattern name from comandline
    # if "pattern" in args:
    #     my_config.config['system']['pattern_name'] = args.pattern

    my_pattern.start_ola()

    if args.interactive:
        handle_interactive()
    # if not interactive
    else:
        # just wait
        flag_run_global = True
        try:
            while flag_run_global:
                time.sleep(5)
        except KeyboardInterrupt:
            print("\nstop script.")
            flag_run_global = False
    # blocks untill thread has joined.
    my_pattern.stop_ola()


##########################################
if __name__ == '__main__':

    main()

##########################################