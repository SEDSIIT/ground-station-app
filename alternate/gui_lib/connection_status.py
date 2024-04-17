from tkinter import *
from tkinter import ttk

def connection_status(parent, gsa_obj):

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

        #in nova_mini_f
        nova_connect_btn = ttk.Button(nova_mini_f, text="Connect")
        nova_light = ttk.Frame(nova_mini_f, width=20, height=20)
        nova_light['width'] = 20
        nova_light['height'] = 20
        nova_light['style'] = 'Red.TFrame'
        #nova_light['background'] = 'red'

        nova_log_txt = Text(frame, width = 20, height = 5)
        nova_mini_f2 = ttk.Frame(frame, padding=(0,0,5,0))

        #in nova_mini_f2
        nova_callsign_lb = ttk.Label(nova_mini_f2, text="Call Sign", padding=(0,5,0,5))
        nova_callsign_e = ttk.Entry(nova_mini_f2)

        nova_frequency_lb = ttk.Label(nova_mini_f2, text="Frequency | CH", padding=(0,5,0,5))
        nova_frequency_cb = ttk.Combobox(nova_mini_f2)
        nova_frequency_cb['values'] = ('434.550Mhz CH0','435.550Mhz CH1')
        nova_frequency_cb.state(['readonly'])

        nova_baud_lb = ttk.Label(nova_mini_f2, text="Baud rate", padding=(0,5,0,5))
        nova_baud_cb = ttk.Combobox(nova_mini_f2)
        nova_baud_cb['values'] = ('9600','115200')
        nova_baud_cb.state(['readonly'])
        
        # Arduino status
        arduino_lb = ttk.Label(frame, text="Arduino", style="Display2.TLabel")
        arduino_mini_f = ttk.Frame(frame)
        
        #in arduino_mini_f
        arduino_connect_btn = ttk.Button(arduino_mini_f, text="Connect")
        arduino_light = ttk.Frame(arduino_mini_f, width = 20, height = 20)
        arduino_light['width'] = 20
        arduino_light['height'] = 20
        arduino_light['style'] = 'Red.TFrame'

        arduino_log_txt = Text(frame, width=20, height=5)
        arduino_mini_f2 = ttk.Frame(frame, padding=(0,0,5,0))

        #in arduino_mini_f2
        arduino_comport_lb = ttk.Label(arduino_mini_f2, text="COM PORT")
        arduino_comport_cb = ttk.Combobox(arduino_mini_f2)
        arduino_comport_cb['values'] = ('COM1','COM4')
        arduino_comport_cb.state(['readonly'])


        # STATE ATTACHED HERE
        # now attaching state (these are StringVars) and setting default values
        connection_status_lb['textvariable'] = gsa_obj.connection_status
        gsa_obj.connection_status_lb = connection_status_lb
        nova_callsign_e   ['textvariable'] = gsa_obj.nova_callsign_e
        nova_frequency_cb ['textvariable'] = gsa_obj.nova_frequency
        nova_baud_cb      ['textvariable'] = gsa_obj.nova_baud
        gsa_obj.nova_log                   = nova_log_txt
        gsa_obj.nova_light                 = nova_light
        arduino_comport_cb['textvariable'] = gsa_obj.arduino_comport
        gsa_obj.arduino_log                = arduino_log_txt
        gsa_obj.arduino_light              = arduino_light

        gsa_obj.connection_status.set('-')
        gsa_obj.nova_callsign_e.set('-')
        gsa_obj.nova_frequency .set('-')
        gsa_obj.nova_baud      .set('-')
        gsa_obj.arduino_comport.set('-')

        # Gridding and configuring columns/rows
        connection_status_lf.grid(column=0, row=0, columnspan=2, sticky=(W,E))
        connection_status_lb.grid(column=0, row=0)
        
        nova_lb          .grid(column=0, row=1)
        nova_mini_f      .grid(column=1, row=1, sticky=(N,W,E,S))

        # in nova_mini_f
        nova_connect_btn .grid(column=0, row=0)
        nova_light       .grid(column=1, row=0)

        nova_log_txt     .grid(column=1, row=2)
        nova_mini_f2     .grid(column=0, row=2, sticky=(N,W,S,E))

        # in nova_mini_f2
        nova_callsign_lb .grid(column=0, row=0)
        nova_callsign_e  .grid(column=1, row=0, sticky=(E), ipadx=7)
        nova_frequency_lb.grid(column=0, row=1)
        nova_frequency_cb.grid(column=1, row=1, sticky=(E))
        nova_baud_lb     .grid(column=0, row=2)
        nova_baud_cb     .grid(column=1, row=2, sticky=(E))

        arduino_lb         .grid(column=0,row=3)
        arduino_mini_f     .grid(column=1,row=3, sticky=(N,W,E,S))

        # in arduino_mini_f
        arduino_connect_btn.grid(column=0, row=0)
        arduino_light      .grid(column=1, row=0)

        arduino_log_txt    .grid(column=1, row=4)
        arduino_mini_f2    .grid(column=0, row=4, sticky=(N,W,E,S))

        #in arduino_mini_f2
        arduino_comport_lb.grid(column=0, row=0, sticky=(N))
        arduino_comport_cb.grid(column=1, row=0, sticky=(E,N))
        
        frame               .columnconfigure(0, weight = 1)
        frame               .columnconfigure(1, weight = 1)

        connection_status_lf.columnconfigure(0, weight=1)

        nova_mini_f     .columnconfigure(0, weight = 1)
        nova_mini_f     .columnconfigure(1, weight = 1)
        nova_mini_f     .rowconfigure(0, weight = 1)

        nova_mini_f2    .columnconfigure(0, weight = 1, minsize=120)
        nova_mini_f2    .columnconfigure(1, weight = 1)
        nova_mini_f2    .rowconfigure(0, weight=1)
        nova_mini_f2    .rowconfigure(1, weight=1)
        nova_mini_f2    .rowconfigure(2, weight=1)

        arduino_mini_f     .columnconfigure(0, weight = 1)
        arduino_mini_f     .columnconfigure(1, weight = 1)
        arduino_mini_f     .rowconfigure(0, weight = 1)

        arduino_mini_f2    .columnconfigure(0, weight=1, minsize=120)
        arduino_mini_f2    .columnconfigure(1, weight=1)
        arduino_mini_f2    .rowconfigure(0, weight=1)

        return frame