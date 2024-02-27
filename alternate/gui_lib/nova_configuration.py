from tkinter import *
from tkinter import ttk

def nova_configuration(parent):
        frame = ttk.Frame(parent, padding=(10,10,10,10))
        frame['width'] = 384
        frame['borderwidth'] = 2
        frame['relief'] = 'raised'


        header_lb = ttk.Label(frame, text="NOVA FC Configurations", style="Display.TLabel")

        mdm_lb = ttk.Label(frame, text="Main Deploy Altitute(m)")
        mdm_cb = ttk.Combobox(frame)
        mdm_cb['values'] = ('100','200')
        mdm_cb.state(['readonly'])

        apg_delay_lb = ttk.Label(frame, text="Apogee Delay(s)")
        apg_delay_cb = ttk.Combobox(frame)
        apg_delay_cb['values'] = ('10','15')
        apg_delay_cb.state(['readonly'])

        apg_lockout_lb = ttk.Label(frame, text="Apogee Lockout(s)")
        apg_lockout_cb = ttk.Combobox(frame)
        apg_lockout_cb['values'] = ('10','15')
        apg_lockout_cb.state(['readonly'])

        mdm_lb = ttk.Label(frame, text="Main Deploy Altitute(m)")
        mdm_cb = ttk.Combobox(frame)
        mdm_cb['values'] = ('100','200')
        mdm_cb.state(['readonly'])

        mdm_lb = ttk.Label(frame, text="Main Deploy Altitute(m)")
        mdm_cb = ttk.Combobox(frame)
        mdm_cb['values'] = ('100','200')
        mdm_cb.state(['readonly'])

        mdm_lb = ttk.Label(frame, text="Main Deploy Altitute(m)")
        mdm_cb = ttk.Combobox(frame)
        mdm_cb['values'] = ('100','200')
        mdm_cb.state(['readonly'])


        



        header_lb.grid(column=0, row=0)



        return frame