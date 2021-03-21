import settings

from datetime import datetime 
import time
import csv
import os

def local(delay):
    
    while True:
        try:
            timenow = datetime.now()
            yrnow = timenow.strftime("%Y")
            monow = timenow.strftime("%m")
            daynow = timenow.strftime("%d")
            path = "/home/pi/LabWatchGUI6/Logging/{}-{}.csv".format(yrnow,monow)
            file = open(path, "a")
            if os.stat(path).st_size == 0:
                file.write("Time,S1TempC,S1Humid,S2TempC,S2Humid,\n")

            file.write(str(timenow.strftime("%m/%d/%Y %H:%M"))+","+str(settings.sensor_data[0][0])+","+str(settings.sensor_data[0][1])+","+str(settings.sensor_data[1][0])+","+str(settings.sensor_data[1][1])+"\n")
            file.flush()
            file.close()
        except:
            print("Logging Failed")
        time.sleep(delay)




