from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import time
from gui_lib import live_metrics as lm_md
from gui_lib import connection_status as cs_md
from gui_lib import nova_configuration as nc_md
from gui_lib import styles 



class GroundStationApp:
    def __init__(self):
        
        # check out https://ttkthemes.readthedocs.io/en/latest/themes.html
        # you must have 'ttkthemes' installed
        # 'python -m pip install ttkthemese'
        
        

        # To see what kind of fonts are installed:
        # 'from tkinter import font'
        # print(font.families())'

        # Root toplevel window
        # set theme here!
        self.root = ThemedTk(theme="equilux")
        # That being said, we will still define custom styles that are derived from the styles 
        # of the currently set theme 
        s = ttk.Style()
        # print(s.theme_names())
        styles.set_styles(s)
        print(s.layout("TFrame"))
        print(s.element_options("Frame.border"))

        
        self.root.title("Control Panel")
        # following 16:9 aspect ration
        self.root_mainframe = ttk.Frame(self.root)
        self.root_mainframe.grid(column = 0, row = 0)

        # Subroot toplevel window
        # Monitor window
        self.subroot = Toplevel(self.root)
        self.subroot.title("Monitor")
        # following 16:9 aspect ratio
        self.subroot_mainframe = ttk.Frame(self.subroot)
        self.subroot_mainframe.grid(column = 0, row = 0)

        # Control Panel window widget instantiations
        lm = lm_md.live_metrics(self.root_mainframe)
        cs = cs_md.connection_status(self.root_mainframe)
        nc = nc_md.nova_configuration(self.root_mainframe)

        # Control Panel window gridding widgets
        lm.grid(column=0, row=0)
        cs.grid(column=1, row=0)
        nc.grid(column=2, row=0)
    
    def run(self):
        self.root.mainloop()


