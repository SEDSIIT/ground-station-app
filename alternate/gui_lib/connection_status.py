from tkinter import *
from tkinter import ttk

def connection_status(parent):

        frame = ttk.Frame(parent, padding=(10,0,10,10))
        frame['width'] = 384
        frame['borderwidth'] = 5
        frame['relief'] = 'groove'

        # Connection status 
        connection_status_lf = ttk.LabelFrame(frame, text="Connection Status",width=350,height=50)
        connection_status_lb = ttk.Label(connection_status_lf, text="DISCONNECTED", style="HeaderRed.TLabel")

        # NOVA FC status 
        nova_lb = ttk.Label(frame, text="NOVA FC", style="Display2.TLabel")
        nova_mini_f = ttk.Frame(frame)
        nova_connect_btn = ttk.Button(nova_mini_f, text="Connect")
        nova_light = ttk.Radiobutton(nova_mini_f)
        nova_log_txt = Text(frame, width = 20, height = 5)
        nova_mini_f2 = ttk.Frame(frame, padding=(10,0,10,0))

        nova_callsign_cb = ttk.Combobox(nova_mini_f2)

        nova_channel_cb = ttk.Combobox(nova_mini_f2)
        nova_channel_cb['values'] = ('Channel 1','Channel 2')
        nova_channel_cb.state(['readonly'])

        nova_frequency_cb = ttk.Combobox(nova_mini_f2)
        nova_frequency_cb['values'] = ('500Mhz','1000Mhz')
        nova_frequency_cb.state(['readonly'])
        

        # Arduino status
        arduino_lb = ttk.Label(frame, text="Arduino", style="Display2.TLabel")
        arduino_mini_f = ttk.Frame(frame)
        arduino_connect_btn = ttk.Button(arduino_mini_f, text="Connect")
        arduino_light = ttk.Radiobutton(arduino_mini_f)
        arduino_log_txt = Text(frame, width=20, height=5)
        arduino_mini_f2 = ttk.Frame(frame, padding=(10,0,10,0))

        arduino_callsign_cb = ttk.Combobox(arduino_mini_f2)
        arduino_callsign_cb['values'] = ('COM1','COM4')
        arduino_callsign_cb.state(['readonly'])

        connection_status_lf.grid(column=0, row=0, columnspan=2, sticky=(W,E))
        connection_status_lb.grid(column=0, row=0)
        
        nova_lb          .grid(column=0, row=1)
        nova_mini_f      .grid(column=1, row=1, sticky=(N,W,E,S))
        nova_connect_btn .grid(column=0, row=0)
        nova_light       .grid(column=1, row=0)
        nova_log_txt     .grid(column=1, row=2)
        nova_mini_f2     .grid(column=0, row=2, sticky=(N,W,S,E))
        nova_callsign_cb .grid(column=0, row=0)
        nova_channel_cb  .grid(column=0, row=1)
        nova_frequency_cb.grid(column=0, row=2)

        arduino_lb         .grid(column=0,row=3)
        arduino_mini_f     .grid(column=1,row=3, sticky=(N,W,E,S))
        arduino_connect_btn.grid(column=0, row=0)
        arduino_light      .grid(column=1, row=0)
        arduino_log_txt    .grid(column=1, row=4)
        arduino_mini_f2    .grid(column=0, row=4)
        arduino_callsign_cb.grid(column=0, row=0)
        
        frame               .columnconfigure(0, weight = 1)
        frame               .columnconfigure(1, weight = 1)

        connection_status_lf.columnconfigure(0, weight=1)

        nova_mini_f     .columnconfigure(0, weight = 1)
        nova_mini_f     .columnconfigure(1, weight = 1)
        nova_mini_f     .rowconfigure(0, weight = 1)

        nova_mini_f2    .columnconfigure(0, weight=1)
        nova_mini_f2    .rowconfigure(0, weight=1)
        nova_mini_f2    .rowconfigure(1, weight=1)
        nova_mini_f2    .rowconfigure(2, weight=1)

        arduino_mini_f     .columnconfigure(0, weight = 1)
        arduino_mini_f     .columnconfigure(1, weight = 1)
        arduino_mini_f     .rowconfigure(0, weight = 1)

        arduino_mini_f2    .columnconfigure(0, weight=1)
        arduino_mini_f2    .rowconfigure(0, weight=1)





        return frame