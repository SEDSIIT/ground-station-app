'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Configuration for the style, size, and elements of the GUI
will be configured here
'''

### Global Variables START ###

LARGE_FONT = ("Verdona", 12)

PATH = None
PATH_LIVEDATA = None # location of telemetry data
PATH_DATAFILE = None

PLATFORM = None

CURRENT_PAGE = "HomePage"
### Global Variables END ###


class DEBUG:
    status = True

class window:
    height = 1
    width = 1
    scale_height = 0.5
    scale_width = 0.5

class screen:
    height = 1
    width = 1
    