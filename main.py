#!/usr/bin/env python2
# coding=utf-8

"""
ola test pattern generator.

    generates some test patterns.
"""


import sys
import time
# import array
# import struct
import signal
import argparse
# import re
# import readline

from ola_pattern import OLAPattern
from userinput import request_userinput

version = """20.03.2018 12:00 stefan"""


##########################################
# globals


##########################################
# functions

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
                my_pattern.config['system']
                ['pattern_interval']
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


def parse_ui__repeat_count(user_input):
    """Parse repeate count."""
    # try to extract repeate count
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
            my_pattern.config['system']['repeat_count'] = (
                value_new
            )
            print("set repeat_count to {}.".format(
                my_pattern.config['system']['repeat_count']
            ))


def parse_ui__repeat_snake(user_input):
    """Parse repeate snake."""
    # try to extract repeat_snake
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
            my_pattern.config['system']['repeat_snake'] = (
                mode_value_new
            )
            print("set repeat_snake to {}.".format(
                my_pattern.config['system']['repeat_snake']
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


def parse_ui__pattern_id(user_input):
    """Parse pattern id."""
    # check for integer
    try:
        pattern_index = int(user_input)
    except ValueError as e:
        print("input not valid. ({})".format(e))
    else:
        # print("my_pattern.pattern_list.count = {}".format(
        #     len(pattern_list)
        # ))

        if (
            (pattern_index >= 0) and
            (pattern_index <= len(my_pattern.pattern_list))
        ):
            my_pattern.config['system']['pattern_name'] = (
                my_pattern.pattern_list[pattern_index]
            )
            print("switched to {}.".format(
                my_pattern.pattern_list[pattern_index]
            ))
        else:
            print("not a valid index.")


def parse_ui__pattern_freez(user_input):
    """Parse pattern freez."""
    my_pattern.config['system']['pattern_running'] = False
    print("freezed.")


def parse_ui__pattern_run(user_input):
    """Parse pattern run."""
    my_pattern.config['system']['pattern_running'] = True
    print("running.")


def parse_ui__pattern_run_toggle(user_input):
    """Parse pattern run toggle."""
    my_pattern.config['system']['pattern_running'] = (
        not my_pattern.config['system']['pattern_running']
    )
    print("toggled: {}".format(my_pattern.config['system']['pattern_running']))


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
    "rc": {
        "info": "set repeate count",
        "example": "{repeat_count}",
        "func": parse_ui__repeat_count,
    },
    "rs": {
        "info": "set repeate snake",
        "example": "{repeat_snake}",
        "func": parse_ui__repeat_snake,
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
    "f": {
        "info": "freez pattern generator 'f'",
        "example": None,
        "func": parse_ui__pattern_freez,
    },
    "r": {
        "info": "run pattern generator 'r'",
        "example": None,
        "func": parse_ui__pattern_run,
    },
    "t": {
        "info": "toggle running pattern generator 't'",
        "example": None,
        "func": parse_ui__pattern_run_toggle,
    },
    "sc": {
        "info": "save config 'sc'",
        "example": None,
        "func": parse_ui__save_config,
    },
    "-": {
        "info": "",
        "example": None,
        "func": None,
    },
}

parser_functions_order = [
    "f",
    "r",
    "t",
    "-",
    "ui",
    # "pi",
    "uo",
    "uc",
    "pc",
    "rc",
    "rs",
    "mo",
    "-",
    "vh",
    "vl",
    "vo",
    "gd",
    "pd",
    "-",
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
    else:
        parse_ui__pattern_id(user_input)
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
                    repeat_count=my_pattern.config['system']['repeat_count'],
                    repeat_snake=my_pattern.config['system']['repeat_snake'],
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
    #     repeat_count=my_pattern.config['system']['repeat_count'],
    #     repeat_snake=my_pattern.config['system']['repeat_snake'],
    #     universe_output=my_pattern.config['system']['universe']['output'],
    #     mode_16bit=my_pattern.config['system']['mode_16bit'],
    #     vhigh=my_pattern.config['system']['value']['high'],
    #     vlow=my_pattern.config['system']['value']['low'],
    #     voff=my_pattern.config['system']['value']['off'],
    # )
    # print("done.")
    return parser_message


def generate_pattern_running_state():
    """Build String for menu message/info."""
    message = ""
    running_state = my_pattern.config['system']['pattern_running']
    if running_state:
        message = "  running\n"
    else:
        message = "  freezed\n"
    return message


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
        pattern_list += " {}'{}' {}\n".format(selected, index, value)

    message = (
        "\n" +
        42 * '*' + "\n"
        "select pattern: \n" +
        pattern_list +
        generate_pattern_running_state() +
        "set option: \n" +
        generate_parser_message() +
        42 * '*' + "\n"
        "\n"
    )
    return message


##########################################


def handle_interactive():
    """Handle all interactive running."""
    # wait for user to hit key.
    flag_run = True
    while flag_run:
        message = generate_menu_message()
        flag_run = request_userinput(message, handle_userinput)
    return flag_run


def main():
    """Main handling."""
    print(42 * '*')
    print('Python Version: ' + sys.version)
    print(42 * '*')

    ##########################################
    # commandline arguments
    filename_default = "./pattern.json"
    # pattern_name_default = "channelcheck"

    parser = argparse.ArgumentParser(
        description="generate patterns - output with olad"
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
        "-p",
        "--pattern",
        help="start with given pattern",
        metavar='PATTERN_NAME'
        # default=pattern_name_default
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

    # if args.interactive:
    #     # as last thing we save the current configuration.
    #     print("\nwrite config.")
    #     my_pattern.my_config.write_to_file()


##########################################
if __name__ == '__main__':

    main()

##########################################
