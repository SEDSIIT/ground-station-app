'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
# necessary libraries
import numpy as np
import os
import time

# initialize file name - ok if it rewrites the file every time for testing
FileName = 'TestData.csv'
cwd = os.getcwd()
FilePath = os.path.join(cwd, 'data', FileName)

# open file to begin writing process
f = open(FilePath, 'w')
f.write('Time,Altitude,Velocity,Events\r')

# Can change these
duration = 30 # test time
sampling_rate = 10 # Hz

start = time.time()
current = 0
while duration > current:
    f = open(FilePath, 'a')
    alt = np.random.randint(0,5000)
    vel = np.random.randint(0, 500)
    f.write(f"{current}, {alt}, {vel}\r")
    f.close()
    time.sleep(1/sampling_rate)
    current = time.time() - start
     
f.close()