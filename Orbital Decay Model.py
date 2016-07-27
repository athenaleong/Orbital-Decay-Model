"""
Orbital Decay Model
@author: Athena Leong
"""

from math import exp 
import time
import openpyxl
import os
import numpy as np
import matplotlib.pyplot as plt


#density model
#--------------------------------------------------------------------------------
os.chdir("directory") #<--- replace with corresponding directory 
wb = openpyxl.load_workbook("densitymodel.xlsx")
sheet = wb.get_sheet_by_name("Sheet1")
densityData= {}
densitykey= []
for row in range(1,sheet.max_row + 1):
    a = sheet["A" + str(row)].value
    b = sheet["B" + str(row)].value
    densityData[a] = b
    densitykey.append(a)
    

#function
#-------------------------------------------------------------------------------
def calDensity(orbit):
    for i in range(0,len(densitykey)):
        if densitykey[i] < orbit:
            continue 
        else:
           frontDensity = densityData.get(densitykey[i-1])
           endDensity = densityData.get(densitykey[i])
           interval = int(densitykey[i]) - int(densitykey[i-1])
           density =(((orbit - densitykey[i-1])/interval) * (endDensity - frontDensity)) + frontDensity
           break
    return density
          
#variables
#-------------------------------------------------------------------------------        
t = 0
velocity = 0
totalEnergy = 0
kmorbit = 0
density = 0
fD = 0
distance = 0
workdone = 0
radius = 0
earthRadius =  6371000
gvConstant = 6.67 * (10**-11)
e = 2.7128
m1 = 5.972 *(10**24)
name = input("Name of Satellite:")
m2 = float(input("Mass Of Satellite/kg:"))
dragCoefficient = float(input("drag coefficient of satellite:"))
surfaceArea = float(input ("surface area of satellite:"))
orbit = int(input ("original orbit /m")) 
minimum = 200000
instantTime = 3600
radius = orbit + earthRadius 
T = 2*3.142*(radius**3/(gvConstant*m1))**(1/2)
velocity = ((gvConstant*m1)/radius)**0.5
totalEnergy = -0.5*(gvConstant*m1*m2)/radius
kmorbit = float(orbit/1000)
density = calDensity(orbit) 
orbitList= [orbit]
timeList = [t]


#--------------------------------------------------------------------------------

while orbit >= minimum:
    
    fD = 0.5*density*(velocity**2)*dragCoefficient*surfaceArea
    distance = (instantTime/T)*3.14*radius
    workdone = fD*distance 
    totalEnergy = totalEnergy - workdone 
    radius = ((-0.5)*gvConstant*m1*m2/totalEnergy)
    velocity =((gvConstant*m1)/radius)**0.5 
    orbit = radius - earthRadius 
    t += instantTime
    orbitList.append(orbit/1000)
    timeList.append(t/31536000)
    if orbit >= minimum:
        density = calDensity(orbit) 
    else:
        break
years = float(t/31536000)
print ("years taken: %s" % (years))

#plot
#------------------------------------------------------------------------------
plt.plot(timeList, orbitList, color = "blue", lw = 2)
plt.plot([0,years],[200,200],color = "red", linestyle = "--", lw =2)
plt.title("Orbital Decay Simulation of " + name, fontsize=20)
plt.title("lifetime: %s" % (years), fontsize = 10, loc = "right")
plt.xlabel("time/years", fontsize =18)
plt.ylabel("orbit/km", fontsize = 18)
plt.axis([0,years,150,kmorbit])
ax = plt.axes()        
ax.yaxis.grid(True)
ax.xaxis.grid(True) 

plt.show()



