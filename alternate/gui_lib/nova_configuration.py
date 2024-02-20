from tkinter import *
from tkinter import ttk

def nova_configuration(parent):
        frame = ttk.Frame(parent, padding=(10,10,10,10))
        frame['width'] = 384
        frame['height'] = 600
        frame['borderwidth'] = 10
        frame['relief'] = 'groove'
        return frame