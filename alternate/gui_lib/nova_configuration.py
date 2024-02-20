from tkinter import *
from tkinter import ttk

def nova_configuration(parent):
        frame = ttk.Frame(parent, padding=(10,10,10,10))
        frame['width'] = 384
        frame['borderwidth'] = 2
        frame['relief'] = 'raised'
        return frame