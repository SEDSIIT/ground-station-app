from tkinter import *
from tkinter import ttk

def nova_configuration(parent, gsa_obj):
        frame = ttk.Frame(parent, padding=(10,10,10,10))
        frame['width'] = 384
        frame['borderwidth'] = 2
        frame['relief'] = 'raised'


        header_lb = ttk.Label(frame, text="NOVA FC Configurations", style="Display.TLabel")

        mda_lb = ttk.Label(frame, text="Main Deploy Altitute(m)", padding=(0,5,0,5))
        mda_cb = ttk.Combobox(frame)
        mda_cb['values'] = ('100','200')

        apg_delay_lb = ttk.Label(frame, text="Apogee Delay(s)", padding=(0,5,0,5))
        apg_delay_cb = ttk.Combobox(frame)
        apg_delay_cb['values'] = ('10','15')

        apg_lockout_lb = ttk.Label(frame, text="Apogee Lockout(s)", padding=(0,5,0,5))
        apg_lockout_cb = ttk.Combobox(frame)
        apg_lockout_cb['values'] = ('10','15')
     

        ign_fmode_lb = ttk.Label(frame, text="Igniter Firing Mode", padding=(0,5,0,5))
        ign_fmode_cb = ttk.Combobox(frame)
        ign_fmode_cb['values'] = ('Seperation & Apogee')
        ign_fmode_cb.state(['readonly'])

        bf_lb = ttk.Label(frame, text="Beeper Frequency", padding=(0,5,0,5))
        bf_cb = ttk.Combobox(frame)
        bf_cb['values'] = ('4000')


        cpc_b = ttk.Button(frame, text="Configure Pyro Channels", padding=(0,5,0,5), command=gsa_obj.open_pyro_channels)
        send_b = ttk.Button(frame, text="Send")

        # STATE ATTACHED HERE
        # now attaching state (these are StringVars) and setting default values
        mda_cb          ['textvariable'] = gsa_obj.mda
        apg_delay_cb    ['textvariable'] = gsa_obj.apg_delay
        apg_lockout_cb  ['textvariable'] = gsa_obj.apg_lockout
        ign_fmode_cb    ['textvariable'] = gsa_obj.ign_fmode




        # Gridding and configuring columns/rows
        header_lb.grid(column=0, row=0, columnspan=2)

        mda_lb.grid(column=0, row=1)
        mda_cb.grid(column=1, row=1)

        apg_delay_lb.grid(column=0, row=2)
        apg_delay_cb.grid(column=1, row=2)

        apg_lockout_lb.grid(column=0, row=3)
        apg_lockout_cb.grid(column=1, row=3)

        ign_fmode_lb.grid(column=0, row=4)
        ign_fmode_cb.grid(column=1, row=4)

        bf_lb.grid(column=0, row=5)
        bf_cb.grid(column=1, row=5)

        cpc_b.grid(column=1, row=6)
        send_b.grid(column=1,row=7, sticky=(E))

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=1)
        frame.rowconfigure(5, weight=1)
        frame.rowconfigure(6, weight=1)
        frame.rowconfigure(7, weight=1)

        return frame