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
    
def refresh(self,page,parent,controller): 

        self.destroy()
        self.__init__(parent,controller)
        frame = page(parent,controller)
        controller.frames[page] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        controller.show_frame(page)

        # TODO: add functionality to auto refresh for live feed
        # self.after(100,self.refresh(parent,controller))
