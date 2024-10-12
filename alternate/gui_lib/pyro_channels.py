from tkinter import *
from tkinter import ttk

def pyro_channels(parent, gsa_obj):
    frame = ttk.Frame(parent, padding=(10,10,10,10))
    frame['width'] = 384
    frame['borderwidth'] = 2
    frame['relief'] = 'raised'


    # Common
    val_lb  = ttk.Label(frame, text="Vertical Acceleration Less than (m/s^2)", padding=(0,5,0,5))
    vag_lb  = ttk.Label(frame, text="Vertical Acceleration Greater than (m/s^2)", padding=(0,5,0,5))
    arl_lb  = ttk.Label(frame, text="Ascent Rate Less Than (m/s)", padding=(0,5,0,5))
    arg_lb  = ttk.Label(frame, text="Ascent Rate Greater Than (m/s)", padding=(0,5,0,5))
    hapl_lb = ttk.Label(frame, text="Height Above Pad Less Than (m)", padding=(0,5,0,5))
    hapg_lb = ttk.Label(frame, text="Height Above Pad Greater Than (m)", padding=(0,5,0,5))
    afvl_lb = ttk.Label(frame, text="Angle From Vertical Less Than (degrees)", padding=(0,5,0,5))
    afvg_lb = ttk.Label(frame, text="Angle From Vertical Greater Than (degrees)", padding=(0,5,0,5))
    tsll_lb = ttk.Label(frame, text="Time Since Launch Less Than (s)", padding=(0,5,0,5))
    tslg_lb = ttk.Label(frame, text="Time Since Launch Greater Than (s)", padding=(0,5,0,5))
    afm_lb  = ttk.Label(frame, text="After Motor Number", padding=(0,5,0,5))
    daoc_lb = ttk.Label(frame, text="Delay After Other Conditions (s)", padding=(0,5,0,5))
    fsb_lb  = ttk.Label(frame, text="Flight State Before", padding=(0,5,0,5))
    fsa_lb  = ttk.Label(frame, text="Flight State After", padding=(0,5,0,5))

    a_pyro_lb = ttk.Label(frame, text="Pyro Channel A" , padding=(0,5,0,5))

    

    pfr_lb = ttk.Label(frame, text="Pyro Firing Time (s)", padding=(0,5,0,5))
    pfr_e  = ttk.Entry(frame)
    done_btn = ttk.Button(frame, text="Done", padding=(0,5,0,5), command = lambda: save_and_close(parent, gsa_obj.i_pyroChanConf, gsa_obj.i_updatePyroChan))

    pyro_conf = gsa_obj.i_pyroChanConf
    int_params, bool_params = pyro_conf.get_valid_params()
    attr_dict = pyro_conf.get_attr_dict()
    
    # Pyro Channel A
    a_val_chkb  = ttk.Checkbutton(frame, variable=attr_dict['a_val_chkb'])
    a_vag_chkb  = ttk.Checkbutton(frame, variable=attr_dict["a_vag_chkb"])
    a_arl_chkb  = ttk.Checkbutton(frame, variable=attr_dict["a_arl_chkb"])
    a_arg_chkb  = ttk.Checkbutton(frame, variable=attr_dict["a_arg_chkb"])
    a_hapl_chkb = ttk.Checkbutton(frame, variable=attr_dict["a_hapl_chkb"])
    a_hapg_chkb = ttk.Checkbutton(frame, variable=attr_dict["a_hapg_chkb"])
    a_afvl_chkb = ttk.Checkbutton(frame, variable=attr_dict["a_afvl_chkb"])
    a_afvg_chkb = ttk.Checkbutton(frame, variable=attr_dict["a_afvg_chkb"])
    a_tsll_chkb = ttk.Checkbutton(frame, variable=attr_dict["a_tsll_chkb"])
    a_tslg_chkb = ttk.Checkbutton(frame, variable=attr_dict["a_tslg_chkb"])
    a_amn_chkb  = ttk.Checkbutton(frame, variable=attr_dict["a_amn_chkb"])
    a_daoc_chkb = ttk.Checkbutton(frame, variable=attr_dict["a_daoc_chkb"])
    a_fsb_chkb  = ttk.Checkbutton(frame, variable=attr_dict["a_fsb_chkb"])
    a_fsa_chkb  = ttk.Checkbutton(frame, variable=attr_dict["a_fsa_chkb"])

    a_val_e     = ttk.Entry      (frame, textvariable=attr_dict["a_val_e"])
    a_vag_e     = ttk.Entry      (frame, textvariable=attr_dict["a_vag_e"])
    a_arl_e     = ttk.Entry      (frame, textvariable=attr_dict["a_arl_e"])
    a_arg_e     = ttk.Entry      (frame, textvariable=attr_dict["a_arg_e"])
    a_hapl_e    = ttk.Entry      (frame, textvariable=attr_dict["a_hapl_e"])
    a_hapg_e    = ttk.Entry      (frame, textvariable=attr_dict["a_hapg_e"])
    a_afvl_e    = ttk.Entry      (frame, textvariable=attr_dict["a_afvl_e"])
    a_afvg_e    = ttk.Entry      (frame, textvariable=attr_dict["a_afvg_e"])
    a_tsll_e    = ttk.Entry      (frame, textvariable=attr_dict["a_tsll_e"])
    a_tslg_e    = ttk.Entry      (frame, textvariable=attr_dict["a_tslg_e"])
    a_amn_e     = ttk.Entry      (frame, textvariable=attr_dict["a_amn_e"])
    a_daoc_e    = ttk.Entry      (frame, textvariable=attr_dict["a_daoc_e"])
    a_fsb_cb    = ttk.Combobox   (frame)
    a_fsb_cb['values'] = 'Boost'
    a_fsa_cb    = ttk.Combobox   (frame)
    a_fsa_cb['values'] = ('Boost')

    # Gridding
    # Common
    val_lb .grid(column = 0, row = 1, sticky=(W))
    vag_lb .grid(column = 0, row = 2, sticky=(W))
    arl_lb .grid(column = 0, row = 3, sticky=(W))
    arg_lb .grid(column = 0, row = 4, sticky=(W))
    hapl_lb.grid(column = 0, row = 5, sticky=(W))
    hapg_lb.grid(column = 0, row = 6, sticky=(W))
    afvl_lb.grid(column = 0, row = 7, sticky=(W))
    afvg_lb.grid(column = 0, row = 8, sticky=(W))
    tsll_lb.grid(column = 0, row = 9, sticky=(W))
    tslg_lb.grid(column = 0, row = 10, sticky=(W))
    afm_lb .grid(column = 0, row = 11, sticky=(W))
    daoc_lb.grid(column = 0, row = 12, sticky=(W))
    fsb_lb .grid(column = 0, row = 13, sticky=(W))
    fsa_lb .grid(column = 0, row = 14, sticky=(W))

    a_pyro_lb.grid(column = 2, row = 0)

    pfr_lb.grid(column = 0, row = 15, sticky=(W))
    pfr_e.grid(column = 2, row = 15, columnspan = 7, sticky=(W))
    done_btn.grid(column = 8, row = 16)



    
    # Pyro A
    a_val_chkb .grid(column = 1, row = 1)
    a_vag_chkb .grid(column = 1, row = 2)
    a_arl_chkb .grid(column = 1, row = 3)
    a_arg_chkb .grid(column = 1, row = 4)
    a_hapl_chkb.grid(column = 1, row = 5)
    a_hapg_chkb.grid(column = 1, row = 6)
    a_afvl_chkb.grid(column = 1, row = 7)
    a_afvg_chkb.grid(column = 1, row = 8)
    a_tsll_chkb.grid(column = 1, row = 9)
    a_tslg_chkb.grid(column = 1, row = 10)
    a_amn_chkb .grid(column = 1, row = 11)
    a_daoc_chkb.grid(column = 1, row = 12)
    a_fsb_chkb .grid(column = 1, row = 13)
    a_fsa_chkb .grid(column = 1, row = 14)

    a_val_e .grid(column = 2, row = 1)
    a_vag_e .grid(column = 2, row = 2)
    a_arl_e .grid(column = 2, row = 3)
    a_arg_e .grid(column = 2, row = 4)
    a_hapl_e.grid(column = 2, row = 5)
    a_hapg_e.grid(column = 2, row = 6)
    a_afvl_e.grid(column = 2, row = 7)
    a_afvg_e.grid(column = 2, row = 8)
    a_tsll_e.grid(column = 2, row = 9)
    a_tslg_e.grid(column = 2, row = 10)
    a_amn_e .grid(column = 2, row = 11)
    a_daoc_e.grid(column = 2, row = 12)
    a_fsb_cb.grid(column = 2, row = 13)
    a_fsa_cb.grid(column = 2, row = 14)

    frame.columnconfigure(0, weight = 1)
    frame.columnconfigure(1, weight = 1)
    frame.columnconfigure(2, weight = 1)

    frame.rowconfigure(0 , weight = 1)
    frame.rowconfigure(1 , weight = 1)
    frame.rowconfigure(2 , weight = 1)
    frame.rowconfigure(3 , weight = 1)
    frame.rowconfigure(4 , weight = 1)
    frame.rowconfigure(5 , weight = 1)
    frame.rowconfigure(6 , weight = 1)
    frame.rowconfigure(7 , weight = 1)
    frame.rowconfigure(8 , weight = 1)
    frame.rowconfigure(9 , weight = 1)
    frame.rowconfigure(10, weight = 1)
    frame.rowconfigure(11, weight = 1)
    frame.rowconfigure(12, weight = 1)
    frame.rowconfigure(13, weight = 1)
    frame.rowconfigure(14, weight = 1)

    return frame    

class PyroConf:
    def __init__(self):
        self.bool_params = ["a_val_chkb",
                       "a_vag_chkb",
                       "a_arl_chkb",
                       "a_arg_chkb",
                       "a_hapl_chkb",
                       "a_hapg_chkb",
                       "a_afvl_chkb",
                       "a_afvg_chkb",
                       "a_tsll_chkb",
                       "a_tslg_chkb",
                       "a_amn_chkb",
                       "a_daoc_chkb",
                       "a_fsb_chkb",
                       "a_fsa_chkb"]
        
        self.int_params = ["a_val_e",
                       "a_vag_e",
                       "a_arl_e",
                       "a_arg_e",
                       "a_hapl_e",
                       "a_hapg_e",
                       "a_afvl_e",
                       "a_afvg_e",
                       "a_tsll_e",
                       "a_tslg_e",
                       "a_amn_e",
                       "a_daoc_e",
                       "a_fsb_e",
                       "a_fsa_e"]
        
        self.vars = {k: IntVar(value=0) for k in self.int_params}
        self.vars = self.vars | {k: BooleanVar(value=False) for k in self.bool_params}

        self.uninitialized = True

    def set_attr(self, param: str, value) -> None:
        if param not in self.vars:
            print("Error: attempting to set unknown parameter in pyro config")
            return
        
        self.uninitialized = False
        self.vars[param] = value
        return

    def get_attr(self, param: str):
        if param not in self.vars:
            print("Error: attempting to get unknown parameter in pyro config")
            return None
        
        ret = self.vars[param]
        if ret is None:
            print(f"Error: parameter {param} has not been set yet")

        return ret
    
    # Use responsibly
    def get_attr_dict(self):
        return self.vars
    
    # Use responsibly
    def set_attr_dict(self, attr_dict):
        self.vars = attr_dict
    
    def get_valid_params(self) -> list[str]:
        return (self.int_params, self.bool_params)


def save_and_close(frame, pyroConf: PyroConf, updatePyroChan):
    pyroConf.set_attr("vert_acc_upper", 6969)
    updatePyroChan.set()
    frame.destroy()





