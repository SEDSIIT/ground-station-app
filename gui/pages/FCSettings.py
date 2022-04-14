import tkinter as tk
from tkinter import ttk, StringVar, Entry, Label
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
import os
import pandas as pd

import lib.app_settings as settings
import pages.HomePage

def switchbuttonstatus(m):
        button_status[m] = 1
        ### Send Button Information ###
        button_status[m] = 0
        print("Data Sent")

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
        filepath_fcconfig_header = os.path.join(settings.PATH, 'images', 'fcconfig_header_nobg.png')
        
        render = ImageTk.PhotoImage(Image.open(filepath_fcconfig_header))
        img = ttk.Label(self, image=render)
        img.image = render
        img.pack(pady=10, padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(pages.HomePage.HomePage))
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