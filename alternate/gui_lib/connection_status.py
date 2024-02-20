from tkinter import *
from tkinter import ttk

def connection_status(parent):
        frame = ttk.Frame(parent, padding=(10,10,10,10))
        frame['width'] = 384
        frame['borderwidth'] = 10
        frame['relief'] = 'sunken'
        return frame