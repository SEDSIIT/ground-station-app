import tkinter as tk
import lib.app_settings as settings
import pages.core 

# Get window screen information to scale window properly
def get_win_dimensions():
    '''Get window screen information to scale window properly'''
    root = tk.Tk() # "hacky" work around

    settings.screen.height = root.winfo_screenheight()
    settings.screen.width = root.winfo_screenwidth()

    settings.window.height = int(settings.screen.height * settings.window.scale_height)
    settings.window.width = int(settings.screen.width * settings.window.scale_width)

    window_dimensions = str(settings.window.width) + "x" + str(settings.window.height)
    
    if (settings.DEBUG.status == True):
        print("Window Stats:")
        print("screen width:", settings.screen.width)
        print("window width scale:", settings.window.scale_width)
        print("window width:", settings.window.width)
        print("screen height:", settings.screen.height)
        print("window height scale:", settings.window.scale_height)
        print("window height:", settings.window.height)
        print("window dimensions:", window_dimensions)
        print()
    root.destroy()
    return window_dimensions
    
def refresh(): 
    '''
    ### CURRENTLY DOES NOT WORK ###
    Resizes window to force window update for "DataAnalysis" page
    '''
    geometry_string = str(settings.window.width + 10) + "x" + str(settings.window.height + 10)
    pages.core.GSApp.geometry(geometry_string) # This part does not work

    if (settings.DEBUG.status == True):
        print("Refreshing window...")