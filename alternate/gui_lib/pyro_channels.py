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
    done_btn = ttk.Button(frame, text="Done", padding=(0,5,0,5), command= lambda: save_and_close(parent))

    # Pyro Channel A
    a_val_chkb  = ttk.Checkbutton(frame)
    a_vag_chkb  = ttk.Checkbutton(frame)
    a_arl_chkb  = ttk.Checkbutton(frame)
    a_arg_chkb  = ttk.Checkbutton(frame)
    a_hapl_chkb = ttk.Checkbutton(frame)
    a_hapg_chkb = ttk.Checkbutton(frame)
    a_afvl_chkb = ttk.Checkbutton(frame)
    a_afvg_chkb = ttk.Checkbutton(frame)
    a_tsll_chkb = ttk.Checkbutton(frame)
    a_tslg_chkb = ttk.Checkbutton(frame)
    a_amn_chkb  = ttk.Checkbutton(frame)
    a_daoc_chkb = ttk.Checkbutton(frame)
    a_fsb_chkb  = ttk.Checkbutton(frame)
    a_fsa_chkb  = ttk.Checkbutton(frame)

    a_val_e     = ttk.Entry      (frame)
    a_vag_e     = ttk.Entry      (frame)
    a_arl_e     = ttk.Entry      (frame)
    a_arg_e     = ttk.Entry      (frame)
    a_hapl_e    = ttk.Entry      (frame)
    a_hapg_e    = ttk.Entry      (frame)
    a_afvl_e    = ttk.Entry      (frame)
    a_afvg_e    = ttk.Entry      (frame)
    a_tsll_e    = ttk.Entry      (frame)
    a_tslg_e    = ttk.Entry      (frame)
    a_amn_e     = ttk.Entry      (frame)
    a_daoc_e    = ttk.Entry      (frame)
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


def save_and_close(frame):
    frame.destroy()








