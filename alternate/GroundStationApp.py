from tkinter import *
from tkinter import ttk
import time

class GroundStationApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Testing")

    def run(self):
        print("Hello World")
        time.sleep(3)
        print("testing threading!")
        self.root.mainloop()