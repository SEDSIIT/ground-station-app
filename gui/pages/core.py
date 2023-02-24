'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

ABOUT:
This defines the main window of the GUI. This acts as the tree trunk where
the individual pages act as branches.
'''

import tkinter as tk
import lib.app_settings as settings
import lib.files
import pages.HomePage
import pages.DataAnalysis
import pages.FCSettings
import pages.Settings
import pages.Telemetry

class GSApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
                
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        
        # File Menu 
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Save Settings", command = lambda: tk.messagebox.showinfo("Information","Not supported yet!"))
        fileMenu.add_command(label="Open", command = lambda: lib.files.select_file(self,pages.DataAnalysis.DataAnalysis,container,self))
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command = lambda: quit()) # Fixed?
        menubar.add_cascade(label="File", menu=fileMenu)

        # Page Menu
        pageMenu = tk.Menu(menubar, tearoff=0)
        pageMenu.add_command(label="Home", command = lambda: self.show_frame(pages.HomePage.HomePage))
        pageMenu.add_separator()
        pageMenu.add_command(label="Data Analysis", command = lambda: self.show_frame(pages.DataAnalysis.DataAnalysis))
        pageMenu.add_command(label="FC Settings", command = lambda: self.show_frame(pages.FCSettings.FCSettings))
        pageMenu.add_command(label="Live Flight Data", command = lambda: self.show_frame(pages.Telemetry.Telemetry))
        menubar.add_cascade(label="Page", menu=pageMenu)

        # Settings Menu
        settingsMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settingsMenu)

        # Help Menu
        helpMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpMenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        # Load all pages initially
        for page in (pages.HomePage.HomePage, pages.DataAnalysis.DataAnalysis, pages.FCSettings.FCSettings, pages.Telemetry.Telemetry, pages.Settings.Settings):

            frame = page(container, self)

            self.frames[page] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(pages.HomePage.HomePage)

    # Show frame that is requested
    def show_frame(self, cont):
        global CURRENT_PAGE
        if (cont.__name__ == 'DataAnalysis'):
            CURRENT_PAGE = "DataAnalysis"
        elif (cont.__name__ == 'FCSettings'):
            CURRENT_PAGE = "FCSettings"
        elif (cont.__name__ == 'Telemetry'):
            CURRENT_PAGE = "Telemetry"
        elif (cont.__name__ == 'Settings'):
            CURRENT_PAGE = "Settings"
        else:
            CURRENT_PAGE = "HomePage" 
        if (settings.DEBUG.status == True):
            print("CURRENT_PAGE: %s" %(CURRENT_PAGE))
        frame = self.frames[cont]
        frame.tkraise()
