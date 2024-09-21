from tkinter import *
from tkinter import ttk
import threading
import time
from GroundStationApp import GroundStationApp
from ArduinoSerial import ArduinoSerial
from gui_lib import pyro_channels


pyroChanConf = pyro_channels.PyroConf()
updatePyroChan = threading.Event()

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
        
        gsa_obj.set_as_ref(as_obj)
        as_obj.set_gsa_ref(gsa_obj)

        test_thread = threading.Thread(target=as_obj.run, args=(pyroChanConf, updatePyroChan))
        test_thread.start()

        gsa_obj.run(pyroChanConf, updatePyroChan)

        test_thread.join()

if (__name__ == '__main__'):
        main()