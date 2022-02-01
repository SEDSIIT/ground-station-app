# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 13:58:53 2022

@author: user
"""
#necessary libraries
import numpy as np
import os
import time

#initialize file name - ok if it rewrites the file every time for testing
FileName = 'TestData.csv'
cwd = os.getcwd()
FilePath = os.path.join(cwd, 'data', FileName)

#open file to begin writing process
f = open(FilePath, 'w')
f.write('Time,Altitude,Velocity,Events\r')
#Can change these
duration = 30 #test time
sampling_rate = 10 #Hz

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