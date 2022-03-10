'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This software is the ground station GUI software that will be used to view and
analyze flight data while also be able to configure the custom flight computer
built by the students of SEDS@IIT.

The goal is to make the software compatable with multiple OS enviroments with
minimal additional packages and easy to use for users unfamiliar with the
software.

TO DO:
# - fix bug on static plot need to move plot to see plotted data
# - have matplotlib plots appear in the gui window in quadrants
- have a performance metric bar on the side of the GUI
- be able to communicate with STM32F4 over USB (COM)
- have a window to print output of USB device
'''

### IMPORT START ###
from dataclasses import dataclass
from distutils import command
from faulthandler import disable
from glob import glob
import string
from turtle import width
import matplotlib
from matplotlib import image

from paramiko import Channel
from sqlalchemy import true

from sympy import expand

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import BOTH, DISABLED, TOP, Canvas, Entry, Label, PhotoImage, StringVar, ttk
from tkinter.filedialog import askopenfilename

import tkinter.font as tkFont

from PIL import ImageTk, Image

import pandas as pd
import numpy as np

import os
import sys

import shutil
import time
import threading
import glob
import serial as Serial
import pandas as pd
import numpy as np


import settings
### IMPORT END ###

### STYLING START ###
LARGE_FONT = ("Verdona", 12)
style.use("ggplot")

live_plot = Figure(figsize=(5,10), dpi=100)
live_plot_subplot1 = live_plot.add_subplot(221)
live_plot_subplot2 = live_plot.add_subplot(222)
live_plot_subplot3 = live_plot.add_subplot(223)
live_plot_subplot4 = live_plot.add_subplot(224)

live_table = Figure(figsize=(5,2), dpi=100)
live_table_subplot = live_table.add_subplot(111)

static_plot = Figure(figsize=(5,10), dpi=100)
static_plot_subplot1 = static_plot.add_subplot(221)
static_plot_subplot2 = static_plot.add_subplot(222)
static_plot_subplot3 = static_plot.add_subplot(223)
static_plot_subplot4 = static_plot.add_subplot(224)

static_table = Figure(figsize=(5,2), dpi=100)
static_table_subplot = static_table.add_subplot(111)

### STYLING END ###

### GLOBAL VARIABLES START ###
PATH = os.path.dirname(__file__)
if sys.platform == "linux" or sys.platform == "linux2":
    PLATFORM = "linux"
elif sys.platform == "darwin":
    PLATFORM = "macOS"
elif sys.platform == "win32":
    PLATFORM = "windows"
else:
    print("WARNING: Unrecognized platform")
    quit()

    
PATH_DATAFILE = os.path.join(PATH, 'data', 'Init.csv')
PATH_LIVEDATA = os.path.join(PATH, 'data', 'LiveData.csv') # placeholder
PATH_FSC = os.path.join(PATH, 'data', 'FSConfig_Saved.csv')

## For generating live data sim, comment out when not needed ##
PATH_HISTDATA = os.path.join(PATH, 'data', 'example_flight.csv')

### For Simulation Live Data Read. Comment out when reading actual live data ###
data = [[0,0,0,0,0]]
ex_livedata = pd.DataFrame(data, columns = ['Time', 'Altitude', 'Velocity', 'Latitude', 'Longitude'])
ex_livedata.to_csv(PATH_LIVEDATA)
rng = np.random.default_rng(seed=31)
### End Live Data Simulation ###


### GLOBAL VARIABLES END ###

### CLASS START ###
class GSApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
                
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        
        # File Menu 
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Save Settings", command = lambda: tk.messagebox.showinfo("Information","Not supported yet!"))
        fileMenu.add_command(label="Open", command= lambda: select_file())
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command = lambda: quit()) # Fixed?
        menubar.add_cascade(label="File", menu=fileMenu)

        # Page Menu
        pageMenu = tk.Menu(menubar, tearoff=0)
        pageMenu.add_command(label="Home", command = lambda: self.show_frame(HomePage))
        pageMenu.add_separator()
        pageMenu.add_command(label="Data Analysis", command = lambda: self.show_frame(DataAnalysis))
        pageMenu.add_command(label="FC Settings", command = lambda: self.show_frame(FCSettings))
        pageMenu.add_command(label="Live Flight Data", command = lambda: self.show_frame(LiveFlight))
        menubar.add_cascade(label="Page", menu=pageMenu)

        # Settings Menu
        settingsMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settingsMenu)

        # Help Menu
        helpMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpMenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        # Load all pages initially
        for page in (HomePage, DataAnalysis, FCSettings, LiveFlight):

            frame = page(container, self)

            self.frames[page] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(HomePage)

    # Show frame that is requested
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Individual Pages Start

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        # Create multiple widgets in a frame to make organization easier

        # title
        tk.Frame.__init__(self, parent)

        # Homescreen title
        fontStyle = tkFont.Font(family="Lucida Grande", size=32)
        label = ttk.Label(self, text=("Ad Astra Per Aspera"), font=fontStyle)
        label.pack(pady=5, padx=5) 
        label.place(relx=0.5, rely=0.1, anchor="n")
        
        # menu

        flightAnalysisButton = ttk.Button(self, text="Flight Analysis",
                            command=lambda: controller.show_frame(DataAnalysis))
        flightAnalysisButton.pack()
        flightAnalysisButton.place(relx=0.2, rely=0.2, anchor="n")


        fcComputerConfigButton = ttk.Button(self, text="Flight Computer Configuration",
                            command=lambda: controller.show_frame(FCSettings))
        fcComputerConfigButton.pack()
        fcComputerConfigButton.place(relx=0.4, rely=0.2, anchor="n")

        
        telemetryButton = ttk.Button(self, text="Telemetry",
                            command=lambda: controller.show_frame(Telemetry))
        telemetryButton.pack()
        telemetryButton.place(relx=0.6, rely=0.2, anchor="n")
        
        settingsButton = ttk.Button(self, text="Settings",
                            command=lambda: controller.show_frame(Settings))
        settingsButton.pack()
        settingsButton.place(relx=0.8, rely=0.2, anchor="n")
        
        # image
        filepath_logo_nobg = os.path.join(PATH, 'images', 'SEDSIIT-logo_noBG.png')
        
        render = ImageTk.PhotoImage(Image.open(filepath_logo_nobg))
        img = ttk.Label(self, image=render)
        img.image = render
        img.pack()
        img.place(relx=0.5, rely=0.3, anchor="n")

class Settings(tk.Frame):
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
                s = Serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, Serial.SerialException):
                pass
        return result
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Settings", font=LARGE_FONT)
        label.pack()    
        
        homeButton = ttk.Button(self, text="Home",
                    command=lambda: controller.show_frame(HomePage))
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
        write_connection_button = ttk.Button(fcConnect, text="WRTIE", command=lambda: fc_connection_test_write(fc_connect_button_clicked.get()))
        
        clear_output_button = ttk.Button(fcConnect, text="CLEAR OUTPUT", command=lambda: readOnlyText.delete("1.0","end"))
        
        # <<<fcConnect>>> HELPER FUNCTION DEFS START
        def fc_connection_set(comport):
            ser = Serial.Serial(comport, 115200)
            if not ser.isOpen():
                ser.open()
            readOnlyText.insert(1.0, comport + " is open and ready to go! \n")
        
        def fc_connection_test_read(comport):
            ser = Serial.Serial(comport, 115200)
            readOnlyText.insert(1.0, "************************\n")
            readOnlyText.insert(1.0, "READ TEST: READING FROM FLIGHT COMPUTER: \n")
            
            for i in range(5):
                data = ser.readline(1000)
                readOnlyText.insert(1.0, data)
            readOnlyText.insert(1.0, "SUCCESS!!\n")
                
        def fc_connection_test_write(comport):
            ser = Serial.Serial(comport, 115200)
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

class DataAnalysis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Grid.rowconfigure(self, (0,5), weight=1) 
        tk.Grid.columnconfigure(self, (0,4), weight=1) 
        
        label = ttk.Label(self, text="Data Analysis", font=LARGE_FONT)
        label.grid(column=2,row=0, sticky=tk.N)
        
        button_home = ttk.Button(self, text="Home",
                                    command=lambda: controller.show_frame(HomePage))
        button_home.grid(column=1,row=1)

        button_file_select = ttk.Button(self, text="Open File",
                                    command=lambda: select_file())
        button_file_select.grid(column=3, row=1)
        
        # static plot
        canvas = FigureCanvasTkAgg(static_plot, self)
        canvas.get_tk_widget().grid(column=0, row=5, columnspan=5, rowspan=1, sticky="NSEW")
        canvas.draw()
        
        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(column=0, row=4, columnspan=5, sticky=tk.W)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()
        
        # Static table
        canvas2 = FigureCanvasTkAgg(static_table, self)
        canvas2.get_tk_widget().grid(column=0, row=3, columnspan=5, rowspan=1, sticky="NSEW")
        canvas2.draw()
        
        toolbarFrame2 = tk.Frame(self)
        toolbarFrame2.grid(column=0, row=2, columnspan=5, sticky=tk.W)
        toolbar2 = NavigationToolbar2Tk(canvas2, toolbarFrame2)
        toolbar2.update()
        


class FCSettings(tk.Frame):
    def DeleteWarningMessageBoxPopup():
        tk.messagebox.showwarning("*Warning", "This will delete ALL DATA ON THE FLIGHT COMPUTER.\nAre you sure you want to delete all data?")
    
    def TestingPageWarningMessageBoxPopup(idx, m):
        if (idx == 6):
            tk.messagebox.showwarning("*Warning", "USE CAREFULLY! Test Pyro {}".format(m))
            switchbuttonstatus(m)
        else:
            pass
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Flight control settings header img        
        filepath_fcconfig_header = os.path.join(PATH, 'images', 'fcconfig_header_nobg.png')
        
        render = ImageTk.PhotoImage(Image.open(filepath_fcconfig_header))
        img = ttk.Label(self, image=render)
        img.image = render
        img.pack(pady=10, padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        homeButton.pack()

        savebutton = ttk.Button(self, text="Save Flight Control Settings", command=lambda: saveflightcontrolsettings(drogueDeployDelayEntryBox.get(),
            mainDeploymentAltitudeEntryBox.get(), pyroIgnitionTimeClicked.get(), self.auxPyroC_EnablePyroCheckboxValue.get(),
            auxPyroC_Clicked.get(),self.auxPyroC_DelayAfterFlagCheckBoxValue.get(),self.auxPyroD_EnablePyroCheckboxValue.get(),auxPyroD_Clicked.get(),
            self.auxPyroD_DelayAfterFlagCheckBoxValue.get(),self.auxPyroE_EnablePyroCheckboxValue.get(),auxPyroE_Clicked.get(),self.auxPyroE_DelayAfterFlagCheckBoxValue.get(),
            self.auxPyroF_EnablePyroCheckboxValue.get(),auxPyroF_Clicked.get(),self.auxPyroF_DelayAfterFlagCheckBoxValue.get(),transmitPowerClicked.get(),
            serialBuadRateClicked.get(),channelEntryBox.get(),transmitFlightRateClicked.get(),transmitLandingRateClicked.get(),callsignEntryBox.get(),
            dataSaveRateClicked.get(), buzzerFreqencyEntryBox.get(),buzzerBeepPatternClicked.get()))
        savebutton.pack()

        opensettingsbutton = ttk.Button(self, text="Open FC Settings", command=lambda: openflightsettingsfile(drogueDeployDelayEntryBox,
            mainDeploymentAltitudeEntryBox, pyroIgnitionTimeClicked,self.auxPyroC_EnablePyroCheckboxValue,auxPyroC_Clicked,self.auxPyroC_DelayAfterFlagCheckBoxValue, 
            self.auxPyroD_EnablePyroCheckboxValue,auxPyroD_Clicked, self.auxPyroD_DelayAfterFlagCheckBoxValue,self.auxPyroE_EnablePyroCheckboxValue,auxPyroE_Clicked,
            self.auxPyroE_DelayAfterFlagCheckBoxValue, self.auxPyroF_EnablePyroCheckboxValue,auxPyroF_Clicked,self.auxPyroF_DelayAfterFlagCheckBoxValue,transmitPowerClicked,
            serialBuadRateClicked,channelEntryBox,transmitFlightRateClicked,transmitLandingRateClicked,callsignEntryBox, dataSaveRateClicked, buzzerFreqencyEntryBox,buzzerBeepPatternClicked))
        opensettingsbutton.pack()
        
        # Flight control settings body        
        notebook = ttk.Notebook(self) 
        
        recovery = ttk.Frame(notebook)
        auxPyro = ttk.Frame(notebook)
        telemetryConfig = ttk.Frame(notebook)
        calibration = ttk.Frame(notebook)
        data = ttk.Frame(notebook)
        aux = ttk.Frame(notebook)
        testing = ttk.Frame(notebook)
        
        notebook.add(recovery, text="Recovery")
        notebook.add(auxPyro, text="Auxiliary Pyro")
        notebook.add(telemetryConfig, text="Telemetry Config")
        notebook.add(calibration, text="Calibration")
        notebook.add(data, text="Data")
        notebook.add(aux, text="Aux")
        notebook.add(testing, text="Testing")
        notebook.pack(padx=16, pady=30)
        
        #TODO: Fix the issue of no warning on testing tab when it is selected
        idx = notebook.index(notebook.select())
        pyrolabel = []
        notebook.bind('<<NotebookTabChanged>>', FCSettings.TestingPageWarningMessageBoxPopup(idx, pyrolabel))
        
        # Recovery frame <<<START>>>:
        #Drogue Deploy Delay
        drogueDeployDelayLabel = Label(recovery, text="Drogue Deploy Delay: ") 
        drogueDeployDelayEntryBox = Entry(recovery, width=12)
        drogueDeployDelaySetButton = ttk.Button(recovery, text="Set")
        #TODO: add stutus label for drogue deploy delay
        
        #Main deployment altitude (AGL)
        mainDeploymentAltitudeLabel = Label(recovery, text="Main deployment altitude (AGL): ") 
        mainDeploymentAltitudeEntryBox = Entry(recovery, width=12)
        mainDeploymentAltitudeSetButton = ttk.Button(recovery, text="Set")
        #TODO: add stutus label for main deployment altitude
        
        #Pyro igniton time
        global pyroIgnitionTimeOptions
        pyroIgnitionTimeOptions = [ "NULL",
                                    "NULL",
                                    "0.5 seconds",
                                    "1.0 seconds",
                                    "2.0 seconds",
                                    "3.0 seconds",
                                    "4.0 seconds",
                                    "5.0 seconds"]
        
        pyroIgnitionTimeClicked = StringVar()
        pyroIgnitionTimeClicked.set(pyroIgnitionTimeOptions[0])
        pyroIgnitionTimeDropdown = ttk.OptionMenu(recovery, pyroIgnitionTimeClicked, *pyroIgnitionTimeOptions)
        
        pyroIgnitionTimeLabel = Label(recovery, text="Pyro igniton time: ") 
        
        #Drogue Deploy Delay grid display 
        drogueDeployDelayLabel.grid(row=0, column=0, sticky="w")
        drogueDeployDelayEntryBox.grid(row=0, column=1, sticky="w")
        drogueDeployDelaySetButton.grid(row=0, column=2, sticky="w")
        
        #Main Deployment Altitude grid display
        mainDeploymentAltitudeLabel.grid(row=1, column=0, sticky="w")
        mainDeploymentAltitudeEntryBox.grid(row=1, column=1, sticky="w")
        mainDeploymentAltitudeSetButton.grid(row=1, column=2, sticky="w")
        
        #Pyro igniton time grid display
        pyroIgnitionTimeLabel.grid(row=2, column=0, sticky="w")
        pyroIgnitionTimeDropdown.grid(row=2, column=1, sticky="w")
        
        #LOGIC FOR RECOVERY
        #TODO: IMPLEMENT LOGIC FOR RECOVERY
        #<<<END>>> Recovery frame
    
        #Aux Pyro Frame <<<START>>>:
        auxPyroC_EnablePyroLabel = Label(auxPyro, text="Enable Pyros C: ") 
        auxPyroD_EnablePyroLabel = Label(auxPyro, text="Enable Pyros D: ") 
        auxPyroE_EnablePyroLabel = Label(auxPyro, text="Enable Pyros E: ") 
        auxPyroF_EnablePyroLabel = Label(auxPyro, text="Enable Pyros F: ") 
        
        auxPyroC_DeployPositionLabel = Label(auxPyro, text="Deploy position C: ")
        auxPyroD_DeployPositionLabel = Label(auxPyro, text="Deploy position D: ")
        auxPyroE_DeployPositionLabel = Label(auxPyro, text="Deploy position E: ")
        auxPyroF_DeployPositionLabel = Label(auxPyro, text="Deploy position F: ")
        
        auxPyroC_DelayAfterFlagLabel = Label(auxPyro, text="Delay C after Flag: ")
        auxPyroD_DelayAfterFlagLabel = Label(auxPyro, text="Delay D after Flag: ")
        auxPyroE_DelayAfterFlagLabel = Label(auxPyro, text="Delay E after Flag: ")
        auxPyroF_DelayAfterFlagLabel = Label(auxPyro, text="Delay F after Flag: ")

        self.auxPyroC_EnablePyroCheckboxValue = tk.IntVar(value=0)
        self.auxPyroD_EnablePyroCheckboxValue = tk.IntVar(value=0)
        self.auxPyroE_EnablePyroCheckboxValue = tk.IntVar(value=0)
        self.auxPyroF_EnablePyroCheckboxValue = tk.IntVar(value=0)

        self.auxPyroC_DelayAfterFlagCheckBoxValue = tk.IntVar(value=0)
        self.auxPyroD_DelayAfterFlagCheckBoxValue = tk.IntVar(value=0)
        self.auxPyroE_DelayAfterFlagCheckBoxValue = tk.IntVar(value=0)
        self.auxPyroF_DelayAfterFlagCheckBoxValue = tk.IntVar(value=0)
        
        auxPyroC_EnablePyroCheckBox = ttk.Checkbutton(auxPyro, variable=self.auxPyroC_EnablePyroCheckboxValue)
        auxPyroD_EnablePyroCheckBox = ttk.Checkbutton(auxPyro, variable=self.auxPyroD_EnablePyroCheckboxValue)
        auxPyroE_EnablePyroCheckBox = ttk.Checkbutton(auxPyro, variable=self.auxPyroE_EnablePyroCheckboxValue)
        auxPyroF_EnablePyroCheckBox = ttk.Checkbutton(auxPyro, variable=self.auxPyroF_EnablePyroCheckboxValue)
        
        auxPyroC_DelayAfterFlagCheckBox = ttk.Checkbutton(auxPyro, variable=self.auxPyroC_DelayAfterFlagCheckBoxValue)
        auxPyroD_DelayAfterFlagCheckBox = ttk.Checkbutton(auxPyro, variable=self.auxPyroD_DelayAfterFlagCheckBoxValue)
        auxPyroE_DelayAfterFlagCheckBox = ttk.Checkbutton(auxPyro, variable=self.auxPyroE_DelayAfterFlagCheckBoxValue)
        auxPyroF_DelayAfterFlagCheckBox = ttk.Checkbutton(auxPyro, variable=self.auxPyroF_DelayAfterFlagCheckBoxValue)

        global auxPryoDeployPositions
        auxPryoDeployPositions = [  "NULL",
                                    "NULL"
                                    "BECO",
                                    "Stage",
                                    "Separation",
                                    "MECO",
                                    "Apogee",
                                    "Main",
                                    "Deploy",
                                    "Landing"]
        
        auxPyroC_Clicked = StringVar()
        auxPyroC_Clicked.set(auxPryoDeployPositions[0])
        auxPyroC_DeployDropdown = ttk.OptionMenu(auxPyro, auxPyroC_Clicked, *auxPryoDeployPositions)

        auxPyroD_Clicked = StringVar()
        auxPyroD_Clicked.set(auxPryoDeployPositions[0])
        auxPyroD_DeployDropdown = ttk.OptionMenu(auxPyro, auxPyroD_Clicked, *auxPryoDeployPositions)

        auxPyroE_Clicked = StringVar()
        auxPyroE_Clicked.set(auxPryoDeployPositions[0])
        auxPyroE_DeployDropdown = ttk.OptionMenu(auxPyro, auxPyroE_Clicked, *auxPryoDeployPositions)
        
        auxPyroF_Clicked = StringVar()
        auxPyroF_Clicked.set(auxPryoDeployPositions[0])
        auxPyroF_DeployDropdown = ttk.OptionMenu(auxPyro, auxPyroF_Clicked, *auxPryoDeployPositions)

        #Aux Pyro for C
        auxPyroC_EnablePyroLabel.grid(row=0, column=0, sticky="w")
        auxPyroC_EnablePyroCheckBox.grid(row=0, column=1, sticky="w")
        auxPyroC_DeployPositionLabel.grid(row=1, column=0, sticky="w")
        auxPyroC_DeployDropdown.grid(row=1, column=1, sticky="w")
        auxPyroC_DelayAfterFlagLabel.grid(row=2, column=0, sticky="w")
        auxPyroC_DelayAfterFlagCheckBox.grid(row=2, column=1, sticky="w")

        #Aux Pyro for D
        auxPyroD_EnablePyroLabel.grid(row=4, column=0, sticky="w")
        auxPyroD_EnablePyroCheckBox.grid(row=4, column=1, sticky="w")
        auxPyroD_DeployPositionLabel.grid(row=5, column=0, sticky="w")
        auxPyroD_DeployDropdown.grid(row=5, column=1, sticky="w")
        auxPyroD_DelayAfterFlagLabel.grid(row=6, column=0, sticky="w")
        auxPyroD_DelayAfterFlagCheckBox.grid(row=6, column=1, sticky="w")

        #Aux Pyro for E
        auxPyroE_EnablePyroLabel.grid(row=8, column=0, sticky="w")
        auxPyroE_EnablePyroCheckBox.grid(row=8, column=1, sticky="w")
        auxPyroE_DeployPositionLabel.grid(row=9, column=0, sticky="w")
        auxPyroE_DeployDropdown.grid(row=9, column=1, sticky="w")
        auxPyroE_DelayAfterFlagLabel.grid(row=10, column=0, sticky="w")
        auxPyroE_DelayAfterFlagCheckBox.grid(row=10, column=1, sticky="w")

        #Aux Pyro for F
        auxPyroF_EnablePyroLabel.grid(row=12, column=0, sticky="w")
        auxPyroF_EnablePyroCheckBox.grid(row=12, column=1, sticky="w")
        auxPyroF_DeployPositionLabel.grid(row=13, column=0, sticky="w")
        auxPyroF_DeployDropdown.grid(row=13, column=1, sticky="w")
        auxPyroF_DelayAfterFlagLabel.grid(row=14, column=0, sticky="w")
        auxPyroF_DelayAfterFlagCheckBox.grid(row=14, column=1, sticky="w")
        
        #LOGIC FOR AUX PYRO
        #TODO: IMPLEMENT LOGIC FOR AUX PYRO
        #<<<END>>> AUX PYRO frame
        
        #TELEMETRY CONFIG: Frame <<<START>>>:
        transmitPowerLabel = ttk.Label(telemetryConfig, text="Transmit Power: ")
        global transmitPowerOptions
        transmitPowerOptions = ["NULL",
                                "NULL",
                                "-1 dBm", 
                                "2 dBm",
                                "5 dBm",
                                "8 dBm", 
                                "11 dBm", 
                                "14 dBm", 
                                "17 dBm", 
                                "20 dBm"]
        
        transmitPowerClicked = StringVar()
        transmitPowerClicked.set(transmitPowerOptions[0])
        transmitPowerDropdown = ttk.OptionMenu(telemetryConfig, transmitPowerClicked, *transmitPowerOptions)
        
        serialBuadRateLabel = ttk.Label(telemetryConfig, text="Serial Buad Rate: ")
        global serialBuadRateOptions
        serialBuadRateOptions = ["NULL", 
                                 "NULL",
                                 "1200 bps", 
                                 "2400 bps", 
                                 "4800 bps", 
                                 "9600 bps", 
                                 "19200 bps", 
                                 "38400 bps", 
                                 "57600 bps", 
                                 "115200 bps"]
        
        serialBuadRateClicked = StringVar()
        serialBuadRateClicked.set(serialBuadRateOptions[0])
        serialBuadRateDropdown = ttk.OptionMenu(telemetryConfig, serialBuadRateClicked, *serialBuadRateOptions)
        
        channelLabel = ttk.Label(telemetryConfig, text="Channel (1-100): ")
        channelEntryBox = Entry(telemetryConfig, width=12)
        channelSetButton = ttk.Button(telemetryConfig, text="Set")
        
        transmitFlightRateLabel = ttk.Label(telemetryConfig, text="Flight Transmit Rate: ")
        global transmitFlightRateOptions
        transmitFlightRateOptions = ["NULL", 
                                     "NULL",
                                     "1 hz", 
                                     "2 hz", 
                                     "5 hz", 
                                     "10 hz", 
                                     "20 hz"]
        
        transmitFlightRateClicked = StringVar()
        transmitFlightRateClicked.set(transmitFlightRateOptions[0])
        transmitFlightRateDropdown = ttk.OptionMenu(telemetryConfig, transmitFlightRateClicked, *transmitFlightRateOptions)
        
        transmitLandingRateLabel = ttk.Label(telemetryConfig, text="Landing Transmit Rate: ")
        global transmitLandingRateOptions
        transmitLandingRateOptions = ["NULL", 
                                      "NULL",
                                     "1 seconds", 
                                     "2 seconds", 
                                     "5 seconds", 
                                     "10 seconds", 
                                     "20 seconds",
                                     "30 seconds",
                                     "60 seconds"]
        
        transmitLandingRateClicked = StringVar()
        transmitLandingRateClicked.set(transmitLandingRateOptions[0])
        transmitLandingRateDropdown = ttk.OptionMenu(telemetryConfig, transmitLandingRateClicked, *transmitLandingRateOptions)
        
        callsignLabel = ttk.Label(telemetryConfig, text="Callsign: ")
        callsignEntryBox = Entry(telemetryConfig, width=12)
        callsignSetButton = ttk.Button(telemetryConfig, text="Set")
        
        transmitPowerLabel.grid(row=0, column=0, sticky="w")
        transmitPowerDropdown.grid(row=0, column=1, sticky="w")
        
        serialBuadRateLabel.grid(row=1, column=0, sticky="w")
        serialBuadRateDropdown.grid(row=1, column=1, sticky="w")
        
        channelLabel.grid(row=2, column=0, sticky="w")
        channelEntryBox.grid(row=2, column=1, sticky="w")
        channelSetButton.grid(row=2, column=2, sticky="w")
        
        transmitFlightRateLabel.grid(row=3, column=0, sticky="w")
        transmitFlightRateDropdown.grid(row=3, column=1, sticky="w")
        
        transmitLandingRateLabel.grid(row=4, column=0, sticky="w")
        transmitLandingRateDropdown.grid(row=4, column=1, sticky="w")
        
        callsignLabel.grid(row=5, column=0, sticky="w")
        callsignEntryBox.grid(row=5, column=1, sticky="w")
        callsignSetButton.grid(row=5, column=2, sticky="w")

        #LOGIC FOR TELEMETRY CONFIG
        #TODO: IMPLEMENT LOGIC FOR TELEMETRY CONFIG
        #<<<END>>> TELEMETRY CONFIG frame
        
        #CALIBRATION:: Frame <<<START>>>:
        global button_status
        button_status = {
            "calibrateAccelerometerButton": 0,
            "calibrateMagnetometerButton": 0,
            "downloadDataButton": 0,
            "dataDeleteButton": 0,
            "enablePWN_Button": 0,
            "enableBuzzer_Button": 0,
            "testPyroAButton": 0,
            "testPyroBButton": 0,
            "testPyroCButton": 0,
            "testPyroDButton": 0,
            "testPyroEButton": 0,
            "testPyroFButton": 0,

        }
        calibrateAccelerometerLabel = ttk.Label(calibration, text="Calibrate Accelerometer: ")
        calibrateAccelerometerButton = ttk.Button(calibration, text="RUN Calibrate", command=lambda m="calibrateAccelerometerButton": switchbuttonstatus(m))
        calibrateAccelerometerStatus = ttk.Label(calibration, text="Status: Null")
        
        calibrateMagnetometerLabel = ttk.Label(calibration, text="Calibrate Magnetometer: ")
        calibrateMagnetometerButton = ttk.Button(calibration, text="RUN Calibrate", command=lambda m="calibrateMagnetometerButton": switchbuttonstatus(m))
        calibrateMagnetometerStatus = ttk.Label(calibration, text="Status: NULL")
        
        calibrateAccelerometerLabel.grid(row=0, column=0, sticky="w")
        calibrateAccelerometerButton.grid(row=0, column=1, sticky="w")
        calibrateAccelerometerStatus.grid(row=0, column=2, sticky="w")
        
        calibrateMagnetometerLabel.grid(row=1, column=0, sticky="w")
        calibrateMagnetometerButton.grid(row=1, column=1, sticky="w")
        calibrateMagnetometerStatus.grid(row=1, column=2, sticky="w")
        
        #LOGIC FOR CALIBRATION
        #TODO: IMPLEMENT LOGIC FOR CALIBRATION
        #<<<END>>> CALIBRATION frame
        
        #DATA Frame <<<START>>>:
        downloadDataLabel = ttk.Label(data, text="Download Data: ")
        downloadDataButton = ttk.Button(data, text="Download", command=lambda m="downloadDataButton": switchbuttonstatus(m))
        downloadDataStatus = ttk.Label(data, text="Download Status: NULL")
        
        dataSaveRateLabel = ttk.Label(data, text="Data Save Rate: ")
        global dataSaveRateOptions
        dataSaveRateOptions = ["NULL", 
                               "NULL",
                               "1 hz",
                               "5 hz", 
                               "10 hz", 
                               "20 hz", 
                               "30 hz", 
                               "50 hz"]
        
        dataSaveRateClicked = StringVar()
        dataSaveRateClicked.set(dataSaveRateOptions[0])
        dataSaveRateDropdown = ttk.OptionMenu(data, dataSaveRateClicked, *dataSaveRateOptions)
        
        dataDeleteLabel = ttk.Label(data, text="Data Delete: ")
        dataDeleteButton = ttk.Button(data, text="*Delete", command=lambda m="dataDeleteButton": [FCSettings.DeleteWarningMessageBoxPopup(), switchbuttonstatus(m)])
        dataDeleteStatus = ttk.Label(data, text="Delete Status: NULL")
        
        downloadDataLabel.grid(row=0, column=0, sticky="w")
        downloadDataButton.grid(row=0, column=1, sticky="w")
        downloadDataStatus.grid(row=0, column=2, sticky="w")
        
        dataSaveRateLabel.grid(row=1, column=0, sticky="w")
        dataSaveRateDropdown.grid(row=1, column=1, sticky="w")
        
        dataDeleteLabel.grid(row=2, column=0, sticky="w")
        dataDeleteButton.grid(row=2, column=1, sticky="w")
        dataDeleteStatus.grid(row=2, column=2, sticky="w")
        
        #LOGIC FOR DATA
        #TODO: IMPLEMENT LOGIC FOR DATA
        #<<<END>>> DATA frame
        
        #Aux Frame <<<START>>>:
        enablePWM_Label = ttk.Label(aux, text="Enable PWM: ")
        enablePWN_Button = ttk.Button(aux, text="Enable", command=lambda m="enablePWN_Button": switchbuttonstatus(m))
        enablePWN_Status = ttk.Label(aux, text="Status: NULL")
        
        enableBuzzer_Label = ttk.Label(aux, text="Enable Buzzer: ")
        enableBuzzer_Button = ttk.Button(aux, text="Enable", command=lambda m="enableBuzzer_Button": switchbuttonstatus(m))
        enableBuzzer_Status = ttk.Label(aux, text="Status: NULL")
        
        buzzerFreqencyLabel = ttk.Label(aux, text="Buzzer Frequency (1800-2200): ")
        buzzerFreqencyEntryBox = Entry(aux, width=12)
        buzzerFreqencyStatus = ttk.Label(aux, text="Status: NULL")
        
        buzzerBeepPatternLabel = ttk.Label(aux, text="Buzzer Beep Pattern: ")
        global buzzerBeepPatternOptions
        buzzerBeepPatternOptions = ["NULL",
                                    "NULL",
                             "1",
                             "2",
                             "3",
                             "4"]
        
        buzzerBeepPatternClicked = StringVar()
        buzzerBeepPatternClicked.set(buzzerBeepPatternOptions[0])
        buzzerBeepPatternDropdown = ttk.OptionMenu(aux, buzzerBeepPatternClicked, *buzzerBeepPatternOptions)
        
        enablePWM_Label.grid(row=0, column=0, sticky="w")
        enablePWN_Button.grid(row=0, column=1, sticky="w")
        enablePWN_Status.grid(row=0, column=2, sticky="w")
        
        enableBuzzer_Label.grid(row=1, column=0, sticky="w")
        enableBuzzer_Button.grid(row=1, column=1, sticky="w")
        enableBuzzer_Status.grid(row=1, column=2, sticky="w")
        
        buzzerFreqencyLabel.grid(row=2, column=0, sticky="w")
        buzzerFreqencyEntryBox.grid(row=2, column=1, sticky="w")
        buzzerFreqencyStatus.grid(row=2, column=2, sticky="w")
        
        buzzerBeepPatternLabel.grid(row=3, column=0, sticky="w")
        buzzerBeepPatternDropdown.grid(row=3, column=1, sticky="w")
        
        #LOGIC FOR Aux
        #TODO: IMPLEMENT LOGIC FOR Aux
        #<<<END>>> Aux frame
        
        #Aux Frame <<<START>>>:
        testPyroALabel = ttk.Label(testing, text="*Test Pyro A: ")
        testPyroAButton = ttk.Button(testing, text="WARNING*Test", command=lambda m = "testPyroAButton": [FCSettings.TestingPageWarningMessageBoxPopup(6, m)])
        testPyroAStatus = ttk.Label(testing, text="Status: NULL")

        testPyroBLabel = ttk.Label(testing, text="*Test Pyro A: ")
        testPyroBButton = ttk.Button(testing, text="WARNING*Test", command=lambda m = "testPyroBButton": [FCSettings.TestingPageWarningMessageBoxPopup(6, m)])
        testPyroBStatus = ttk.Label(testing, text="Status: NULL")

        testPyroCLabel = ttk.Label(testing, text="*Test Pyro A: ")
        testPyroCButton = ttk.Button(testing, text="WARNING*Test", command=lambda m = "testPyroCButton": [FCSettings.TestingPageWarningMessageBoxPopup(6, m)])
        testPyroCStatus = ttk.Label(testing, text="Status: NULL")

        testPyroDLabel = ttk.Label(testing, text="*Test Pyro A: ")
        testPyroDButton = ttk.Button(testing, text="WARNING*Test", command=lambda m = "testPyroDButton": [FCSettings.TestingPageWarningMessageBoxPopup(6, m)])
        testPyroDStatus = ttk.Label(testing, text="Status: NULL")

        testPyroELabel = ttk.Label(testing, text="*Test Pyro A: ")
        testPyroEButton = ttk.Button(testing, text="WARNING*Test", command=lambda m = "testPyroEButton": [FCSettings.TestingPageWarningMessageBoxPopup(6, m)])
        testPyroEStatus = ttk.Label(testing, text="Status: NULL")

        testPyroFLabel = ttk.Label(testing, text="*Test Pyro A: ")
        testPyroFButton = ttk.Button(testing, text="WARNING*Test", command=lambda m = "testPyroFButton": [FCSettings.TestingPageWarningMessageBoxPopup(6, m)])
        testPyroFStatus = ttk.Label(testing, text="Status: NULL")
        
        testTelemetryLabel = ttk.Label(testing, text="Test Telemetry: ")
        testTelemetryButton = ttk.Button(testing, text="Test")
        testTelemetryStatus = ttk.Label(testing, text="Status: NULL")
        
        testGPS_Label = ttk.Label(testing, text="Test GPS: ")
        testGPS_Button = ttk.Button(testing, text="Test")
        testGPS_Status = ttk.Label(testing, text="Status: NULL")
        
        testAcclerometer1_Label = ttk.Label(testing, text="Test Accelerometer 1: ")
        testAcclerometer1_Button = ttk.Button(testing, text="Test")
        testAcclerometer1_status = ttk.Label(testing, text="Status: NULL")
        
        testAcclerometer2_Label = ttk.Label(testing, text="Test Accelerometer 2: ")
        testAcclerometer2_Button = ttk.Button(testing, text="Test")
        testAcclerometer2_status = ttk.Label(testing, text="Status: NULL")
        
        testPyroALabel.grid(row=0, column=0, sticky="w")
        testPyroAButton.grid(row=0, column=1, sticky="w")
        testPyroAStatus.grid(row=0, column=2, sticky="w")

        testPyroBLabel.grid(row=1, column=0, sticky="w")
        testPyroBButton.grid(row=1, column=1, sticky="w")
        testPyroBStatus.grid(row=1, column=2, sticky="w")

        testPyroCLabel.grid(row=2, column=0, sticky="w")
        testPyroCButton.grid(row=2, column=1, sticky="w")
        testPyroCStatus.grid(row=2, column=2, sticky="w")

        testPyroDLabel.grid(row=3, column=0, sticky="w")
        testPyroDButton.grid(row=3, column=1, sticky="w")
        testPyroDStatus.grid(row=3, column=2, sticky="w")

        testPyroELabel.grid(row=4, column=0, sticky="w")
        testPyroEButton.grid(row=4, column=1, sticky="w")
        testPyroEStatus.grid(row=4, column=2, sticky="w")

        testPyroFLabel.grid(row=5, column=0, sticky="w")
        testPyroFButton.grid(row=5, column=1, sticky="w")
        testPyroFStatus.grid(row=5, column=2, sticky="w")
        
        testTelemetryLabel.grid(row=6, column=0, sticky="w")
        testTelemetryButton.grid(row=6, column=1, sticky="w")
        testTelemetryStatus.grid(row=6, column=2, sticky="w")
        
        testGPS_Label.grid(row=7, column=0, sticky="w")
        testGPS_Button.grid(row=7, column=1, sticky="w")
        testGPS_Status.grid(row=7, column=2, sticky="w")
        
        testAcclerometer1_Label.grid(row=8, column=0, sticky="w")
        testAcclerometer1_Button.grid(row=8, column=1, sticky="w")
        testAcclerometer1_status.grid(row=8, column=2, sticky="w")
        
        testAcclerometer2_Label.grid(row=9, column=0, sticky="w")
        testAcclerometer2_Button.grid(row=9, column=1, sticky="w")
        testAcclerometer2_status.grid(row=9, column=2, sticky="w")

        global saved_information
        saved_information = {
            "drogueDeployDelay": drogueDeployDelayEntryBox.get(),
            "mainDeploymentAltitude": mainDeploymentAltitudeEntryBox.get(),
            "pyroIgnitionTime": pyroIgnitionTimeClicked.get(),
            "auxPyroC": self.auxPyroC_EnablePyroCheckboxValue.get(), 
            "auxPyroC_DeployPosition": auxPyroC_Clicked.get(),
            "auxPyroC_DelayAfterFlag": self.auxPyroC_DelayAfterFlagCheckBoxValue.get(),
            "auxPyroD": self.auxPyroD_EnablePyroCheckboxValue.get(),
            "auxPyroD_DeployPosition": auxPyroD_Clicked.get(),
            "auxPyroD_DelayAfterFlag": self.auxPyroD_DelayAfterFlagCheckBoxValue.get(),
            "auxPyroE": self.auxPyroE_EnablePyroCheckboxValue.get(),
            "auxPyroE_DeployPosition": auxPyroE_Clicked.get(),
            "auxPyroE_DelayAfterFlag": self.auxPyroE_DelayAfterFlagCheckBoxValue.get(),
            "auxPyroF": self.auxPyroF_EnablePyroCheckboxValue.get(),
            "auxPyroF_DeployPosition": auxPyroF_Clicked.get(),
            "auxPyroF_DelayAfterFlag": self.auxPyroF_DelayAfterFlagCheckBoxValue.get(),
            "transmitPower": transmitPowerClicked.get(),
            "serialBuadRate": serialBuadRateClicked.get(),
            "channel": channelEntryBox.get(),
            "transmitFlightRate": transmitFlightRateClicked.get(),
            "transmitLandingRate": transmitLandingRateClicked.get(),
            "callsignEntryBox": callsignEntryBox.get(),
            "dataSaveRate": dataSaveRateClicked.get(),
            "buzzerFreqency": buzzerFreqencyEntryBox.get(),
            "buzzerBeepPatternClicked": buzzerBeepPatternClicked.get()
        }
        #LOGIC FOR Testing
        #TODO: IMPLEMENT LOGIC FOR Testing

        #<<<END>>> Testing frame
        
        
        
        
        
        
        
        
        
        
class LiveFlight(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Grid.rowconfigure(self, (0,5), weight=1) 
        tk.Grid.columnconfigure(self, (0,4), weight=1) 
        
        label = ttk.Label(self, text="Telemetry", font=LARGE_FONT)
        label.grid(column=2,row=0, sticky=tk.N)
        
        button_home = ttk.Button(self, text="Home",
                                    command=lambda: controller.show_frame(HomePage))
        button_home.grid(column=1,row=1)


        button_file_select = ttk.Button(self, text="Save Flight",
                                    command=lambda: save_file())
        button_file_select.grid(column=3, row=1)
        
        canvas = FigureCanvasTkAgg(live_plot, self)
        canvas.get_tk_widget().grid(column=0, row=5, columnspan=5, rowspan=1, sticky="NSEW")
        canvas.draw()
        
        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(column=0, row=4, columnspan=5, sticky=tk.W)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()
        
        # Static table
        canvas2 = FigureCanvasTkAgg(live_table, self)
        canvas2.get_tk_widget().grid(column=0, row=3, columnspan=5, rowspan=1, sticky="NSEW")
        canvas2.draw()
        
        toolbarFrame2 = tk.Frame(self)
        toolbarFrame2.grid(column=0, row=2, columnspan=5, sticky=tk.W)
        toolbar2 = NavigationToolbar2Tk(canvas2, toolbarFrame2)
        toolbar2.update()
# Individual Pages End
### CLASS END ###


### FUNCTION DEFINE START ###
# Used to animate a matplotlib figure
def animate_live_plot(i):

    if (CURRENT_PAGE == "Telemetry"): # To do: add additional statement to require new data to update plot
        if (settings.DEBUG.status == True):
            start = time.time()
            print("\nTelemetry plot performance:")
    
        data = pd.read_csv(PATH_LIVEDATA)
        try:
            data.drop(["Events"], axis=1)
        except:
            if (settings.DEBUG.status == True):
                print("WARNING: No 'Events' in data file")
        
        if (settings.DEBUG.status == True):
            data_time_stop = time.time()
            print("Data Read Time: %f sec" %(data_time_stop-start))
            start = time.time()

        live_plot.subplots_adjust(hspace = 0.3)

        # Multi-threading start

        def plot_altitude():
            live_plot_subplot1.clear()
            live_plot_subplot1.plot(data['Time'], data['Altitude'], color='k')
            live_plot_subplot1.set_xlabel("Time (sec)")
            live_plot_subplot1.set_ylabel("AGL Altitude (ft)")

        def plot_velocity():
            live_plot_subplot2.clear()
            live_plot_subplot2.plot(data['Time'], data['Velocity'], color='k')
            live_plot_subplot2.set_xlabel("Time (sec)")
            live_plot_subplot2.set_ylabel("Velocity (ft/s)")

        def plot_acceleration():
            live_plot_subplot3.clear()
            live_plot_subplot3.plot(data['Time'], data['Acceleration'], color='k')
            live_plot_subplot3.set_xlabel("Time (sec)")
            live_plot_subplot3.set_ylabel("Acceleration (G)")

        def plot_coordinates():
            live_plot_subplot4.clear()
            live_plot_subplot4.plot(data['Longitude'], data['Latitude'], color='k')
            live_plot_subplot4.set_xlabel("Longitude (deg)")
            live_plot_subplot4.set_ylabel("Latitude (deg)")

        t1 = threading.Thread(target=plot_altitude)
        t2 = threading.Thread(target=plot_velocity)
        t3 = threading.Thread(target=plot_acceleration)
        t4 = threading.Thread(target=plot_coordinates)
        
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        if (settings.DEBUG.status == True):
            data_plot_stop = time.time()
            print("Plot Time: %f sec\n" %(data_plot_stop-start))


def animate_live_table(i):
    if (CURRENT_PAGE == "Telemetry"): # To Do: add additional statement to require new data flag
        data = pd.read_csv(PATH_LIVEDATA)

        try:
            max_altitude = max(data['Altitude'])
            max_altitude_index = np.where(data['Altitude'] == max_altitude)
        except:
            max_altitude = 0
            max_altitude_index = 0
            if (settings.DEBUG.status == True):
                print("WARNING: Could not find max altitude!")
            return None
        
        try:
            max_velocity = max(data['Velocity'])
            max_velocity_index = np.where(data['Velocity'] == max_velocity)
        except:
            max_velocity = 0
            max_velocity_index = 0
            if (settings.DEBUG.status == True):
                print("WARNING: Could not find max velocity!")
            return None

        try:
            max_acceleration = max(data['Acceleration'])
            max_acceleration_index = np.where(data['Acceleration'] == max_acceleration)
        except:
            max_acceleration = 0
            max_acceleration_index = 0
            if (settings.DEBUG.status == True):
                print("Warning: Could not find max acceleration!")
            return None
        try:
            data_length = len(data["Latitude"]) - 1
            latitude = data['Latitude'][data_length]
            longitude = data['Longitude'][data_length]
        except:
            latitude = 0
            longitude = 0
            if (settings.DEBUG.status == True):
                print("Warning: Could not find coordinates!")
            return None
        
        data_table = [[max_velocity, round(data['Time'][max_velocity_index[0][0]],2)],
                        [max_altitude, round(data['Time'][max_altitude_index[0][0]],2)],
                        [latitude, round(data['Time'][len(data['Time'])-1],2)], 
                        [longitude, round(data['Time'][len(data['Time'])-1],2)]]
        
        
        useful_params = pd.DataFrame(data_table, index = ['Max Velocity [m/s]', 'Apogee [m]', 'Current Latitude', 'Current Longitude'], columns = ['Value', 'Time [s]'])

        live_table_subplot.clear()

        # Table parameters
        live_table.patch.set_visible(False)
        live_table_subplot.axis('off')
        live_table_subplot.table(cellText=useful_params.values, colLabels=useful_params.columns, rowLabels=useful_params.index, loc='center')
        live_table.tight_layout()


def plot_static(): 
    data = pd.read_csv(PATH_DATAFILE)
    data.drop(["Events"], axis=1)
   
    static_plot_subplot1.clear()
    static_plot_subplot2.clear()
    static_plot_subplot3.clear()
    static_plot_subplot4.clear()
    static_plot_subplot1.plot(data['Time'], data['Altitude'], color='k')
    static_plot.subplots_adjust(hspace = 0.3)
    static_plot_subplot2.plot(data['Time'], data['Velocity'], color='r')
    static_plot_subplot1.set_xlabel("Time (sec)")
    static_plot_subplot1.set_ylabel("AGL Altitude (ft)")

    static_plot_subplot2.plot(data['Time'], data['Velocity'], color='k')
    static_plot_subplot2.set_xlabel("Time (sec)")
    static_plot_subplot2.set_ylabel("Velocity (ft/s)")
    
    static_plot_subplot3.plot(data['Time'], data['Acceleration'], color='k')
    static_plot_subplot3.set_xlabel("Time (sec)")
    static_plot_subplot3.set_ylabel("Acceleration (G)")

    static_plot_subplot4.plot(data['Latitude'], data['Longitude'], color='k')
    static_plot_subplot4.set_xlabel("Longitude (deg)")
    static_plot_subplot4.set_ylabel("Latitude (deg)")


def table_static():
    data = pd.read_csv(PATH_DATAFILE)
    try:
        data.drop(["Events"], axis=1)
    except:
        if (settings.DEBUG.status == True):
            print("WARNING: No 'Events' in data file")
    
    try:
        max_altitude = max(data['Altitude'])
        max_altitude_index = np.where(data['Altitude'] == max_altitude)
    except:
        max_altitude = 0
        max_altitude_index = 0
        if (settings.DEBUG.status == True):
            print("WARNING: Could not find max altitude!")
    
    try:
        max_velocity = max(data['Velocity'])
        max_velocity_index = np.where(data['Velocity'] == max_velocity)
    except:
        max_velocity = 0
        max_velocity_index = 0
        if (settings.DEBUG.status == True):
            print("WARNING: Could not find max velocity!")

    try:
        max_acceleration = max(data['Acceleration'])
        max_acceleration_index = np.where(data['Acceleration'] == max_acceleration)
    except:
        max_acceleration = 0
        max_acceleration_index = 0
        if (settings.DEBUG.status == True):
            print("Warning: Could not find max acceleration!")

    try:
        data_length = len(data["Latitude"]) - 1
        latitude = data['Latitude'][data_length]
        longitude = data['Longitude'][data_length]
    except:
        latitude = 0
        longitude = 0
        if (settings.DEBUG.status == True):
            print("Warning: Could not find coordinates!")
    
    data_table = None
    data_table = [[max_velocity, round(data['Time'][max_velocity_index[0][0]],2)], [max_altitude, round(data['Time'][max_altitude_index[0][0]],2)],
        [latitude, round(data['Time'][len(data['Time'])-1],2)], 
        [longitude, round(data['Time'][len(data['Time'])-1],2)]]
    
    useful_params = None
    useful_params = pd.DataFrame(data_table, index = ['Max Velocity [m/s]', 'Apogee [m]', 'Current Latitude', 'Current Longitude'], columns = ['Value', 'Time [s]'])


    live_table_subplot.clear()

    #The Table
    live_table.patch.set_visible(False)
    live_table_subplot.axis('off')
    live_table_subplot.table(cellText=useful_params.values, colLabels=useful_params.columns, rowLabels=useful_params.index, loc='center')
    live_table.tight_layout()

    ### Generating Live Data. COMMENT OUT WHEN ACTUALLY READING LIVE DATA ###

    data = pd.read_csv(PATH_LIVEDATA)
    data_total = pd.read_csv(PATH_HISTDATA)
    s = np.size(data['Time'])

    vel = data_total['Velocity'][(s*10)-1]
    alt = data_total['Altitude'][(s*10)-1]
    time = data_total['Time'][(s*10)-1]
    lat = rng.integers(low=0, high=1000, size=1)
    lat = lat[0]
    lon = rng.integers(low=0, high=1000, size=1)
    lon = lon[0]

    os.remove(PATH_LIVEDATA)
    new_data = pd.DataFrame(
        {
            "Time": [time],
            "Altitude": [alt],
            "Velocity": [vel],
            "Latitude": [lat],
            "Longitude": [lon],
        })
    data = pd.concat([data, new_data])
    data.to_csv(PATH_LIVEDATA)
    ### END generating live data ###

def plot_static(): 
    data = pd.read_csv(PATH_DATAFILE)
    data.drop(["Events"], axis=1)
   
    static_plot_subplot1.clear()
    static_plot_subplot2.clear()
    static_plot_subplot3.clear()
    static_plot_subplot4.clear()
    static_plot_subplot1.plot(data['Time'], data['Altitude'], color='k')
    static_plot.subplots_adjust(hspace = 0.3)
    static_plot_subplot2.plot(data['Time'], data['Velocity'], color='r')
    static_plot_subplot1.set_xlabel("Time (sec)")
    static_plot_subplot1.set_ylabel("AGL Altitude (ft)")
    static_plot_subplot2.set_xlabel("Time (sec)")
    static_plot_subplot2.set_ylabel("Velocity (ft/s)")
    static_plot_subplot3 
    static_plot_subplot4
    
def saveflightcontrolsettings(drogueDeployDelayEntryBox, mainDeploymentAltitudeEntryBox, pyroIgnitionTimeClicked,\
        auxPyroC_EnablePyroCheckboxValue,auxPyroC_Clicked,auxPyroC_DelayAfterFlagCheckBoxValue,auxPyroD_EnablePyroCheckboxValue,\
        auxPyroD_Clicked,auxPyroD_DelayAfterFlagCheckBoxValue,auxPyroE_EnablePyroCheckboxValue,auxPyroE_Clicked,\
        auxPyroE_DelayAfterFlagCheckBoxValue,auxPyroF_EnablePyroCheckboxValue,auxPyroF_Clicked,auxPyroF_DelayAfterFlagCheckBoxValue,\
        transmitPowerClicked,serialBuadRateClicked,channelEntryBox,transmitFlightRateClicked,transmitLandingRateClicked,callsignEntryBox,\
        dataSaveRateClicked,buzzerFreqencyEntryBox,\
        buzzerBeepPatternClicked):
        saved_information["drogueDeployDelay"] = [drogueDeployDelayEntryBox]
        saved_information["mainDeploymentAltitude"] = [mainDeploymentAltitudeEntryBox]
        saved_information["pyroIgnitionTime"] = [pyroIgnitionTimeClicked]
        saved_information["auxPyroC"] = [auxPyroC_EnablePyroCheckboxValue]
        saved_information["auxPyroC_DeployPosition"] =  [auxPyroC_Clicked]
        saved_information["auxPyroC_DelayAfterFlag"] = [auxPyroC_DelayAfterFlagCheckBoxValue]
        saved_information["auxPyroD"] = [auxPyroD_EnablePyroCheckboxValue]
        saved_information["auxPyroD_DeployPosition"] = [auxPyroD_Clicked]
        saved_information["auxPyroD_DelayAfterFlag"] = [auxPyroD_DelayAfterFlagCheckBoxValue]
        saved_information["auxPyroE"] = [auxPyroE_EnablePyroCheckboxValue]
        saved_information["auxPyroE_DeployPosition"] = [auxPyroE_Clicked]
        saved_information["auxPyroE_DelayAfterFlag"] = [auxPyroE_DelayAfterFlagCheckBoxValue]
        saved_information["auxPyroF"] = [auxPyroF_EnablePyroCheckboxValue]
        saved_information["auxPyroF_DeployPosition"] = [auxPyroF_Clicked]
        saved_information["auxPyroF_DelayAfterFlag"] = [auxPyroF_DelayAfterFlagCheckBoxValue]
        saved_information["transmitPower"] = [transmitPowerClicked]
        saved_information["serialBuadRate"] = [serialBuadRateClicked]
        saved_information["channel"] = [channelEntryBox]
        saved_information["transmitFlightRate"] = [transmitFlightRateClicked]
        saved_information["transmitLandingRate"] = [transmitLandingRateClicked]
        saved_information["callsignEntryBox"] = [callsignEntryBox]
        saved_information["dataSaveRate"] = [dataSaveRateClicked]
        saved_information["buzzerFreqency"] = [buzzerFreqencyEntryBox]
        saved_information["buzzerBeepPatternClicked"] = [buzzerBeepPatternClicked]

        FSdf = pd.DataFrame.from_dict(saved_information)
        FSdf.to_csv(PATH_FSC)

        ### Add Code to send the information ###
        print('Flight Settings Saved')



    window_width = int(screen_width * settings.window.scale_width)
    window_height = int(screen_height * settings.window.scale_height)

    window_dimensions = str(window_width) + "x" + str(window_height)
    
    if (settings.DEBUG.status == True):
        print("Window Stats:")
        print("screen width:", screen_width)
        print("window width scale:", settings.window.scale_width)
        print("window width:", window_width)
        print("screen height:", screen_height)
        print("window height scale:", settings.window.scale_height)
        print("window height:", window_height)
        print("window dimensions:", window_dimensions)
        print()

    return window_dimensions
    
# Resizes window to force window update for "DataAnalysis" page
def refresh():
    screen_height = app.winfo_height()
    screen_width = app.winfo_width()

    geometry_string = str(screen_width + 10) + "x" + str(screen_height + 10)
    app.geometry(geometry_string)

    if (settings.DEBUG.status == True):
        print("Refreshing window...")
    
def select_file():
    global PATH_DATAFILE

    PATH_DATAFILE = askopenfilename()
    print("Selected data file path: %s" % (PATH_DATAFILE))
    plot_static()

def openflightsettingsfile(drogueDeployDelayEntryBox, mainDeploymentAltitudeEntryBox, pyroIgnitionTimeClicked, auxPyroC_EnablePyroCheckboxValue,auxPyroC_Clicked,\
    auxPyroC_DelayAfterFlagCheckBoxValue, auxPyroD_EnablePyroCheckboxValue,auxPyroD_Clicked, auxPyroD_DelayAfterFlagCheckBoxValue, auxPyroE_EnablePyroCheckboxValue,\
    auxPyroE_Clicked,auxPyroE_DelayAfterFlagCheckBoxValue, auxPyroF_EnablePyroCheckboxValue,auxPyroF_Clicked, auxPyroF_DelayAfterFlagCheckBoxValue,transmitPowerClicked, \
    serialBuadRateClicked,channelEntryBox,transmitFlightRateClicked,transmitLandingRateClicked,callsignEntryBox, dataSaveRateClicked, buzzerFreqencyEntryBox,\
    buzzerBeepPatternClicked):
    global PATH_FSC
    PATH_FSC = askopenfilename()
    print("Selected Flight Settings Configuation file path: %s" % (PATH_FSC))
    global saved_information
    saved_information = pd.read_csv(PATH_FSC)
    saved_information.to_dict('dict')
    del saved_information[saved_information.columns[0]]
    drogueDeployDelayEntryBox.insert(0,saved_information["drogueDeployDelay"][0])
    mainDeploymentAltitudeEntryBox.insert(0,saved_information["mainDeploymentAltitude"][0])
    pyroIgnitionTimeClicked.set(pyroIgnitionTimeOptions[pyroIgnitionTimeOptions.index(saved_information["pyroIgnitionTime"][0])])
    auxPyroC_EnablePyroCheckboxValue.set(saved_information["auxPyroC"][0])
    auxPyroC_Clicked.set(auxPryoDeployPositions[auxPryoDeployPositions.index(saved_information["auxPyroC_DeployPosition"][0])])
    auxPyroC_DelayAfterFlagCheckBoxValue.set(saved_information["auxPyroC_DelayAfterFlag"])
    auxPyroD_EnablePyroCheckboxValue.set(saved_information["auxPyroD"][0])
    auxPyroD_Clicked.set(auxPryoDeployPositions[auxPryoDeployPositions.index(saved_information["auxPyroD_DeployPosition"][0])])
    auxPyroD_DelayAfterFlagCheckBoxValue.set(saved_information["auxPyroD_DelayAfterFlag"])
    auxPyroE_EnablePyroCheckboxValue.set(saved_information["auxPyroE"][0])
    auxPyroE_Clicked.set(auxPryoDeployPositions[auxPryoDeployPositions.index(saved_information["auxPyroE_DeployPosition"][0])])
    auxPyroE_DelayAfterFlagCheckBoxValue.set(saved_information["auxPyroE_DelayAfterFlag"])
    auxPyroF_EnablePyroCheckboxValue.set(saved_information["auxPyroF"][0])
    auxPyroF_Clicked.set(auxPryoDeployPositions[auxPryoDeployPositions.index(saved_information["auxPyroF_DeployPosition"][0])])
    auxPyroF_DelayAfterFlagCheckBoxValue.set(saved_information["auxPyroF_DelayAfterFlag"])
    transmitPowerClicked.set(transmitPowerOptions[transmitPowerOptions.index(saved_information["transmitPower"][0])])
    serialBuadRateClicked.set(serialBuadRateOptions[serialBuadRateOptions.index(saved_information["serialBuadRate"][0])])
    channelEntryBox.insert(0,saved_information["channel"][0])
    transmitFlightRateClicked.set(transmitFlightRateOptions[transmitFlightRateOptions.index(saved_information["transmitFlightRate"][0])])
    transmitLandingRateClicked.set(transmitLandingRateOptions[transmitLandingRateOptions.index(saved_information["transmitLandingRate"][0])])
    callsignEntryBox.insert(0,saved_information["callsignEntryBox"][0])
    dataSaveRateClicked.set(dataSaveRateOptions[dataSaveRateOptions.index(saved_information["dataSaveRate"][0])])
    buzzerFreqencyEntryBox.insert(0,saved_information["buzzerFreqency"][0])
    buzzerBeepPatternClicked.set(buzzerBeepPatternOptions[buzzerBeepPatternOptions.index(str(saved_information["buzzerBeepPatternClicked"][0]))])

    print('Settings Loaded')
    
def switchbuttonstatus(m):
    button_status[m] = 1
    ### Send Button Information ###
    button_status[m] = 0
    print("Data Sent")

    try:
        temp_file_path = askopenfilename()
    except:
        print("Warning: file path not valid: %s " %(temp_file_path))
        return None
    PATH_DATAFILE = temp_file_path
    if (settings.DEBUG.status == True):
        print("Selected data file path: %s" % (PATH_DATAFILE))
    #GSApp.show_frame(DataAnalysis) 
    plot_static()
    table_static()
    refresh()

# Saves temporary telemetry flight data file and saves it in a specified location
def save_file(): 
    global PATH_LIVEDATA, PATH_DATAFILE
    PATH_DATAFILE = asksaveasfilename(filetypes=[("comma separated value (*.csv)", "*.csv")]) + ".csv"
    shutil.copyfile(PATH_LIVEDATA, PATH_DATAFILE)
    if (settings.DEBUG.status == True):
        print("Taking telemetry file: %s" %(PATH_LIVEDATA))
        print("Saving as: %s" %(PATH_DATAFILE))

# Clear temporary telemetry flight data file
def telemetry_file_init():
    global PATH_LIVEDATA
    if os.path.exists(PATH_LIVEDATA):
        os.remove(PATH_LIVEDATA)
    else:
        print("WARNING: Telemetry file not found!")
    temp_file = open(PATH_LIVEDATA,"x")
    temp_file.write("Time,Altitude,Velocity,Acceleration,Latitude,Longitude,Events\n") # empty header
    temp_file.close()
    if (settings.DEBUG.status == True):
        print("Clearing temp file: %s" %(PATH_LIVEDATA))


### MAIN START ###
def main():
    ### SETUP START ###
    if (settings.DEBUG.status == True):
        print("Starting ground station GUI...\n")
    
    telemetry_file_init()

    ### SETUP END ###

    global app 
    app = GSApp()
    app.geometry(get_win_dimensions(app))
    app.minsize(600,400)
    app.title("Ground Station Application")


    if (PLATFORM == "windows"):
        filepath_icon_photo = os.path.join(PATH, 'images', 'SEDSIIT-logo_icon.ico')
        app.iconbitmap(filepath_icon_photo)
    else:
        filepath_icon_photo = os.path.join(PATH, 'images', 'SEDSIIT-logo.png')
        app.tk.call('wm','iconphoto',app._w,tk.Image("photo", file=filepath_icon_photo))
    #app.tk.call('wm','iconphoto',app._w,tk.Image("photo", file=filepath_icon_photo))

    ani = animation.FuncAnimation(live_plot, animate_live_plot, interval=500)
    ani2 = animation.FuncAnimation(live_table, animate_live_table, interval=500)
    
    app.mainloop()
### MAIN END ###
### FUNCTION DEFINE END ###

if __name__ == '__main__':
    main()