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
