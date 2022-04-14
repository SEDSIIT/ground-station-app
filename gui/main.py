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

from dataclasses import dataclass
from distutils import command
from faulthandler import disable
import string
from turtle import width

import matplotlib
import matplotlib.animation as animation
import tkinter as tk
import os
import sys

# Local imports
import lib.app_settings as settings
import lib.plotting
import lib.window
import lib.files

import pages.core

### IMPORT END ###

### STYLING START ###
matplotlib.use("TkAgg")
lib.plotting.plotting_init()
### STYLING END ###

### GLOBAL VARIABLES START ###
settings.PATH = os.path.dirname(__file__)
if sys.platform == "linux" or sys.platform == "linux2":
    settings.PLATFORM = "linux"
elif sys.platform == "darwin":
    settings.PLATFORM = "macOS"
elif sys.platform == "win32":
    settings.PLATFORM = "windows"
else:
    print("WARNING: Unrecognized platform")
    quit()

settings.PATH_LIVEDATA = os.path.join(settings.PATH, 'data', 'temp', 'TELEMETRY_TEMP.csv') # location of telemetry data
#PATH_LIVEDATA = os.path.join(PATH, 'data', 'TEST_FLIGHT.csv') # plot sample data (Note: also comment out telemetry_file_int in main())
settings.PATH_DATAFILE = settings.PATH_LIVEDATA

settings.CURRENT_PAGE = "HomePage"
### GLOBAL VARIABLES END ###

### MAIN START ###
def main():
    ### SETUP START ###
    if (settings.DEBUG.status == True):
        print("Starting ground station GUI...\n")
    
    lib.files.telemetry_file_init()
    ### SETUP END ###

    global app 
    app = pages.core.GSApp()
    app.geometry(lib.window.get_win_dimensions())
    app.minsize(600,400)
    app.title("Ground Station Application")

    if (settings.PLATFORM == "windows"):
        filepath_icon_photo = os.path.join(settings.PATH, 'images', 'SEDSIIT-logo_icon.ico')
        app.iconbitmap(filepath_icon_photo)
    else:
        filepath_icon_photo = os.path.join(settings.PATH, 'images', 'SEDSIIT-logo.png')
        app.tk.call('wm','iconphoto',app._w,tk.Image("photo", file=filepath_icon_photo))
    
    animation.FuncAnimation(lib.plotting.live_plot, lib.plotting.animate_live_plot, interval=500)
    animation.FuncAnimation(lib.plotting.live_table, lib.plotting.animate_live_table, interval=500)
    
    app.mainloop()
### MAIN END ###

if (__name__ == '__main__'):
    main()