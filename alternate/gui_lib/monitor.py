from tkinter import *
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def monitor(parent, gsa_obj):
    frame = ttk.Frame(parent)


    # according to the TEST_FLIGHT.csv, these are the supported attributes we will be tracking
    # Altitude, Velocity (more accurately speed), Acceleration, Latitude, Longitude, 'Events', 
    # all wrt to time
    # of course more can be added easily

    # initially gridding all the axes in one figure seems better
    # however, we need to have them as seperate figures so that we can easily
    # track if an element is clicked on (otherwise we would have to deal with mouse position details...)
    # also makes it easier to position (although one could've have used mosaic)
    # please see the matplotlib user guide to see how this works, in particular,
    # the embedded example at  https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html


    # mini canvases
    # will be placed in their own frame
    multi_canvas_frame = ttk.Frame(frame)

    t = np.arange(0, 3, .01)

    altitude_fig = Figure(figsize=(5, 4), dpi=100)
    altitude_ax = altitude_fig.add_subplot()
    altitude_line = altitude_ax.plot(t, 2 * np.sin(2 * np.pi * t))
    altitude_canvas = FigureCanvasTkAgg(altitude_fig, master=multi_canvas_frame)  # A tk.DrawingArea.
    altitude_widget = altitude_canvas.get_tk_widget()
    altitude_canvas.draw()

    altitude_fig = Figure(figsize=(5, 4), dpi=100)
    altitude_ax = altitude_fig.add_subplot()
    altitude_line = altitude_ax.plot(t, 2 * np.sin(2 * np.pi * t))
    altitude_canvas = FigureCanvasTkAgg(altitude_fig, master=multi_canvas_frame)  # A tk.DrawingArea.
    altitude_canvas.draw()

    altitude_fig = Figure(figsize=(5, 4), dpi=100)
    altitude_ax = altitude_fig.add_subplot()
    altitude_line = altitude_ax.plot(t, 2 * np.sin(2 * np.pi * t))
    altitude_canvas = FigureCanvasTkAgg(altitude_fig, master=multi_canvas_frame)  # A tk.DrawingArea.
    altitude_canvas.draw()

    altitude_fig = Figure(figsize=(5, 4), dpi=100)
    altitude_ax = altitude_fig.add_subplot()
    altitude_line = altitude_ax.plot(t, 2 * np.sin(2 * np.pi * t))
    altitude_canvas = FigureCanvasTkAgg(altitude_fig, master=multi_canvas_frame)  # A tk.DrawingArea.
    altitude_canvas.draw()

    altitude_fig = Figure(figsize=(5, 4), dpi=100)
    altitude_ax = altitude_fig.add_subplot()
    altitude_line = altitude_ax.plot(t, 2 * np.sin(2 * np.pi * t))
    altitude_canvas = FigureCanvasTkAgg(altitude_fig, master=multi_canvas_frame)  # A tk.DrawingArea.
    altitude_canvas.draw()
    


    # large canvas
    

    # Gridding/Configuring done here
    altitude_widget.grid(column=0, row=0)
    
    return frame