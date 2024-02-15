from tkinter import *
from tkinter import ttk
import time

class GroundStationApp:
    def __init__(self):
        
        # Root toplevel window
        # Control panel window
        self.root = Tk()
        self.root.title("Control Panel")

        # Subroot toplevel window
        # Monitor window
        self.subroot = Toplevel(self.root)
        self.subroot.title("Monitor")


        # Setting up



    def run(self):
        self.root.mainloop()