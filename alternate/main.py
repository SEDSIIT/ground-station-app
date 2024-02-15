from tkinter import *
from tkinter import ttk
import threading
import time
from GroundStationApp import GroundStationApp
from ArduinoSerial import ArduinoSerial

def test_io():
      time.sleep(10)
      print("Input 1...")


# main thread will run the gui loop
# added thread will run i/o operations
# how to get threads to share info
# just pass class objects to eachother


def main():
        

        gsa_obj = GroundStationApp()
        as_obj = ArduinoSerial()

        test_thread = threading.Thread(target=as_obj.run, args=())
        test_thread.start()

        gsa_obj.run()

        test_thread.join()
        



if (__name__ == '__main__'):
        main()