from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import time
from gui_lib import live_metrics as lm_md
from gui_lib import connection_status as cs_md
from gui_lib import nova_configuration as nc_md
from gui_lib import pyro_channels as pc_md
from gui_lib import monitor as mr_md
from gui_lib import styles 


class GroundStationApp:
    def __init__(self):
        # this will be the reference to the arduino serial object
        self.as_obj = None

        # check out https://ttkthemes.readthedocs.io/en/latest/themes.html
        # you must have 'ttkthemes' installed
        # 'python -m pip install ttkthemese'
        
        # To see what kind of fonts are installed:
        # 'from tkinter import font'
        # print(font.families())'

        # Root toplevel window
        # set theme here!
        self.root = ThemedTk(theme="radiance")
        self.root.columnconfigure(0, weight = 1)
        self.root.rowconfigure(0, weight=1)
        # That being said, we will still define custom styles that are derived from the styles 
        # of the currently set theme 
        s = ttk.Style()
        # print(s.theme_names())
        styles.set_styles(s)

        # entire state of gs app listed here
        # need to be connected to the appropriate widgets

        # live_metrics 
        self.call_sign = StringVar()
        self.serial    = StringVar()
        self.flight    = StringVar()
        self.state     = StringVar()
        self.rssi      = StringVar()
        self.age       = StringVar()

        # connection_status
        self.nova_callsign_e  = StringVar()
        self.nova_frequency   = StringVar()
        self.nova_baud        = StringVar()
        self.nova_log         = None        # reference to the log (to be set)
        self.nova_light       = None        # reference to the log (to be set)
        self.arduino_comport  = StringVar()
        self.arduino_log      = None        # reference to the log (to be set)
        self.arduino_light    = None        # reference to the log (to be set)

        # nova_configuration
        self.mda             = StringVar()
        self.apg_delay       = StringVar()
        self.apg_lockout     = StringVar()
        self.ign_fmode       = StringVar()
        self.bf              = StringVar()
        self.a_pyro_data     = {}
        # key : value, key is param, value is tuple pair
        # key : (enabled? , value)
        # i.e
        # a_val : (true/false , a_val_e)

        
        self.root.title("Control Panel")
        # following 16:9 aspect ration
        self.root_mainframe = ttk.Frame(self.root)
        self.root_mainframe.grid(column = 0, row = 0, sticky=(N,W,E,S))

        # Subroot toplevel window
        # Monitor window
        self.subroot = Toplevel(self.root)
        self.subroot.title("Monitor")
        # following 16:9 aspect ratio
        self.subroot_mainframe = ttk.Frame(self.subroot)
        self.subroot_mainframe.grid(column = 0, row = 0, sticky=(N,W,E,S))

        # Control Panel window widget instantiations
        lm = lm_md.live_metrics(self.root_mainframe, self)
        cs = cs_md.connection_status(self.root_mainframe, self)
        nc = nc_md.nova_configuration(self.root_mainframe, self)

        # Control Panel window gridding widgets
        lm.grid(column=0, row=0, sticky=(N,W,E,S))
        cs.grid(column=1, row=0, sticky=(N,W,E,S))
        nc.grid(column=2, row=0, sticky=(N,W,E,S))

        self.root_mainframe.columnconfigure(0, weight=1)
        self.root_mainframe.columnconfigure(1, weight=1)
        self.root_mainframe.columnconfigure(2, weight=1)
        self.root_mainframe.rowconfigure(0, weight=1)

        # Monitor Panel window widget instantiations
        mr = mr_md.monitor(self.subroot, self)


        # Monitor Panel window gridding widgets
        mr.grid(column=0, row=0, sticky=(N,W,E,S))



    

    def set_as_ref(self, as_obj):
        self.as_obj = as_obj

    def open_pyro_channels(self):
        pyro_root = Toplevel(self.root)
        pyro_root.title("Pyro Channels Configuration")
        pyro_root.columnconfigure(0, weight = 1)
        pyro_root.rowconfigure(0, weight = 1)

        pyro_frame = pc_md.pyro_channels(pyro_root, self)
        pyro_frame.grid(column = 0, row = 0, sticky=(N, W, E, S))


        pyro_root.transient(self.root)
        pyro_root.grab_set()
        self.root.wait_window(pyro_root)

    def run(self):
        self.root.mainloop()


