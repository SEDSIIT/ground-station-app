from tkinter import *
from tkinter import ttk
import time

class GroundStationApp:
    def __init__(self):
        
        # Root toplevel window
        # Control Panel window
        self.root = Tk()
        self.root.title("Control Panel")
        self.root_mainframe = ttk.Frame(self.root)

        # Subroot toplevel window
        # Monitor window
        self.subroot = Toplevel(self.root)
        self.subroot.title("Monitor")
        self.subroot_mainframe = ttk.Frame(self.root)

        # Control Panel window widget instantiations
        lm = self.live_metrics()
        cs = self.connection_status()
        nc = self.nova_configuration()

        # Control Panel window gridding widgets
        lm.grid(column=0, row=0)
        cs.grid(column=1, row=0)
        nc.grid(column=2, row=0)

        # Live Metrics

        # Connection Status

        # Nova Configuration

    
    

    # Control Panel window widget instantiations
    def live_metrics(self):
        #frame = ttk.Frame()
        return 
    
    def connection_status(self):
        return
    
    def nova_configuration(self):
        return
    
    def run(self):
        self.root.mainloop()


