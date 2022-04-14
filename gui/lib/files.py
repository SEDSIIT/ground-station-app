from tkinter.filedialog import askopenfilename, asksaveasfilename
import lib.app_settings as settings
import lib.plotting as plot
import lib.window
import os
import shutil

def select_file():
    '''Creates a window to select a file and plots the file data on the DataAnalysis page'''
    try:
        temp_file_path = askopenfilename()
    except:
        print("Warning: file path not valid: %s " %(temp_file_path))
        return None
    settings.PATH_DATAFILE = temp_file_path
    if (settings.DEBUG.status == True):
        print("Selected data file path: %s" % (settings.PATH_DATAFILE))
    plot.plot_static()
    plot.table_static()
    lib.window.refresh()

def save_file(): 
    '''Save the current data on the temporary telemetry data file on a file of the user's choosing'''
    if (settings.PLATFORM == "windows"):
        settings.PATH_DATAFILE = asksaveasfilename(filetypes=[("comma separated value (*.csv)", "*.csv")]) + ".csv"
    else:
        settings.PATH_DATAFILE = asksaveasfilename(filetypes=[("comma separated value (*.csv)", "*.csv")])
    shutil.copyfile(settings.PATH_LIVEDATA, settings.PATH_DATAFILE)
    if (settings.DEBUG.status == True):
        print("Taking telemetry file: %s" %(settings.PATH_LIVEDATA))
        print("Saving as: %s" %(settings.PATH_DATAFILE))

def telemetry_file_init():
    '''Clear temporary telemetry flight data file'''
    if os.path.exists(settings.PATH_LIVEDATA):
        os.remove(settings.PATH_LIVEDATA)
    else:
        print("WARNING: Telemetry file not found!")
    temp_file = open(settings.PATH_LIVEDATA,"x")
    temp_file.write("Time,Altitude,Velocity,Acceleration,Latitude,Longitude,Events\n") # empty header
    temp_file.close()
    if (settings.DEBUG.status == True):
        print("Clearing temp file: %s" %(settings.PATH_LIVEDATA))

