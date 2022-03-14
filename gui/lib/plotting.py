'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

ABOUT:
This handles how the static and live figures are plotted in the DataAnalysis
and Telemetry pages
'''
import threading
import lib.app_settings as settings
import pandas as pd
import numpy as np

from matplotlib.figure import Figure
from matplotlib import style
import time

import lib.app_settings as settings


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

def plotting_init():
    '''Initialize and configure subplots'''
    style.use("ggplot")

    global live_plot, live_plot_subplot1, live_plot_subplot2, live_plot_subplot3, live_plot_subplot4
    global live_table, live_table_subplot
    global static_plot, static_plot_subplot1, static_plot_subplot2, static_plot_subplot3, static_plot_subplot4
    global static_table, static_table_subplot

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

def animate_live_plot(i):
    '''Used to create an animated matplotlib plot'''
    if (settings.CURRENT_PAGE == "Telemetry"): # To do: add additional statement to require new data to update plot
        if (settings.DEBUG.status == True):
            start = time.time()
            print("\nTelemetry plot performance:")
    
        data = pd.read_csv(settings.PATH_LIVEDATA)
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
    '''Used to create an animated matplotlib table'''
    if (settings.CURRENT_PAGE == "Telemetry"): # To Do: add additional statement to require new data flag
        data = pd.read_csv(settings.PATH_LIVEDATA)

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
        
        
        useful_params = pd.DataFrame(data_table, index = ['Max Velocity [ft/s]', 'Apogee [ft]', 'Current Latitude', 'Current Longitude'], columns = ['Value', 'Time [s]'])

        live_table_subplot.clear()

        # Table parameters
        live_table.patch.set_visible(False)
        live_table_subplot.axis('off')
        live_table_subplot.table(cellText=useful_params.values, colLabels=useful_params.columns, rowLabels=useful_params.index, loc='center')
        live_table.tight_layout()


def table_static():
    '''Used to create a static matplotlib table'''
    data = pd.read_csv(settings.PATH_DATAFILE)
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
    useful_params = pd.DataFrame(data_table, index = ['Max Velocity [ft/s]', 'Apogee [ft]', 'Current Latitude[deg]', 'Current Longitude[deg]'], columns = ['Value', 'Time [s]'])

    static_table_subplot.clear()

    # table parameters
    static_table.patch.set_visible(False)
    static_table_subplot.axis('off')
    static_table_subplot.table(cellText=useful_params.values, colLabels=useful_params.columns, rowLabels=useful_params.index, loc='center')
    static_table.tight_layout()

def plot_static(): 
    '''Used to create a static matplotlib plot'''
    data = pd.read_csv(settings.PATH_DATAFILE)
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
    
    static_plot_subplot2.plot(data['Time'], data['Velocity'], color='k')
    static_plot_subplot2.set_xlabel("Time (sec)")
    static_plot_subplot2.set_ylabel("Velocity (ft/s)")
    
    static_plot_subplot3.plot(data['Time'], data['Acceleration'], color='k')
    static_plot_subplot3.set_xlabel("Time (sec)")
    static_plot_subplot3.set_ylabel("Acceleration (G)")

    static_plot_subplot4.plot(data['Latitude'], data['Longitude'], color='k')
    static_plot_subplot4.set_xlabel("Longitude (deg)")
    static_plot_subplot4.set_ylabel("Latitude (deg)")