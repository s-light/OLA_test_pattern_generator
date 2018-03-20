#!/usr/bin/env python2
# coding=utf-8

"""Wrapper for User Input."""

import sys


def request_userinput(message, handle_userinput):
    """Request userinput."""
    flag_run = True
    # handle different python versions:
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
