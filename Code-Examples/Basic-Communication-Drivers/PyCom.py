'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import serial
from serial import Serial

ser = Serial('COM3', 115200)
if not ser.isOpen():
    ser.open()
print('COM4 is open', ser.isOpen())


while True:
    action = input("r=read,  w=write,  q=quit: ")

    if(action == 'r'):
        print("r")
        for i in range(10):
            data = ser.readline(1000)
            print(data)
    elif(action == 'w'):
        print("w")
        send = "Send Data not "
        for i in range(10):
            ser.write( send.encode())
            data = ser.readline(1000)
            print(data)
    elif(action == 'q'):
        print("q, byebye!")
        exit()
