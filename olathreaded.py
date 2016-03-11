#!/usr/bin/env python
# coding=utf-8

"""
olad client abstraction.

    packs the communication with the olad deamon in an threaded way.
    it will automaticaly reconnect if olad is shutdown and comes back online.

    history:
        see git commits

    todo:
        ~ all fine :-)
"""


import os
import sys
import time
import threading
from enum import Enum, unique
import array
import socket

from ola.ClientWrapper import ClientWrapper
from ola.OlaClient import OLADNotRunningException

version = """08.03.2016 19:00 stefan"""


##########################################
# globals


##########################################
# functions


##########################################
# classes


@unique
class OLAThread_States(Enum):
    """states for OLAThread."""

    standby = 1
    waiting = 2
    connected = 3
    running = 4
    stopping = 5
    starting = 6


class OLAThread(threading.Thread):
    """connect to olad in a threaded way."""

    def __init__(self):
        """create new OLAThread instance."""
        # super().__init__()
        # super(threading.Thread, self).__init__()
        threading.Thread.__init__(self)

        self.wrapper = None
        self.client = None

        self.state = OLAThread_States.standby

        self.flag_connected = False
        self.flag_wait_for_ola = False

        # self.start()

    def run(self):
        """run state engine in threading."""
        print("run")
        print("self.state: {}".format(self.state))
        while self.state is not OLAThread_States.standby:
            if self.state is OLAThread_States.waiting:
                # print("state - waiting")
                self.ola_waiting_for_connection()
            elif self.state is OLAThread_States.connected:
                self.ola_connected()
            elif self.state is OLAThread_States.running:
                self.ola_wrapper_run()
            # elif self.state is OLAThread_States.stopping:
            #     pass
            # elif self.state is OLAThread_States.starting:
            #     pass

    def ola_wrapper_run(self):
        """run ola wrapper."""
        print("run ola wrapper.")
        try:
            self.wrapper.Run()
        except KeyboardInterrupt:
            self.wrapper.Stop()
            print("\nstopped")
        except socket.error as error:
            print("connection to OLAD lost:")
            print("   error: " + error.__str__())
            self.flag_connected = False
            self.state = OLAThread_States.waiting
            # except Exception as error:
            #     print(error)

    def ola_waiting_for_connection(self):
        """connect to ola."""
        print("waiting for olad....")
        self.flag_connected = False
        self.flag_wait_for_ola = True
        while (not self.flag_connected) & self.flag_wait_for_ola:
            try:
                # print("get wrapper")
                self.wrapper = ClientWrapper()
            except OLADNotRunningException:
                time.sleep(0.5)
            else:
                self.flag_connected = True
                self.state = OLAThread_States.connected

        if self.flag_connected:
            self.flag_wait_for_ola = False
            print("get client")
            self.client = self.wrapper.Client()
        else:
            print("\nstopped waiting for olad.")

    def ola_connected(self):
        """
        just switch to running mode.

           this can be overriden in a subclass.
        """
        self.state = OLAThread_States.running

    # dmx frame sending
    def dmx_send_frame(self, universe, data):
        """send data as one dmx frame."""
        if self.flag_connected:
            try:
                # temp_array = array.array('B')
                # for channel_index in range(0, self.channel_count):
                #     temp_array.append(self.channels[channel_index])

                # print("temp_array:{}".format(temp_array))
                # print("send frame..")
                self.wrapper.Client().SendDmx(
                    universe,
                    data,
                    # temp_array,
                    self.dmx_send_callback
                )
                # print("done.")
            except OLADNotRunningException:
                self.wrapper.Stop()
                print("olad not running anymore.")
        else:
            # throw error
            pass

    def dmx_send_callback(self, state):
        """react on ola state."""
        if not state.Succeeded():
            self.wrapper.Stop()
            self.state = OLAThread_States.waiting
            print("warning: dmxSent does not Succeeded.")
        else:
            # print("send frame succeeded.")
            pass

    # managment functions
    def start_ola(self):
        """switch to state running."""
        print("start_ola")
        if self.state == OLAThread_States.standby:
            self.state = OLAThread_States.waiting
            self.start()

    def stop_ola(self):
        """stop ola wrapper."""
        if self.flag_wait_for_ola:
            print("stop search for ola wrapper.")
            self.flag_wait_for_ola = False
        if self.flag_connected:
            print("stop ola wrapper.")
            self.wrapper.Stop()
        # stop thread
        self.state = OLAThread_States.standby
        # wait for thread to finish.
        self.join()

##########################################
if __name__ == '__main__':

    print(42*'*')
    print('Python Version: ' + sys.version)
    print(42*'*')
    print(__doc__)
    print(42*'*')

    my_olathread = OLAThread()

    my_olathread.start_ola()

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

    # blocks untill thread has joined.
    my_olathread.stop_ola()

    # ###########################################
