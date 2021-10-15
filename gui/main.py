'''
This software is the ground station GUI software that will
be used to view and analyze flight data while also be able
to configure the custom flight computer built by the
students of SEDS@IIT.

The goal is to make the software compatable with multiple
OS enviroments with minimal additional packages and easy
to use for users unfamiliar with the software.

TO DO:
- have matplotlib plots appear in the gui window in quadrants
- have a performance metric bar on the side of the GUI
- be able to communicate with USB devices
- have a window to print output of USB device
- be able to send messages to USB device
'''

### IMPORT START ###
from typing import AsyncIterable
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd
import numpy as np

import settings
### IMPORT END ###

LARGE_FONT = ("Verdona", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)



### CLASS START ###
class GSApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
                
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Settings", command = lambda: tk.messagebox.showinfo("Information","Not supported yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command = quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (HomePage, DataAnalysis, FCConfig, LiveFlight):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(HomePage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Individual Pages Start

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text=("Ad Astra Per Aspera"), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Data Analysis",
                            command=lambda: controller.show_frame(DataAnalysis))
        button.pack()

        button2 = ttk.Button(self, text="Flight Computer Configure",
                            command=lambda: controller.show_frame(FCConfig))
        button2.pack()

        button3 = ttk.Button(self, text="Live Flight Data",
                            command=lambda: controller.show_frame(LiveFlight))
        button3.pack()


class DataAnalysis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Data Analysis", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()
        # Plots
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class FCConfig(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Flight Computer Configure", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()


class LiveFlight(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Telemetry Data", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()


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
    
    if (DEBUG == True):
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
def animate(i):
    pullData = open("sampledata.txt","r").read()
    dataList = pullData.split("\n")
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    a.clear()
    a.plot(xList, yList)


def main():
    app = GSApp()
    app.geometry(get_win_dimensions(app))
    app.title("Ground Station Application")
    img = tk.Image("photo", file="SEDSIIT-logo.png")
    app.tk.call('wm','iconphoto',app._w,img)
    ani = animation.FuncAnimation(f, animate, interval=1000)
    app.mainloop()

### FUNCTION DEFINE END ###


### SETUP START ###
DEBUG = True
if (DEBUG == True):
    print("Starting ground station GUI...")
    print()

### SETUP END ###



### MAIN START ###
if __name__ == '__main__':
    main()
### MAIN END ###