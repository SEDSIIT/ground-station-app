from tkinter import *
from tkinter import ttk

def live_metrics(parent):
        
        frame = ttk.Frame(parent, padding=(10,0,10,10))
        frame['width'] = 256
        frame['borderwidth'] = 0
        frame['relief'] = 'flat'
        

        live_metrics_lb = ttk.Label(frame, text="Live Metrics", style='Header.TLabel')

        call_sign_lb = ttk.Label(frame, text="Call Sign", style="Display.TLabel")
        serial_lb    = ttk.Label(frame, text="Serial", style="Display.TLabel")
        flight_lb    = ttk.Label(frame, text="Flight", style="Display.TLabel")
        state_lb     = ttk.Label(frame, text="State", style="Display.TLabel")
        rssi_lb      = ttk.Label(frame, text="RSSI", style="Display.TLabel")
        age_lb       = ttk.Label(frame, text="Age", style="Display.TLabel")

        live_metrics_lb.grid(column=0,row=0,columnspan=2, sticky=(N))
        
        call_sign_lb.grid(column=0,row=1)
        serial_lb   .grid(column=0,row=2)
        flight_lb   .grid(column=0,row=3)
        state_lb    .grid(column=0,row=4)
        rssi_lb     .grid(column=0,row=5)
        age_lb      .grid(column=0,row=6)

        frame.columnconfigure(0, minsize=128)
        frame.columnconfigure(1, minsize=128)

        return frame