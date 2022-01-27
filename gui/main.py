'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This software is the ground station GUI software that willbe used to view and
analyze flight data while also be able to configure the custom flight computer
built by the students of SEDS@IIT.

The goal is to make the software compatable with multiple OS enviroments with
minimal additional packages and easy to use for users unfamiliar with the
software.

TO DO:
- make all files and data relative
- fix the quit() define bug
- have matplotlib plots appear in the gui window in quadrants
- have a performance metric bar on the side of the GUI
- be able to communicate with STM32F4 over USB (COM)
- have a window to print output of USB device
'''

### IMPORT START ###
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import Canvas, Label, ttk
from tkinter.filedialog import askopenfilename

from PIL import ImageTk, Image

import pandas as pd
import numpy as np

import settings
import os
### IMPORT END ###

### STYLING START ###
LARGE_FONT = ("Verdona", 12)
style.use("ggplot")

live_figure = Figure(figsize=(5,5), dpi=100)
live_figure_subplot = live_figure.add_subplot(111)


### STYLING END ###

### GLOBAL VARIABLES START ###
PATH = os.path.dirname(__file__)
### GLOBAL VARIABLES END ###

### CLASS START ###
class GSApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
                
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
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
        pageMenu.add_command(label="FC Config", command = lambda: self.show_frame(FCConfig))
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
        for page in (HomePage, DataAnalysis, FCConfig, LiveFlight):

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
        label = ttk.Label(self, text=("Ad Astra Per Aspera"), font=LARGE_FONT)
        label.pack()
        label.place(relx=0.5, rely=0.1, anchor="n")
        
        # menu
        button = ttk.Button(self, text="Data Analysis",
                            command=lambda: controller.show_frame(DataAnalysis))
        button.pack()
        button.place(relx=0.3, rely=0.2, anchor="n")

        button2 = ttk.Button(self, text="Flight Computer Configure",
                            command=lambda: controller.show_frame(FCConfig))
        button2.pack()
        button2.place(relx=0.5, rely=0.2, anchor="n")

        button3 = ttk.Button(self, text="Live Flight Data",
                            command=lambda: controller.show_frame(LiveFlight))
        button3.pack()
        button3.place(relx=0.7, rely=0.2, anchor="n")
        
        # image
        filepath_logo_nobg = os.path.join(PATH,"images\\SEDSIIT-logo_noBG.png")
        render = ImageTk.PhotoImage(Image.open(filepath_logo_nobg))
        img = ttk.Label(self, image=render)
        img.image = render
        img.pack()
        img.place(relx=0.5, rely=0.3, anchor="n")
        


class DataAnalysis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Data Analysis", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()
        # plot


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

        # Live Plot
        canvas = FigureCanvasTkAgg(live_figure, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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
    file_path_historical= os.path.join(PATH, 'data\\example_data.csv')

    data_historical = pd.read_csv(file_path_historical)
    data_historical.drop(["Events"], axis=1)
    
    live_figure_subplot.clear()
    live_figure_subplot.plot(data_historical['Time'], data_historical['Altitude'], color="k")
    live_figure_subplot.plot(data_historical['Time'], data_historical['Velocity'], color="r")
    live_figure_subplot.set_xlabel("Time (sec)")
    live_figure_subplot.set_ylabel("Height (ft)")



def select_file():
    file_dir = askopenfilename()

### MAIN START ###
def main():
    ### SETUP START ###
    if (settings.DEBUG.status == True):
        print("Starting ground station GUI...")
        print()
    ### SETUP END ###

    app = GSApp()
    app.geometry(get_win_dimensions(app))
    app.minsize(600,400)
    app.title("Ground Station Application")

    filepath_icon_photo = os.path.join(PATH, 'images\\SEDSIIT-logo.png')
    app.tk.call('wm','iconphoto',app._w,tk.Image("photo", file=filepath_icon_photo))

    ani = animation.FuncAnimation(live_figure, animate_live_plot, interval=500)

    app.mainloop()
### MAIN END ###
### FUNCTION DEFINE END ###

if __name__ == '__main__':
    main()