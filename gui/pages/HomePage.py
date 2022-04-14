import tkinter as tk
from tkinter import ttk
import os
from PIL import ImageTk, Image

import lib.app_settings
import pages.HomePage
import pages.DataAnalysis
import pages.FCSettings
import pages.Telemetry
import pages.Settings

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        # Create multiple widgets in a frame to make organization easier

        # title
        tk.Frame.__init__(self, parent)

        # Homescreen title
        label = ttk.Label(self, text=("Ad Astra Per Aspera"), font=lib.app_settings.LARGE_FONT)
        label.pack(pady=5, padx=5) 
        label.place(relx=0.5, rely=0.1, anchor="n")
        
        # menu
        flightAnalysisButton = ttk.Button(self, text="Flight Analysis",
                            command=lambda: controller.show_frame(pages.DataAnalysis.DataAnalysis))
        flightAnalysisButton.pack()
        flightAnalysisButton.place(relx=0.2, rely=0.2, anchor="n")


        fcComputerConfigButton = ttk.Button(self, text="Flight Computer Configuration",
                            command=lambda: controller.show_frame(pages.FCSettings.FCSettings))
        fcComputerConfigButton.pack()
        fcComputerConfigButton.place(relx=0.4, rely=0.2, anchor="n")

        
        telemetryButton = ttk.Button(self, text="Telemetry",
                            command=lambda: controller.show_frame(pages.Telemetry.Telemetry))
        telemetryButton.pack()
        telemetryButton.place(relx=0.6, rely=0.2, anchor="n")
        
        settingsButton = ttk.Button(self, text="Settings",
                            command=lambda: controller.show_frame(pages.Settings.Settings))
        settingsButton.pack()
        settingsButton.place(relx=0.8, rely=0.2, anchor="n")
        
        # image
        filepath_logo_nobg = os.path.join(lib.app_settings.PATH, 'images', 'SEDSIIT-logo_noBG.png')
        
        render = ImageTk.PhotoImage(Image.open(filepath_logo_nobg))
        img = ttk.Label(self, image=render)
        img.image = render
        img.pack()
        img.place(relx=0.5, rely=0.3, anchor="n")