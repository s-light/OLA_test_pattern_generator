#!/usr/bin/env python
# coding=utf-8

"""
simple package to read and write configs in dict format to file.

    supports two formats:
        json (preferred)
        ini (not implemented jet)

    history:
        see git commits

    todo:
        ~ all fine :-)
"""


import sys
import os
import time
import json
try:
    # python3
    from configparser import ConfigParser
    # print("loaded python3 ConfigParser")
except:
    # python2
    from ConfigParser import ConfigParser
    # print("loaded python2 ConfigParser")


version = """09.03.2016 18:00 stefan"""


##########################################
# globals

##########################################
# functions

##########################################
# classes

class ConfigDict():
    """abstract the reading / writing of configuration parameters."""

    def __init__(self, default_config={}, filename=None):
        """initialize config to defaults."""
        self.default_config = default_config
        self.filename = filename
        self.config = {}
        if self.filename is not None:
            if os.path.isfile(filename):
                self.read_from_file()
            else:
                self.config = self.default_config.copy()
                self.write_to_file()
        else:
            self.config = self.default_config.copy()

    def merge_deep(self, obj_1, obj_2):
        """
        merge dicts deeply.

        obj_2 overwrittes keys with same values in obj_1.
        (if they are dicts its recusive merged.)
        """
        # work on obj_1
        result = obj_1
        # make copy
        # result = obj_1.copy()
        if (isinstance(result, dict) and isinstance(obj_2, dict)):
            for key in obj_2:
                if key in result:
                    result[key] = self.merge_deep(result[key], obj_2[key])
                else:
                    result[key] = obj_2[key]
        else:
            result = obj_2
        return result

    def set_filename(self, filename):
        """set new filename."""
        self.filename = filename

    def _read_from_json_file(self, filename):
        config_temp = {}
        with open(self.filename, 'r') as f:
            config_temp = json.load(f)
            f.closed
        return config_temp

    # def _list_to_string(self, value_list):
    #     """try to convert string  to a meaningfull datatype."""
    #     value_str = ""
    #     value_str = ", ".join(value_list)
    #     value_str = "[{}]".format(value_str)
    #     return value_str
    #
    # def _string_to_list(self, value_str):
    #     """try to convert string  to a meaningfull datatype."""
    #     list = []
    #     if value_str.startswith("[") and value_str.endswith("]"):
    #         value_str = value_str.strip()
    #         list = value_str.split(",")
    #     else:
    #         raise TypeError("input string is not a valid list format.")
    #     return list
    #
    # def _try_to_convert_string(self, value_str):
    #     """try to convert string  to a meaningfull datatype."""
    #     value = None
    #     try:
    #         value = self._string_to_list(value_str)
    #     except Exception as e:
    #         print("value not a list. ({})".format(e))
    #     else:
    #         try:
    #             value = self._string_to_dict(value_str)
    #         except Exception as e:
    #             print("value not a list. ({})".format(e))
    #     return value

    def _convert_string_to_None(self, value_str):
        """test if string is None."""
        value = None
        value_str = value_str.strip()
        if value_str in ["None", "none", "NONE", "Null", "NULL", "null"]:
            value = None
        else:
            value = value_str
            raise TypeError("input string is not valid None")
        return value

    def _try_to_interpret_string(self, value_str):
        """try to interprete string as something meaningfull."""
        value = None
        try:
            value = json.loads(value_str)
        except Exception as e:
            # print("value not valid json. ({})".format(e))
            try:
                value = self._convert_string_to_None(value_str)
            except Exception as e:
                # print("value not None. ({})".format(e))
                value = value_str
        return value

    def _configparser_get_converted(self, cp, section, option):
        """get option and try to convert it to a meaningfull datatype."""
        # with this we try to convert the value to a meaningfull value..
        value = None
        try:
            # try to read as int
            value = cp.getint(section, option)
        except Exception as e:
            # print("value not a int. ({})".format(e))
            try:
                # try to read as float
                value = cp.getfloat(section, option)
            except Exception as e:
                # print("value not a float. ({})".format(e))
                # try to read as int
                try:
                    value = cp.getboolean(section, option)
                except Exception as e:
                    # print("value not a boolean. ({})".format(e))
                    # read as string
                    value = cp.get(section, option)
                    # try to convert it to something meaningfull
                    value = self._try_to_interpret_string(value)
        # return value
        return value

    def _read_from_ini_file(self, filename):
        config_temp = {}
        cp = ConfigParser()
        with open(self.filename, 'r') as f:
            cp.readfp(f)
            f.closed
        # now converte ConfigParser to dict.
        for section in cp.sections():
            # print("section: {}".format(section))
            config_temp[section] = {}
            for option in cp.options(section):
                # get option and add it to the dict
                # print("option: {}".format(option))
                value = self._configparser_get_converted(
                    cp,
                    section,
                    option
                )
                # print("value: {}".format(value))
                config_temp[section][option] = value

        return config_temp

    def read_from_file(self, filename=None):
        """read configuration from file."""
        if filename is not None:
            self.filename = filename
        config_temp = {}
        if self.filename is not None:
            # read file
            filename_ext = os.path.splitext(self.filename)[1]
            if filename_ext is not "" and filename_ext in '.json .js':
                config_temp = self._read_from_json_file(self.filename)
            else:
                config_temp = self._read_from_ini_file(self.filename)

        # do a merge with the defaults.
        self.config = self.default_config.copy()
        self.merge_deep(self.config, config_temp)

    def _write_to_json_file(self, filename, config):
        with open(filename, 'w') as f:
            json.dump(
                config,
                f,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
            f.closed

    def _value_to_string(self, value):
        value_str = ""
        if (
            isinstance(value, object) or
            isinstance(value, dict) or
            isinstance(value, list)
        ):
            value_str = json.dumps(value)
        else:
            value_str = "{}".format(value)
        return value_str

    def _write_to_ini_file(self, filename, config):
        cp = ConfigParser()
        for section in config:
            # add section.
            # print("section: {}".format(section))
            cp.add_section(section)
            for option in config[section]:
                # print("option: {}".format(option))
                value = None
                if isinstance(config[section], list):
                    # option_index = config[section].index(option)
                    # value = config[section][option_index]
                    value = None
                else:
                    value = config[section][option]
                # print("value: {}".format(value))
                # add option
                cp.set(section, option, self._value_to_string(value))
        with open(filename, 'w') as f:
            cp.write(f)
            f.closed

    def write_to_file(self, filename=None):
        """write configuration to file."""
        if filename is not None:
            self.filename = filename
        if self.filename is not None:
            # print("\nwrite file: {}".format(self.filename))
            filename_ext = os.path.splitext(self.filename)[1]
            if filename_ext is not "" and filename_ext in '.json .js':
                self._write_to_json_file(
                    self.filename,
                    self.config
                )
            else:
                self._write_to_ini_file(
                    self.filename,
                    self.config
                )

##########################################
if __name__ == '__main__':

    print(42*'*')
    print('Python Version: ' + sys.version)
    print(42*'*')
    print(__doc__)
    print(42*'*')

    # parse arguments
    filename = "test.json"
    # only use args after script name
    arg = sys.argv[1:]
    if not arg:
        print("using standard values.")
        print(" allowed parameters:")
        print("   filename for config file       (default='test.json')")
        print("")
    else:
        filename = arg[0]
        # if len(arg) > 1:
        #     pixel_count = int(arg[1])
    # print parsed argument values
    print('''values:
        filename: {}
    '''.format(filename))

    default_config = {
        'hello': {
            'world': 1,
            'space': 42,
        },
        'world': {
            'books': [0, 1, 2, 3, 4, 4, 3, 2, 1, 0, ],
            'fun': True,
            'python': True,
            'trees': {
                'fir': 1,
                'birch': 9,
                'poplar': 33,
                'maple': 11,
                'cherry': 5,
                'walnut': 2,
            },
        },
        'blubber': ['water', 'air'],
    }
    my_config = ConfigDict(default_config, filename)
    print("my_config.config: {}".format(my_config.config))

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
    except:
        print("\nstop.")

    # as last thing we save the current configuration.
    print("\nwrite config.")
    my_config.write_to_file()

    # ###########################################
