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

    # Dummy DATA (generated with GPT 4 btw) --------------------------------------------------------
    
    # Time points
    time_points = 30
    t = np.linspace(0, 1, time_points)

    # Simulate altitude: A parabolic curve peaking at half time, representing ascent and descent
    peak_altitude = 500  # Assuming the apogee is 500 meters
    altitude = -4 * peak_altitude * (t - 0.5)**2 + peak_altitude


    # Speed: First derivative of altitude
    speed = np.gradient(altitude, t)

    # Acceleration: Second derivative of altitude
    acceleration = np.gradient(speed, t)

    # Simulate latitude and longitude drift: Assuming launch site is at 0, 0
    initial_latitude = 40.7128  # example latitude
    initial_longitude = -74.0060  # example longitude
    latitude = initial_latitude + 0.0001 * np.cumsum(np.random.normal(0, 1, time_points))  # small random walk
    longitude = initial_longitude + 0.0001 * np.cumsum(np.random.normal(0, 1, time_points))  # small random walk

    time = np.linspace(0, 300, time_points)
    # ----------------------------------------------------------------------------------------------

    util_frame = ttk.Frame(frame)
    start_cap_btn = ttk.Button(util_frame, text="Start Capture")
    stop_cap_btn = ttk.Button(util_frame, text="Stop Capture")
    save_btn = ttk.Button(util_frame, text="Save")
    load_btn = ttk.Button(util_frame, text="Load")
    
    # big canvases
    # the idea is, when you click on one of the mini canvas, it shows it in greater detail and size
    BIG_current_fig = None
    BIG_current_ax = None
    BIG_current_line = None
    BIG_current_canvas = None
    BIG_current_widget = None


    BIG_altitude_fig = Figure(figsize=(10, 8), dpi=100, layout="constrained")
    BIG_altitude_ax = BIG_altitude_fig.add_subplot()
    BIG_altitude_ax.set_title("Altitude Time Graph")
    BIG_altitude_ax.set_xlabel("Time (s)")
    BIG_altitude_ax.set_ylabel("Altitude (m)")
    BIG_altitude_line = BIG_altitude_ax.plot(time, altitude)
    BIG_altitude_canvas = FigureCanvasTkAgg(BIG_altitude_fig, master=frame)  # A tk.DrawingArea.
    BIG_altitude_widget = BIG_altitude_canvas.get_tk_widget()
    BIG_altitude_canvas.draw()

    BIG_speed_fig = Figure(figsize=(10, 8), dpi=100, layout="constrained")
    BIG_speed_ax = BIG_speed_fig.add_subplot()
    BIG_speed_ax.set_title("Speed Time Graph")
    BIG_speed_ax.set_xlabel("Time (s)")
    BIG_speed_ax.set_ylabel("speed (m)")
    BIG_speed_line = BIG_speed_ax.plot(time, speed)
    BIG_speed_canvas = FigureCanvasTkAgg(BIG_speed_fig, master=frame)  # A tk.DrawingArea.
    BIG_speed_widget = BIG_speed_canvas.get_tk_widget()
    BIG_speed_canvas.draw()

    BIG_acceleration_fig = Figure(figsize=(10, 8), dpi=100, layout="constrained")
    BIG_acceleration_ax = BIG_acceleration_fig.add_subplot()
    BIG_acceleration_ax.set_title("Acceleration Time Graph")
    BIG_acceleration_ax.set_xlabel("Time (s)")
    BIG_acceleration_ax.set_ylabel("acceleration (m)")
    BIG_acceleration_line = BIG_acceleration_ax.plot(time, acceleration)
    BIG_acceleration_canvas = FigureCanvasTkAgg(BIG_acceleration_fig, master=frame)  # A tk.DrawingArea.
    BIG_acceleration_widget = BIG_acceleration_canvas.get_tk_widget()
    BIG_acceleration_canvas.draw()

    BIG_latitude_fig = Figure(figsize=(10, 8), dpi=100, layout="constrained")
    BIG_latitude_ax = BIG_latitude_fig.add_subplot()
    BIG_latitude_ax.set_title("Latitude Time Graph")
    BIG_latitude_ax.set_xlabel("Time (s)")
    BIG_latitude_ax.set_ylabel("latitude (?)")
    BIG_latitude_line = BIG_latitude_ax.plot(time, latitude)
    BIG_latitude_canvas = FigureCanvasTkAgg(BIG_latitude_fig, master=frame)  # A tk.DrawingArea.
    BIG_latitude_widget = BIG_latitude_canvas.get_tk_widget()
    BIG_latitude_canvas.draw()

    BIG_longitude_fig = Figure(figsize=(10, 8), dpi=100, layout="constrained")
    BIG_longitude_ax = BIG_longitude_fig.add_subplot()
    BIG_longitude_ax.set_title("Longitude Time Graph")
    BIG_longitude_ax.set_xlabel("Time (s)")
    BIG_longitude_ax.set_ylabel("longitude (?)")
    BIG_longitude_line = BIG_longitude_ax.plot(time, longitude)
    BIG_longitude_canvas = FigureCanvasTkAgg(BIG_longitude_fig, master=frame)  # A tk.DrawingArea.
    BIG_longitude_widget = BIG_longitude_canvas.get_tk_widget()
    BIG_longitude_canvas.draw()

    

    # mini canvases

    # will be placed in their own frame
    multi_canvas_frame = ttk.Frame(frame)

    

    # probably some refactoring can happen here, instead of manually coding this, we can create a function 
    # optimizations and refactoring come later though

    def mini_canva_callback(fig, ax, line, canvas, widget):
        print("fired")
        print(ax.title)
        nonlocal BIG_current_fig 
        nonlocal BIG_current_ax 
        nonlocal BIG_current_line 
        nonlocal BIG_current_canvas 
        nonlocal BIG_current_widget 
        
        BIG_current_fig = fig
        BIG_current_ax = ax
        BIG_current_line = line
        BIG_current_canvas = canvas

        if(BIG_current_widget != None):
            BIG_current_widget.grid_remove()
        BIG_current_widget = widget

        widget.grid(column = 1, row = 1)

        return
    
    altitude_fig = Figure(figsize=(2, 1.6), dpi=100, layout="constrained")
    altitude_ax = altitude_fig.add_subplot()
    altitude_ax.set_yticklabels([])
    altitude_ax.set_xticklabels([])
    altitude_ax.set_yticks([])
    altitude_ax.set_xticks([])
    altitude_line = altitude_ax.plot(time, altitude)
    altitude_canvas = FigureCanvasTkAgg(altitude_fig, master=multi_canvas_frame)  # A tk.DrawingArea.
    altitude_widget = altitude_canvas.get_tk_widget()
    altitude_canvas.draw()
    altitude_widget.bind("<Button-1>", lambda e: mini_canva_callback(BIG_altitude_fig, BIG_altitude_ax, BIG_altitude_line, BIG_altitude_canvas, BIG_altitude_widget))

    speed_fig = Figure(figsize=(2, 1.6), dpi=100, layout="constrained")
    speed_ax = speed_fig.add_subplot()
    speed_ax.set_yticklabels([])
    speed_ax.set_xticklabels([])
    speed_ax.set_yticks([])
    speed_ax.set_xticks([])
    speed_line = speed_ax.plot(time, speed)
    speed_canvas = FigureCanvasTkAgg(speed_fig, master=multi_canvas_frame)  # A tk.DrawingArea.
    speed_widget = speed_canvas.get_tk_widget()
    speed_canvas.draw()
    speed_widget.bind("<Button-1>", lambda e: mini_canva_callback(BIG_speed_fig, BIG_speed_ax, BIG_speed_line, BIG_speed_canvas, BIG_speed_widget))

    acceleration_fig = Figure(figsize=(2, 1.6), dpi=100, layout="constrained")
    acceleration_ax = acceleration_fig.add_subplot()
    acceleration_ax.set_yticklabels([])
    acceleration_ax.set_xticklabels([])
    acceleration_ax.set_yticks([])
    acceleration_ax.set_xticks([])
    acceleration_line = acceleration_ax.plot(time, acceleration)
    acceleration_canvas = FigureCanvasTkAgg(acceleration_fig, master=multi_canvas_frame)  # A tk.DrawingArea.
    acceleration_widget = acceleration_canvas.get_tk_widget()
    acceleration_canvas.draw()
    acceleration_widget.bind("<Button-1>", lambda e: mini_canva_callback(BIG_acceleration_fig, BIG_acceleration_ax, BIG_acceleration_line, BIG_acceleration_canvas, BIG_acceleration_widget))

    latitude_fig = Figure(figsize=(2, 1.6), dpi=100, layout="constrained")
    latitude_ax = latitude_fig.add_subplot()
    latitude_ax.set_yticklabels([])
    latitude_ax.set_xticklabels([])
    latitude_ax.set_yticks([])
    latitude_ax.set_xticks([])
    latitude_line = latitude_ax.plot(time, latitude)
    latitude_canvas = FigureCanvasTkAgg(latitude_fig, master=multi_canvas_frame)  # A tk.DrawingArea.
    latitude_widget = latitude_canvas.get_tk_widget()
    latitude_canvas.draw()
    latitude_widget.bind("<Button-1>", lambda e: mini_canva_callback(BIG_latitude_fig, BIG_latitude_ax, BIG_latitude_line, BIG_latitude_canvas, BIG_latitude_widget))

    longitude_fig = Figure(figsize=(2, 1.6), dpi=100, layout="constrained")
    longitude_ax = longitude_fig.add_subplot()
    longitude_ax.set_yticklabels([])
    longitude_ax.set_xticklabels([])
    longitude_ax.set_yticks([])
    longitude_ax.set_xticks([])
    longitude_line = longitude_ax.plot(time, longitude)
    longitude_canvas = FigureCanvasTkAgg(longitude_fig, master=multi_canvas_frame)  # A tk.DrawingArea.
    longitude_widget = longitude_canvas.get_tk_widget()
    longitude_canvas.draw()
    longitude_widget.bind("<Button-1>", lambda e: mini_canva_callback(BIG_longitude_fig, BIG_longitude_ax, BIG_longitude_line, BIG_longitude_canvas, BIG_longitude_widget))
    
    # respective headers for each mini canvas
    altitude_frame = ttk.Frame(multi_canvas_frame)
    altitude_header_lb = ttk.Label(altitude_frame, text="Altitude")
    altitude_current_lb = ttk.Label(altitude_frame, text="-")
    altitude_max_lb = ttk.Label(altitude_frame, text="-")

    speed_frame = ttk.Frame(multi_canvas_frame)
    speed_header_lb = ttk.Label(speed_frame, text="Speed")
    speed_current_lb = ttk.Label(speed_frame, text="-")
    speed_max_lb = ttk.Label(speed_frame, text="-")

    acceleration_frame = ttk.Frame(multi_canvas_frame)
    acceleration_header_lb = ttk.Label(acceleration_frame, text="Acceleration")
    acceleration_current_lb = ttk.Label(acceleration_frame, text="-")
    acceleration_max_lb = ttk.Label(acceleration_frame, text="-")

    latitude_frame = ttk.Frame(multi_canvas_frame)
    latitude_header_lb = ttk.Label(latitude_frame, text="Latitude")
    latitude_current_lb = ttk.Label(latitude_frame, text="-")
    latitude_max_lb = ttk.Label(latitude_frame, text="-")

    longitude_frame = ttk.Frame(multi_canvas_frame)
    longitude_header_lb = ttk.Label(longitude_frame, text="Longitude")
    longitude_current_lb = ttk.Label(longitude_frame, text="-")
    longitude_max_lb = ttk.Label(longitude_frame, text="-")

    # Buttons
    util_frame.grid(column=0, row=0)
    start_cap_btn.grid(column=0, row=0)
    stop_cap_btn.grid(column=1, row=0)
    save_btn.grid(column=2,row=0)
    load_btn.grid(column=3,row=0)
    

    # large canvas
    multi_canvas_frame.grid(column=0, row=1)

    # Gridding/Configuring done here
    altitude_widget    .grid(column=0, row=0)
    altitude_frame     .grid(column=1, row=0)
    altitude_header_lb .grid(column=0, row=0)
    altitude_current_lb.grid(column=0, row=1)
    altitude_max_lb    .grid(column=0, row=2)

    speed_widget       .grid(column=0, row=1)
    speed_frame        .grid(column=1, row=1)
    speed_header_lb    .grid(column=0, row=0)
    speed_current_lb   .grid(column=0, row=1)
    speed_max_lb       .grid(column=0, row=2)

    acceleration_widget    .grid(column=0, row=2)
    acceleration_frame     .grid(column=1, row=2)
    acceleration_header_lb .grid(column=0, row=0)
    acceleration_current_lb.grid(column=0, row=1)
    acceleration_max_lb    .grid(column=0, row=2)

    latitude_widget    .grid(column=0, row=3)
    latitude_frame     .grid(column=1, row=3)
    latitude_header_lb .grid(column=0, row=0)
    latitude_current_lb.grid(column=0, row=1)
    latitude_max_lb    .grid(column=0, row=2)

    longitude_widget    .grid(column=0, row=4)
    longitude_frame     .grid(column=1, row=4)
    longitude_header_lb .grid(column=0, row=0)
    longitude_current_lb.grid(column=0, row=1)
    longitude_max_lb    .grid(column=0, row=2)

    # Finally before returning, going to by default select altitude
    mini_canva_callback(BIG_altitude_fig, 
                        BIG_altitude_ax, 
                        BIG_altitude_line, 
                        BIG_altitude_canvas, 
                        BIG_altitude_widget)
    
    return frame



    






