import pandas as pd
from matplotlib import pyplot as plt

fdata = pd.read_csv("/home/michael/Desktop/School/SEDS/ground-station/gui/RRC3-LittleRedFlightData.csv")

#cleaning out NaN rows and noncontributig columns
rows = [x for x in range(4371, 4399)]
fdata.drop(['Events'], axis = 1)
fdata.drop(fdata.index[rows])

def flightStats(fdata):
    
    #Plotting Time vs. Altitude
    plt.plot(fdata['Time'], fdata['Altitude'])
    plt.title("Altitude vs. Time Graph")
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.grid()
    plt.show()

    #finding maxAlt and the time it occurs at
    maxAlt = max(fdata['Altitude'])
    timeA = fdata.loc[fdata.Altitude == maxAlt, 'Time'].values[0]
    print("The max altitude is: " + str(maxAlt) + " and the time it happens at is: " + str(timeA))

    #plotting Time vs. Velocity
    plt.plot(fdata['Time'], fdata['Velocity'])
    plt.title("Velocity vs. Time Graph")
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.grid()
    plt.show()

    #finding the max velocity and when it happens
    maxV = max(fdata['Velocity'])
    timeV = fdata.loc[fdata.Velocity == maxV, 'Time'].values[0]
    print("The max velocity reached is: " + str(maxV) + " and it is reached at time: " + str(timeV))


    #calculating the change in velocity over change in time (acceleration) between every neighboring data values
    slope = []
    for x in range(0, len(fdata['Velocity']) - 2):
        dV = fdata.iloc[x+1]['Velocity'] - fdata.iloc[x]['Velocity']
        dT = fdata.iloc[x+1]['Time'] - fdata.iloc[x]['Time']
        slope.append(dV/dT)
        
    #finding and displaying the max acceleration
    print("The max acceleration is: " + str(max(slope)))
    
flightStats(fdata)