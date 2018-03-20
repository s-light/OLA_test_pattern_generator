#!/usr/bin/env python2
# coding=utf-8

"""Readline & History Support."""


import os
import sys
import atexit
import readline


##########################################
# functions

def save(prev_h_len, histfile):
    """Save history."""
    new_h_len = readline.get_current_history_length()
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
    if sys.version_info.major >= 3:
        # python3
        readline.append_history_file(new_h_len - prev_h_len, histfile)
    elif sys.version_info.major == 2:
        # python2
        readline.write_history_file(histfile)
    else:
        pass


def setup_readline_history(histfile=None):
    """Handle readline / history."""
    if not histfile:
        histfile = "./.python_history"
        # histfile = os.path.join(os.path.expanduser("~"), ".python_history")

    if sys.version_info.major >= 3:
        # python3
        try:
            readline.read_history_file(histfile)
            h_len = readline.get_current_history_length()
        except os.FileNotFoundError:
            open(histfile, 'wb').close()
            h_len = 0
    elif sys.version_info.major == 2:
        # python2
        try:
            readline.read_history_file(histfile)
            h_len = readline.get_current_history_length()
        except IOError:
            open(histfile, 'wb').close()
            h_len = 0
    else:
        h_len = 0

    print("readline history length: {}".format(
        readline.get_current_history_length()
    ))

    atexit.register(save, h_len, histfile)


##########################################
if __name__ == '__main__':
    pass

##########################################
