from tkinter import *
from tkinter import ttk
import time
from gui_lib import live_metrics as lm_md
from gui_lib import connection_status as cs_md
from gui_lib import nova_configuration as nc_md



class GroundStationApp:
    def __init__(self):
        
        # Root toplevel window
        # Control Panel window
        self.root = Tk()
        self.root.title("Control Panel")
        # following 16:9 aspect ration
        self.root_mainframe = ttk.Frame(self.root, width=1024, height=600)
        self.root_mainframe.grid(column = 0, row = 0)

        # Subroot toplevel window
        # Monitor window
        self.subroot = Toplevel(self.root)
        self.subroot.title("Monitor")
        # following 16:9 aspect ratio
        self.subroot_mainframe = ttk.Frame(self.subroot, width=1024, height=600)
        self.subroot_mainframe.grid(column = 0, row = 0)

        # Control Panel window widget instantiations
        lm = lm_md.live_metrics(self.root_mainframe)
        cs = cs_md.connection_status(self.root_mainframe)
        nc = nc_md.nova_configuration(self.root_mainframe)

        # Control Panel window gridding widgets
        lm.grid(column=0, row=0, sticky=(N,W,E,S))
        cs.grid(column=1, row=0, sticky=(N,W,E,S))
        nc.grid(column=2, row=0, sticky=(N,W,E,S))
    
    def run(self):
        self.root.mainloop()


