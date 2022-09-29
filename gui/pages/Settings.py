import tkinter as tk
from tkinter import ttk, StringVar
import sys
import glob
import serial


import pages.HomePage
import lib.app_settings as settings


class Settings(tk.Frame):
    '''Page to configure communication between GSApp and USB device'''
    # This function creates and connects to the flight computer COM port 
    # (SHOULD SUPPORT ALL PLATFORMS LINUX MAC AND WINDOWS)
    def serial_ports_finder():
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except:
                pass
        return result
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Settings", font=settings.LARGE_FONT)
        label.pack()    
        
        homeButton = ttk.Button(self, text="Home",
                    command=lambda: controller.show_frame(pages.HomePage.HomePage))
        homeButton.pack()
        
        # Connection control body        
        notebook = ttk.Notebook(self) 
        
        fcConnect = ttk.Frame(notebook)
        nilConnect1 = ttk.Frame(notebook)
        nilConnect2 = ttk.Frame(notebook)
        nilConnect3 = ttk.Frame(notebook)
        nilConnect4 = ttk.Frame(notebook)
        nilConnect5 = ttk.Frame(notebook)
        nilConnect6 = ttk.Frame(notebook)
        nilConnect7 = ttk.Frame(notebook)
        
        notebook.add(fcConnect, text="FC Connect")
        notebook.add(nilConnect1, text="nilConnect1")
        notebook.add(nilConnect2, text="nilConnect2")
        notebook.add(nilConnect3, text="nilConnect3")
        #notebook.add(nilConnect4, text="nilConnect4")
        #notebook.add(nilConnect5, text="nilConnect5")
        #notebook.add(nilConnect6, text="nilConnect6")
        #notebook.add(nilConnect6, text="nilConnect7")
        notebook.pack(padx=16, pady=30)
        

        # <<<fcConnect>>> START
        fc_connections_label = ttk.Label(fcConnect, text="Flight Computer COMPORT: ")
        fc_connections_options = Settings.serial_ports_finder() #setting up connection to FC
        
        fc_connect_button_clicked = StringVar()
        
        fc_connect_button_dropdown = ttk.OptionMenu(fcConnect, fc_connect_button_clicked, *fc_connections_options)
        
        set_connection_button_lable = ttk.Label(fcConnect, text="Set connection: ")
        set_connection_button = ttk.Button(fcConnect, text="SET", command=lambda: fc_connection_set(fc_connect_button_clicked.get()))
        
        test_connection_button_lable = ttk.Label(fcConnect, text="READ connection: ")
        test_connection_button = ttk.Button(fcConnect, text="READ", command=lambda: fc_connection_test_read(fc_connect_button_clicked.get()))
        
        write_connection_button_lable = ttk.Label(fcConnect, text="WRITE connection: ")
        write_connection_button = ttk.Button(fcConnect, text="WRITE", command=lambda: fc_connection_test_write(fc_connect_button_clicked.get()))
        
        clear_output_button = ttk.Button(fcConnect, text="CLEAR OUTPUT", command=lambda: readOnlyText.delete("1.0","end"))
        
        # <<<fcConnect>>> HELPER FUNCTION DEFS START
        def fc_connection_set(comport):
            ser = serial.Serial(comport, 115200)
            if not ser.isOpen():
                ser.open()
            readOnlyText.insert(1.0, comport + " is open and ready to go! \n")
        
        def fc_connection_test_read(comport):
            ser = serial.Serial(comport, 115200)
            readOnlyText.insert(1.0, "************************\n")
            readOnlyText.insert(1.0, "READ TEST: READING FROM FLIGHT COMPUTER: \n")
            
            for i in range(5):
                data = ser.readline(1000)
                readOnlyText.insert(1.0, data)
            readOnlyText.insert(1.0, "SUCCESS!!\n")
                
        def fc_connection_test_write(comport):
            ser = serial.Serial(comport, 115200)
            readOnlyText.insert(1.0, "************************\n")
            readOnlyText.insert(1.0, "WRITE TEST: WRITING DATA TO FLIGHT COMPUTER: \n")
            send = "WROTE DATA SUCCESSFULLY! NOT "
            for i in range(5):
                ser.write( send.encode())
                data = ser.readline(1000)
                readOnlyText.insert(1.0, data)
            readOnlyText.insert(1.0, "SUCCESS!!\n")
        
        def readOnlyTextBox(event):
            if(12==event.state and event.keysym=='c' ):
                return
            else:
                return "break"
        # <<<fcConnect>>> HELPER FUNCTION DEFS END
        
        
        readOnlyText = tk.Text(fcConnect, width=90,height=50,font=('Time 15 bold'),fg="black")
        readOnlyText.insert(1.0, "WAITING FOR CONNECTION TO BE SET!\n")
        readOnlyText.bind("<Key>", lambda e: readOnlyTextBox(e)) #STOPS ALL KEYS FROM WORKING WITHIN TEXTBOX
        
        
        fc_connections_label.grid(row=0, column=0, sticky="w")
        fc_connect_button_dropdown.grid(row=0, column=1, sticky="w")
        
        set_connection_button_lable.grid(row=1, column=0, sticky="w")
        set_connection_button.grid(row=1, column=1, sticky="w")
    
        test_connection_button_lable.grid(row=2, column=0,sticky="w")
        test_connection_button.grid(row=2, column=1, sticky="w")
        
        write_connection_button_lable.grid(row=3, column=0,sticky="w")
        write_connection_button.grid(row=3, column=1, sticky="w")
        
        clear_output_button.grid(row=4, column=1, sticky="w")
        readOnlyText.grid(row = 5, column = 0, columnspan = 2, rowspan = 2, padx = 2, pady = 3)
        # <<<fcConnect>>> END
