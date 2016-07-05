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
import struct

from configdict import ConfigDict
from olathreaded import OLAThread, OLAThread_States


version = """02.04.2016 19:09 stefan"""


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

        # this does not work. the link to main config is lost..
        # self.update_interval = self.config['system']['update_interval']
        # self.universe = self.config['universe']['output']
        # self.channel_count = 512
        # self.channel_count = 50
        # self.channel_count = self.config['system']['channel_count']

        self.strobe_state = False

        self.channel_current = 0

        # high and low values:
        # value_low_hb, value_low_lb = self.calculate_16bit_values(
        #     self.config['system']['value']['low']
        # )
        # value_high_hb, value_high_lb = self.calculate_16bit_values(
        #     self.config['system']['value']['high']
        # )

    def calculate_16bit_values(self, value):
        """calculate the low and high part representations of value."""
        high_byte = 0
        low_byte = 0
        if self.config['system']['mode_16bit']:
            if value > 65535:
                value = 65535
            low_byte, high_byte = struct.unpack(
                "<BB",
                struct.pack("<H", value)
            )
        else:
            if value > 255:
                # convert 16bit range to 8bit range
                value = value / 256
            # check for bounds
            if value > 255:
                value = 255
            if value < 0:
                value = 0
            high_byte = value
        return high_byte, low_byte

    def ola_connected(self):
        """register update event callback and switch to running mode."""
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

    def _calculate_step(self):
        """generate test pattern."""
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

        # pattern_name = 'strobe'
        # pattern_name = 'channelcheck'
        pattern_name = self.config['system']['pattern_name']

        if 'strobe' in pattern_name:
            self._calculate_step_strobe(
                self.config['pattern']['strobe']
            )
        elif 'channelcheck' in pattern_name:
            self._calculate_step_channelcheck(
                self.config['pattern']['channelcheck']
            )
        elif 'staic' in pattern_name:
            self._calculate_step_static(
                self.config['pattern']['static']
            )

    def _calculate_step_strobe(self, config):
        """generate test pattern 'strobe'."""
        # prepare temp array
        data_output = array.array('B')

        mode_16bit = self.config['system']['mode_16bit']
        value_off_hb, value_off_lb = self.calculate_16bit_values(
            self.config['system']['value']['off']
        )
        value_low_hb, value_low_lb = self.calculate_16bit_values(
            self.config['system']['value']['low']
        )
        value_high_hb, value_high_lb = self.calculate_16bit_values(
            self.config['system']['value']['high']
        )

        # calculate device_count
        device_count = self.config['system']['channel_count'] / 12

        # get value set
        channel_values = {}
        if self.strobe_state:
            channel_values = config[0]
        else:
            channel_values = config[1]

        mode_16bit = self.config['system']['mode_16bit']
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

                if mode_16bit:
                    data_output.append(high_byte)
                    data_output.append(low_byte)
                else:
                    data_output.append(high_byte)

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

        # print(self.channel_current)
        # if not hasattr(config, 'channel_current'):
        #     config['channel_current'] = 0

        mode_16bit = self.config['system']['mode_16bit']
        value_low_hb, value_low_lb = self.calculate_16bit_values(
            self.config['system']['value']['low']
        )
        value_high_hb, value_high_lb = self.calculate_16bit_values(
            self.config['system']['value']['high']
        )

        # for devices generate pattern
        for index in range(0, self.config['system']['channel_count']):
            # if index is config['channel_current']:
            high_byte = value_low_hb
            low_byte = value_low_lb
            if index is self.channel_current:
                high_byte = value_high_hb
                low_byte = value_high_lb
            if mode_16bit:
                data_output.append(high_byte)
                data_output.append(low_byte)
            else:
                data_output.append(high_byte)

        if (
            self.channel_current <
            config['wrapp_around_count']
        ):
            self.channel_current = self.channel_current + 1
        else:
            self.channel_current = 0

        # send frame
        self.dmx_send_frame(
            self.config['universe']['output'],
            data_output
        )

    def _calculate_step_static(self, config):
        """generate test pattern 'static'."""
        # prepare temp array
        data_output = array.array('B')

        mode_16bit = self.config['system']['mode_16bit']
        value_off_hb, value_off_lb = self.calculate_16bit_values(
            self.config['system']['value']['off']
        )
        value_low_hb, value_low_lb = self.calculate_16bit_values(
            self.config['system']['value']['low']
        )
        value_high_hb, value_high_lb = self.calculate_16bit_values(
            self.config['system']['value']['high']
        )

        # calculate device_count
        device_count = self.config['system']['channel_count'] / 12

        # get value set
        channel_values = {}
        if self.strobe_state:
            channel_values = config[0]
        else:
            channel_values = config[1]

        mode_16bit = self.config['system']['mode_16bit']
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

                if mode_16bit:
                    data_output.append(high_byte)
                    data_output.append(low_byte)
                else:
                    data_output.append(high_byte)

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
    pattern_name = "channelcheck"
    pattern_name_in_args = False
    filename = "pattern.json"
    # only use args after script name
    arg = sys.argv[1:]
    if not arg:
        print("using standard values.")
        print(" Allowed parameters:")
        print(
            "   pattern name  (default='{}', overwrites config file value)"
            .format(pattern_name)
        )
        print(
            "   filename for config file  (default='{}')"
            .format(filename)
        )
        print("")
    else:
        pattern_name = arg[0]
        pattern_name_in_args = True
        if len(arg) > 1:
            filename = arg[0]
            # pixel_count = int(arg[1])
    # print parsed argument values
    print('''values:
        filename :{}
    '''.format(filename))

    default_config = {
        'system': {
            # 'update_interval': 30,
            'update_interval': 50,
            # 'update_interval': 250,
            'mode_16bit': True,
            'value': {
                'high': 1000,
                'low': 256,
                'off': 0,
            },
            'pattern_name': 'channelcheck',
            'channel_count': 512,
        },
        'universe': {
            'output': 1,
        },
        'pattern': {
            'channelcheck': {
                'wrapp_around_count': 16*5,
                # 'channel_current': 0,
            },
            'static': {
                'channels': [],
                # 'channel_current': 0,
            },
            'strobe': [
                [
                    # 1
                    1,
                    -1,
                    -1,
                    -1,
                    # 2
                    -1,
                    1,
                    -1,
                    -1,
                    # 3
                    -1,
                    -1,
                    1,
                    -1,
                    # 4
                    -1,
                    -1,
                    -1,
                    1,
                ],
                [
                    # 1
                    0,
                    -1,
                    -1,
                    -1,
                    # 2
                    -1,
                    0,
                    -1,
                    -1,
                    # 3
                    -1,
                    -1,
                    0,
                    -1,
                    # 4
                    -1,
                    -1,
                    -1,
                    0,
                ],
            ],
        },
    }
    my_config = ConfigDict(default_config, filename)
    # overwritte with pattern name from comandline
    if pattern_name_in_args:
        my_config.config['system']['pattern_name'] = pattern_name
    print("my_config.config: {}".format(my_config.config))

    ##########################################
    # load patterns

    # dir_current = os.path.dirname(os.path.abspath(__file__))
    # lib_path = os.path.join(dir_current, '../pattern/')
    # sys.path.append(lib_path)
    try:
        # https://docs.python.org/3/library/importlib.html#importlib.import_module
        # import pattern plugins
        from pattern.strobe import Strobe
        from pattern.channelcheck import Channelcheck
        from pattern.static import Static
    except Exception as e:
        raise
    else:
        pattern_list = [
            'channelcheck',
            'strobe',
            'static',
        ]

        pattern = {}
        # for pattern_name in pattern_list:
        pattern_name = 'channelcheck'
        pattern[pattern_name] = Channelcheck(
            my_config.config['pattern'][pattern_name],
            my_config.config['system']
        )
        pattern_name = 'strobe'
        pattern[pattern_name] = Strobe(
            my_config.config['pattern'][pattern_name],
            my_config.config['system']
        )
        pattern_name = 'static'
        pattern[pattern_name] = Static(
            my_config.config['pattern'][pattern_name],
            my_config.config['system']
        )

    my_pattern = OLAPattern(my_config.config)

    my_pattern.start_ola()

    # wait for user to hit key.
    run = True
    while run:

        message_list = ""
        # for index, value in iter(pattern_list):
        for value in pattern_list:
            index = pattern_list.index(value)
            # print(index, value)
            selected = ' '
            if my_config.config['system']['pattern_name'] == value:
                selected = '>'
            message_list += " {}'{}' {}\n".format(selected, index+1, value)

        message = (
            "\n" +
            42*'*' + "\n" +
            "select pattern: \n" +
            message_list +
            "  's': stop\n" +
            "set option: \n" +
            "  'u': update interval 'u:{update_interval}'\n" +
            "  'vh': set value high 'vh:{vhigh}'\n" +
            "  'vl': set value low 'vl:{vlow}'\n" +
            "  'vo': set value off 'vo:{voff}'\n" +
            "Ctrl+C or 'q' to stop script\n" +
            42*'*' + "\n" +
            "\n"
        ).format(
            update_interval=my_config.config['system']['update_interval'],
            vhigh=my_config.config['system']['value']['high'],
            vlow=my_config.config['system']['value']['low'],
            voff=my_config.config['system']['value']['off'],
        )
        try:
            # python2
            user_input = raw_input(message)
            # python3
            # user_input = input(message)
        except KeyboardInterrupt:
            print("\nstop script.")
            run = False
        else:
            try:
                if len(user_input) > 0:

                    if "q" in user_input[0]:
                        run = False
                        print("stop script.")
                    elif "s" in user_input[0]:
                        my_config.config['system']['pattern_name'] = 'stop'
                        print("stopped.")
                    elif "u" in user_input[0]:
                        # try to extract new update interval value
                        start_index = user_input.find(':')
                        if start_index > -1:
                            update_interval_new = user_input[start_index+1:]
                            try:
                                update_interval_new = int(update_interval_new)
                            except Exception as e:
                                print("input not valid. ({})".format(e))
                            else:
                                my_config.config['system']\
                                    ['update_interval'] = (
                                        update_interval_new
                                    )
                                print("set update_interval to {}.".format(
                                    my_config.config['system']
                                    ['update_interval']
                                ))
                    elif "v" in user_input[0]:
                        # try to extract new update interval value
                        start_index = user_input.find(':')
                        if start_index > -1:
                            value_new = user_input[start_index+1:]
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
                                if "h" in user_input:
                                    value_name = 'high'
                                elif "l" in user_input:
                                    value_name = 'low'
                                elif "o" in user_input:
                                    value_name = 'off'
                                try:
                                    my_config.config['system']['value']\
                                        [value_name] = value_new
                                except ValueError as e:
                                    print("input not valid. ({})".format(e))
                                else:
                                    print("set value {} to {}.".format(
                                        value_name,
                                        my_config.config['system']
                                        ['value'][value_name]
                                    ))
                    else:
                        # check for integer
                        try:
                            pattern_index = int(user_input)
                        except ValueError as e:
                            print("input not valid. ({})".format(e))
                        else:
                            # print("pattern_list.count = {}".format(
                            #     len(pattern_list)
                            # ))

                            if (
                                (pattern_index > 0) and
                                (pattern_index <= len(pattern_list))
                            ):
                                my_config.config['system']['pattern_name'] = (
                                    pattern_list[pattern_index-1]
                                )
                                print("switched to {}.".format(
                                    pattern_list[pattern_index-1]
                                ))
                            else:
                                print("not a valid index.")
            except Exception as e:
                print("unknown error: {}".format(e))
                run = False
                print("stop script.")
    # blocks untill thread has joined.
    my_pattern.stop_ola()

    # as last thing we save the current configuration.
    print("\nwrite config.")
    my_config.write_to_file()

    ##########################################
