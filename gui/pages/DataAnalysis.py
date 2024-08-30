import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import lib.app_settings as settings
import pages.HomePage
import pages.DataAnalysis
import lib.plotting
import lib.files


class DataAnalysis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Grid.rowconfigure(self, (0,5), weight=1) 
        tk.Grid.columnconfigure(self, (0,4), weight=1) 
        
        label = ttk.Label(self, text="Data Analysis", font=settings.LARGE_FONT)
        label.grid(column=2,row=0, sticky=tk.N)
        
        button_home = ttk.Button(self, text="Home", command=lambda: controller.show_frame(pages.HomePage.HomePage))
        button_home.grid(column=1,row=1)

        button_file_select = ttk.Button(self, text="Open File", command=lambda: lib.files.select_file(self,pages.DataAnalysis.DataAnalysis,parent,controller))
        button_file_select.grid(column=3, row=1)
        
        # static plot
        canvas = FigureCanvasTkAgg(lib.plotting.static_plot, self)
        canvas.get_tk_widget().grid(column=0, row=5, columnspan=5, rowspan=1, sticky="NSEW")
        canvas.draw()
        
        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(column=0, row=4, columnspan=5, sticky=tk.W)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()
        
        # Static table
        canvas2 = FigureCanvasTkAgg(lib.plotting.static_table, self)
        canvas2.get_tk_widget().grid(column=0, row=3, columnspan=5, rowspan=1, sticky="NSEW")
        canvas2.draw()
        
        toolbarFrame2 = tk.Frame(self)
        toolbarFrame2.grid(column=0, row=2, columnspan=5, sticky=tk.W)
        toolbar2 = NavigationToolbar2Tk(canvas2, toolbarFrame2)
        toolbar2.update()
