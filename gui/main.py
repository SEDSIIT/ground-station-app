'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

ABOUT:
This software is the ground station GUI software that will be used to view and
analyze flight data while also be able to configure the custom flight computer
built by the students of SEDS@IIT.

The goal is to make the software compatable with multiple OS enviroments with
minimal additional packages and easy to use for users unfamiliar with the
software.

TODO:
For latest tasks go to: https://github.com/SEDSIIT/ground-station-app/projects/1
'''

### IMPORT START ###
import matplotlib
from matplotlib import image
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style


import tkinter as tk
from tkinter import TOP, Entry, Label, StringVar, ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.font as tkFont

from PIL import ImageTk, Image

import os
import sys
import shutil
import time
import threading
import pandas as pd

import settings
### IMPORT END ###

### STYLING START ###
LARGE_FONT = ("Verdona", 12)
style.use("ggplot")

live_plot = Figure(figsize=(5,5), dpi=100)
live_plot_subplot1 = live_plot.add_subplot(221)
live_plot_subplot2 = live_plot.add_subplot(222)
live_plot_subplot3 = live_plot.add_subplot(223)
live_plot_subplot4 = live_plot.add_subplot(224)

static_plot = Figure(figsize=(5,5), dpi=100)
static_plot_subplot1 = static_plot.add_subplot(221)
static_plot_subplot2 = static_plot.add_subplot(222)
static_plot_subplot3 = static_plot.add_subplot(223)
static_plot_subplot4 = static_plot.add_subplot(224)

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

PATH_LIVEDATA = os.path.join(PATH, 'data', 'temp', 'telemetry_temp.csv') # location of telemetry data
PATH_DATAFILE = PATH_LIVEDATA

CURRENT_PAGE = "HomePage"

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
        fileMenu.add_command(label="Save As", command = lambda: save_file())
        fileMenu.add_command(label="Open", command= lambda: select_file())
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command = lambda: quit()) 
        menubar.add_cascade(label="File", menu=fileMenu)

        # Page Menu
        pageMenu = tk.Menu(menubar, tearoff=0)
        pageMenu.add_command(label="Home", command = lambda: self.show_frame(HomePage))
        pageMenu.add_separator()
        pageMenu.add_command(label="Data Analysis", command = lambda: self.show_frame(DataAnalysis))
        pageMenu.add_command(label="FC Config", command = lambda: self.show_frame(FCSettings))
        pageMenu.add_command(label="Telemetry", command = lambda: self.show_frame(Telemetry))
        menubar.add_cascade(label="Page", menu=pageMenu)

        # Settings Menu
        menubar.add_command(label="Settings", command=lambda: self.show_frame(Settings))

        # Help Menu
        menubar.add_command(label="Help", command=lambda: tk.messagebox.showinfo("Information","Not supported yet!"))

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        # Load all pages initially
        for page in (HomePage, DataAnalysis, FCSettings, Telemetry, Settings):

            frame = page(container, self)

            self.frames[page] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(HomePage)

    # Show frame that is requested
    def show_frame(self, cont):
        global CURRENT_PAGE
        if (cont.__name__ == 'DataAnalysis'):
            CURRENT_PAGE = "DataAnalysis"
        elif (cont.__name__ == 'FCSettings'):
            CURRENT_PAGE = "FCSettings"
        elif (cont.__name__ == 'Telemetry'):
            CURRENT_PAGE = "Telemetry"
        elif (cont.__name__ == 'Settings'):
            CURRENT_PAGE = "Settings"
        else:
            CURRENT_PAGE = "HomePage" 
        if (settings.DEBUG.status == True):
            print("CURRENT_PAGE: %s" %(CURRENT_PAGE))
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
        button = ttk.Button(self, text="Flight Analysis",
                            command=lambda: controller.show_frame(DataAnalysis))
        button.pack()
        button.place(relx=0.3, rely=0.2, anchor="n")

        button2 = ttk.Button(self, text="Flight Computer Configuration",
                            command=lambda: controller.show_frame(FCSettings))
        button2.pack()
        button2.place(relx=0.5, rely=0.2, anchor="n")

        button3 = ttk.Button(self, text="Telemetry",
                            command=lambda: controller.show_frame(Telemetry))
        button3.pack()
        button3.place(relx=0.7, rely=0.2, anchor="n")
        
        # image
        filepath_logo_nobg = os.path.join(PATH, 'images', 'SEDSIIT-logo_noBG.png')
        
        render = ImageTk.PhotoImage(Image.open(filepath_logo_nobg))
        img = ttk.Label(self, image=render)
        img.image = render
        img.pack()
        img.place(relx=0.5, rely=0.3, anchor="n")

class Settings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Settings", font=LARGE_FONT)
        label.grid(column=1, row=0)

        
        
        homeButton = ttk.Button(self, text="Home",
                    command=lambda: controller.show_frame(HomePage))
        homeButton.grid(column=1,row=1)
        


class DataAnalysis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Data Analysis", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button_file_select = ttk.Button(self, text="Select File",
                                    command=lambda: select_file())
        button_file_select.pack(side=TOP)

        # static plot
        canvas = FigureCanvasTkAgg(static_plot, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()
        

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)



class FCSettings(tk.Frame):
    def DeleteWarningMessageBoxPopup():
        tk.messagebox.showwarning("*Warning", "This will delete ALL DATA ON THE FLIGHT COMPUTER.\nAre you sure you want to delete all data?")
    
    def TestingPageWarningMessageBoxPopup(idx):
        if (idx == 6):
            tk.messagebox.showwarning("*Warning", "USE CAREFULLY! (placeholder warning)")
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
        notebook.bind('<<NotebookTabChanged>>', FCSettings.TestingPageWarningMessageBoxPopup(idx))
        
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
        pyroIgnitionTimeOptions = [ "NULL",
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

        auxPryoDeployPositions = [  "NULL",
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
        transmitPowerOptions = ["NULL",
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
        serialBuadRateOptions = ["NULL", 
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
        transmitFlightRateOptions = ["NULL", 
                                     "1 hz", 
                                     "2 hz", 
                                     "5 hz", 
                                     "10 hz", 
                                     "20 hz"]
        
        transmitFlightRateClicked = StringVar()
        transmitFlightRateClicked.set(transmitFlightRateOptions[0])
        transmitFlightRateDropdown = ttk.OptionMenu(telemetryConfig, transmitFlightRateClicked, *transmitFlightRateOptions)
        
        transmitLandingRateLabel = ttk.Label(telemetryConfig, text="Landing Transmit Rate: ")
        transmitLandingRateOptions = ["NULL", 
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
        calibrateAccelerometerLabel = ttk.Label(calibration, text="Calibrate Accelerometer: ")
        calibrateAccelerometerButton = ttk.Button(calibration, text="RUN Calibrate")
        calibrateAccelerometerStatus = ttk.Label(calibration, text="Status: NULL")
        
        calibrateMagnetometerLabel = ttk.Label(calibration, text="Calibrate Magnetometer: ")
        calibrateMagnetometerButton = ttk.Button(calibration, text="RUN Calibrate")
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
        downloadDataButton = ttk.Button(data, text="Download")
        downloadDataStatus = ttk.Label(data, text="Download Status: NULL")
        
        dataSaveRateLabel = ttk.Label(data, text="Data Save Rate: ")
        dataSaveRateOptions = ["NULL", 
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
        dataDeleteButton = ttk.Button(data, text="*Delete", command=lambda: FCSettings.DeleteWarningMessageBoxPopup())
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
        enablePWN_Button = ttk.Button(aux, text="Enable")
        enablePWN_Status = ttk.Label(aux, text="Status: NULL")
        
        enableBuzzer_Label = ttk.Label(aux, text="Enable Buzzer: ")
        enableBuzzer_Button = ttk.Button(aux, text="Enable")
        enableBuzzer_Status = ttk.Label(aux, text="Status: NULL")
        
        buzzerFreqencyLabel = ttk.Label(aux, text="Buzzer Frequency (1800-2200): ")
        buzzerFreqencyEntryBox = Entry(aux, width=12)
        buzzerFreqencyStatus = ttk.Label(aux, text="Status: NULL")
        
        buzzerBeepPatternLabel = ttk.Label(aux, text="Buzzer Beep Pattern: ")
        buzzerBeepPatternOptions = ["NULL",
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
        testPyroLabel = ttk.Label(testing, text="*Test Pyro: ")
        testPyroButton = ttk.Button(testing, text="WARNING*Test", command=lambda: FCSettings.TestingPageWarningMessageBoxPopup(6))
        testPyroStatus = ttk.Label(testing, text="Status: NULL")
        
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
        
        testPyroLabel.grid(row=0, column=0, sticky="w")
        testPyroButton.grid(row=0, column=1, sticky="w")
        testPyroStatus.grid(row=0, column=2, sticky="w")
        
        testTelemetryLabel.grid(row=1, column=0, sticky="w")
        testTelemetryButton.grid(row=1, column=1, sticky="w")
        testTelemetryStatus.grid(row=1, column=2, sticky="w")
        
        testGPS_Label.grid(row=2, column=0, sticky="w")
        testGPS_Button.grid(row=2, column=1, sticky="w")
        testGPS_Status.grid(row=2, column=2, sticky="w")
        
        testAcclerometer1_Label.grid(row=3, column=0, sticky="w")
        testAcclerometer1_Button.grid(row=3, column=1, sticky="w")
        testAcclerometer1_status.grid(row=3, column=2, sticky="w")
        
        testAcclerometer2_Label.grid(row=4, column=0, sticky="w")
        testAcclerometer2_Button.grid(row=4, column=1, sticky="w")
        testAcclerometer2_status.grid(row=4, column=2, sticky="w")
        #LOGIC FOR Testing
        #TODO: IMPLEMENT LOGIC FOR Testing
        #<<<END>>> Testing frame
        
        
class Telemetry(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Telemetry Data", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        # Live Plot
        canvas = FigureCanvasTkAgg(live_plot, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
# Individual Pages End
### CLASS END ###


### FUNCTION DEFINE START ###
# Get window screen information to scale window properly
def get_win_dimensions(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

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

        # Multi-threading start (Note: this takes longer than a single thread)

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

        t1.join()
        t2.join()
        t3.join()
        t4.join()

        if (settings.DEBUG.status == True):
            data_plot_stop = time.time()
            print("Plot Time: %f sec\n" %(data_plot_stop-start))


def plot_static(): 
    data = pd.read_csv(PATH_DATAFILE)
    try:
        data.drop(["Events"], axis=1)
    except:
        if (settings.DEBUG.status == True):
            print("WARNING: No 'Events' in data file")
    static_plot.subplots_adjust(hspace = 0.3)

    static_plot_subplot1.clear()
    static_plot_subplot2.clear()
    static_plot_subplot3.clear()
    static_plot_subplot4.clear()
    
    static_plot_subplot1.plot(data['Time'], data['Altitude'], color='k')
    static_plot_subplot1.set_xlabel("Time (sec)")
    static_plot_subplot1.set_ylabel("AGL Altitude (ft)")
    
    static_plot_subplot2.plot(data['Time'], data['Velocity'], color='r')
    static_plot_subplot2.set_xlabel("Time (sec)")
    static_plot_subplot2.set_ylabel("Velocity (ft/s)")
    
    static_plot_subplot3.set_xlabel("Time (sec)")
    static_plot_subplot3.set_ylabel("Acceleration (G)")

    static_plot_subplot4.set_xlabel("Longitude (deg)")
    static_plot_subplot4.set_ylabel("Latitude (deg)")

# Select a flight data file to read
def select_file():
    global PATH_DATAFILE
    PATH_DATAFILE = askopenfilename()
    if (settings.DEBUG.status == True):
        print("Selected data file path: %s" % (PATH_DATAFILE))
    #GSApp.show_frame(DataAnalysis) 
    plot_static()
    
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
        print("Starting ground station GUI...")
        print()
    ### SETUP END ###
    telemetry_file_init()

    app = GSApp()
    app.geometry(get_win_dimensions(app))
    app.minsize(600,400)
    app.title("Ground Station Application")

    filepath_icon_photo = os.path.join(PATH, 'images', 'SEDSIIT-logo.png')
    app.tk.call('wm','iconphoto',app._w,tk.Image("photo", file=filepath_icon_photo))


    ani = animation.FuncAnimation(live_plot, animate_live_plot, interval=1000)
   
    app.mainloop()
### MAIN END ###
### FUNCTION DEFINE END ###

if __name__ == '__main__':
    main()