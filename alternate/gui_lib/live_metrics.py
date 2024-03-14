from tkinter import *
from tkinter import ttk

def live_metrics(parent, gsa_obj):
        
        frame = ttk.Frame(parent, padding=(10,0,10,10))
        frame['width'] = 256
        frame['borderwidth'] = 5
        frame['relief'] = 'groove'
        
        call_sign_lb = ttk.Label(frame, text="Call Sign", style="Display.TLabel")
        serial_lb    = ttk.Label(frame, text="Serial", style="Display.TLabel")
        flight_lb    = ttk.Label(frame, text="Flight", style="Display.TLabel")
        state_lb     = ttk.Label(frame, text="State", style="Display.TLabel")
        rssi_lb      = ttk.Label(frame, text="RSSI", style="Display.TLabel")
        age_lb       = ttk.Label(frame, text="Age", style="Display.TLabel")

        call_sign_f = ttk.Frame(frame)
        # leave standard options outside of the style file, otherwise they are invalid options or buggy
        call_sign_f['borderwidth'] = 2
        call_sign_f['relief'] = 'raised'

        serial_f    = ttk.Frame(frame, style="Display.TFrame")
        serial_f['borderwidth'] = 2
        serial_f['relief'] = 'raised'

        flight_f    = ttk.Frame(frame, style="Display.TFrame")
        flight_f['borderwidth'] = 2
        flight_f['relief'] = 'raised'

        state_f     = ttk.Frame(frame, style="Display.TFrame")
        state_f['borderwidth'] = 2
        state_f['relief'] = 'raised'

        rssi_f      = ttk.Frame(frame, style="Display.TFrame")
        rssi_f['borderwidth'] = 2
        rssi_f['relief'] = 'raised'

        age_f       = ttk.Frame(frame, style="Display.TFrame")
        age_f['borderwidth'] = 2
        age_f['relief'] = 'raised'

        call_sign_flb = ttk.Label(call_sign_f, style="DisplayInner.TLabel")
        serial_flb    = ttk.Label(serial_f, style="DisplayInner.TLabel")
        flight_flb    = ttk.Label(flight_f, style="DisplayInner.TLabel")
        state_flb     = ttk.Label(state_f, style="DisplayInner.TLabel")
        rssi_flb      = ttk.Label(rssi_f, style="DisplayInner.TLabel")
        age_flb       = ttk.Label(age_f, style="DisplayInner.TLabel")

        # STATE ATTACHED HERE
        # now attaching state (these are StringVars) and setting default values
        call_sign_flb['textvariable'] = gsa_obj.call_sign
        serial_flb   ['textvariable'] = gsa_obj.serial
        flight_flb   ['textvariable'] = gsa_obj.flight
        state_flb    ['textvariable'] = gsa_obj.state
        rssi_flb     ['textvariable'] = gsa_obj.rssi
        age_flb      ['textvariable'] = gsa_obj.age

        gsa_obj.call_sign.set("-")
        gsa_obj.serial   .set("-")
        gsa_obj.flight   .set("-")
        gsa_obj.state    .set("-")
        gsa_obj.rssi     .set("-")
        gsa_obj.age      .set("-")

        # Gridding/Configuring done here
        call_sign_lb.grid(column=0,row=0)
        serial_lb   .grid(column=0,row=1)
        flight_lb   .grid(column=0,row=2)
        state_lb    .grid(column=0,row=3)
        rssi_lb     .grid(column=0,row=4)
        age_lb      .grid(column=0,row=5)

        call_sign_f.grid(column=1,row=0,sticky=(W,E))
        serial_f   .grid(column=1,row=1,sticky=(W,E))
        flight_f   .grid(column=1,row=2,sticky=(W,E))
        state_f    .grid(column=1,row=3,sticky=(W,E))
        rssi_f     .grid(column=1,row=4,sticky=(W,E))
        age_f      .grid(column=1,row=5,sticky=(W,E))

        call_sign_flb.grid(column=0, row=0)
        serial_flb   .grid(column=0, row=0)
        flight_flb   .grid(column=0, row=0)
        state_flb    .grid(column=0, row=0)
        rssi_flb     .grid(column=0, row=0)
        age_flb      .grid(column=0, row=0)

        call_sign_f.columnconfigure(0, weight = 1)
        serial_f   .columnconfigure(0, weight = 1)
        flight_f   .columnconfigure(0, weight = 1)
        state_f    .columnconfigure(0, weight = 1)
        rssi_f     .columnconfigure(0, weight = 1)
        age_f      .columnconfigure(0, weight = 1)

        call_sign_f.rowconfigure(0, weight = 1)
        serial_f   .rowconfigure(0, weight = 1)
        flight_f   .rowconfigure(0, weight = 1)
        state_f    .rowconfigure(0, weight = 1)
        rssi_f     .rowconfigure(0, weight = 1)
        age_f      .rowconfigure(0, weight = 1)
        
        frame.columnconfigure(0, weight = 1, minsize=128)
        frame.columnconfigure(1, weight = 1, minsize=128)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=1)
        frame.rowconfigure(5, weight=1)

        return frame