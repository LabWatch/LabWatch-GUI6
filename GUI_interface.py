#!/usr/bin/python3

#thingspeak imports 
from urllib.request import urlopen 

#importing threading
import _thread

#import Time 
import time

#importing for the AdaFruit Board
import board
import adafruit_dht


#import for GUI 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import *           #Tkinter Library/ install Tkinter - Python 3. sudo apt-get install python3-tk
import tkinter as tk            #Tkinter Library
import threading                #For running mulitple threads(task,fucntion calls) 
import tkinter.font             #Tkinter font library
import random
import webbrowser
import csv
import os
from datetime import datetime 
import gaugelib


#----------------------------------------------------------
#-----------Sensor Global Variables------------------------

#setting up the pin for the DHT22
dhtDevice0 = adafruit_dht.DHT22(board.D4)
dhtDevice1 = adafruit_dht.DHT22(board.D18)


#global variables for the sensor on D4 pin 
sensor_fault0 = bool(0)
temp0 = 0 
humid0 = 0 

#global variables for the sensors 
sensor_fault1 = bool(0)
temp1 = 0
humid1 = 0 

#global for the dislplay and logging 
temp_last_avg=0
temp_avg = 0
humid_last_avg = 0
humid_avg = 0

#-----------------------------------------------------------------
#----------------ThingSpeak Global Variables----------------------
#ThingSpeak credentrials 
myAPI = '4M4MSZ8ZYP18AU3E' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

#-------------------------------------------------------------------
#-------------------Tkinter Variables-----------------------------------------
#Tkinter window
win = tk.Tk()

#Live update plot of temp and humidity

#Parameters
x_len = 200         # Number of points to display
y_range = [10, 40]  # Range of possible Y values to display

#Create figure for plotting
fig = plt.figure()
fig.patch.set_facecolor('#DcDcDc')
fig.set_size_inches(8, 2)
ax = fig.add_subplot(1,2,1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

#Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

#Add labels
plt.title('Temperature over Time')
plt.xlabel('Samples')
plt.ylabel('Temp °C')
plt.grid(True)

ax2 = fig.add_subplot(1,2,2)
xs2 = list(range(0, 200))
ys2 = [0] * x_len
ax2.set_ylim(y_range)

#Create a blank line. We will update the line in animate
line2, = ax2.plot(xs2, ys2)
#Add labels
#plt.xticks(rotation=45)
plt.title('Humidity over Time')
plt.xlabel('Samples')
plt.ylabel('%')
plt.grid(True)
fig.tight_layout()



#______________________________________________________________________________________________________________________________
#------------------Everything Between lines for Sensor read Data and error checking--------------------------------------------- 


# DHT22 Sensor on Pin D4 
def sensor0( threadName, delay):
    global temp0
    global humid0
    global sensor_fault0
    global temp_avg
    fault = bool(0)
    while True:
        for x in range(5):
            try:
                # Print the values to the serial port
                temperature_c = dhtDevice0.temperature
                humidity = dhtDevice0.humidity
                if (abs(temp_avg - temperature_c ) < 4):
                    fault = bool(0)
                break            
            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                time.sleep(delay)
                
            except Exception as error:
                dhtDevice0.exit()
                raise error
            if (x > 3):
                fault = bool(1)
                temperature_c = 0
                humidity = 0 
                break

        temp0 = temperature_c
        humid0 = humidity
        sensor_fault0 = fault
        time.sleep(delay)


# DHT22 Sensor on Pin D18  
def sensor1( threadName, delay):
    global temp1
    global humid1
    global sensor_fault1
    global temp_avg
    fault = bool(0)
    while True: #runs forever 
        for x in range(5):#tries 5 times before thorwing fault for sensor 
            try:
                # Print the values to the serial port
                temperature_c = dhtDevice1.temperature
                humidity = dhtDevice1.humidity
                if (abs(temp_avg - temperature_c ) < 4): # if the sensor is within a certain range it will be used again 
                    fault = bool(0)
                break            
            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                time.sleep(delay)
                
            except Exception as error:
                dhtDevice1.exit()
                raise error
            if (x > 3):
                fault = bool(1)
                temperature_c = 0
                humidity = 0 
                break
        #stores to global variables once it has gotten a proper value otherwise if faulty sets to 0, 0 
        temp1 = temperature_c
        humid1 = humidity
        sensor_fault1 = fault
        time.sleep(delay)        


# to calculate the avg and error check between two sensors 
def avg(threadName, delay):
    global temp_avg #uses all global variables which are also used for uploading and display
    global humid_avg
    global temp_last_avg
    global humid_last_avg
    global temp0
    global humid0
    global temp1
    global humid1
    global sensor_fault0
    global sensor_fault1
    
    while True: #runs the avg loop forever 
        
        temp_last_avg = temp_avg #stores current avgerage as last avg 
        humid_last_avg = humid_avg

        # mutltiple statments checking different sinarios for faulty sensor 
        if (sensor_fault0 == False and sensor_fault1 == False) :#both good
            tempdiff = abs(temp0-temp1)
            humiddiff = abs(humid0-humid1)

            if (tempdiff < 4 and humiddiff < 10) :# they are roughly the same value 
                temp_avg = (temp0 + temp1) / 2
                humid_avg = (humid0 + humid1) / 2

        elif (sensor_fault0 == False and sensor_fault1 == True) :#D4 OK D18 Bad
            temp_avg = (temp0 + temp_last_avg) / 2
            humid_avg = (humid0 + humid_last_avg) / 2

        elif (sensor_fault0 == True and sensor_fault1 == False): #D4 Bad D18 OK
            temp_avg = (temp1 + temp_last_avg) / 2
            humid_avg = (humid1 + humid_last_avg) / 2 
        else: #both Bad set to 0 , 0 
            temp_avg = 0
            humid_avg = 0

        
        # # prints to terminal for error checking 
        # print(
        #         "Temp_avg:  {:.1f} C    Humidity_avg: {:.1f}%   sensor0: {}   Sensor1: {} ".format(
        #             temp_avg, humid_avg,sensor_fault0,sensor_fault1
        #         )
        #     ) 
        time.sleep(delay)#sleeps for set delay time 




# 
#-----------------------------------End of sensor Data read and error Check------------------------------------------------------------------------
#________________________________________________________________________________________________________________________________________________

#________________________________________________________________________________________________________________________________

#---------------------------------------------Thingspeak Function Validation-------------------------------------------------
def cloud(threadName, delay):
    global temp_avg
    global humid_avg
    global baseURL
    while True:

        try:
            conn = urlopen(baseURL + '&field1=%s&field2=%s' % (temp_avg, humid_avg))
            conn.close()
        except:
            print("Connection Failed")
        time.sleep(delay)


#-------------------------------------End of Thingspeak Uploading ---------------------------------------------------------------------------
#____________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________________
#-----------------------------------GUI to local User Code-----------------------------------------------------------------------


def animate(i, xs, xs2, ys, ys2):
    global temp_avg
    global humid_avg
    global line
    global line2
    global x_len
    p1.set_value(float(temp_avg))
    p2.set_value(float(humid_avg))
    # Add y to list
    ys.append(temp_avg)
    ys2.append(humid_avg)

    # Limit y list to set number of items
    ys = ys[-x_len:]
    ys2 = ys2[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)
    line2.set_ydata(ys2) 

    if temp_avg<10.0:
        win.configure(background='#FF0000')
    else:
        win.configure(background='#DcDcDc')
        


p1 = gaugelib.DrawGauge2(
    win,
    max_value=70.0,
    min_value=-30.0,
    size=250,
    bg_col='#DCDCDC',
    unit = "Temp. °C",bg_sel = 2)
p2 = gaugelib.DrawGauge3(
    win,
    max_value=80.0,
    min_value=20.0,
    size=250,
    bg_col='#DCDCDC',
    unit = "Humidity %",bg_sel = 2)

p1.pack()
p1.place(x=100, y=50)
p2.pack()
p2.place(x=500, y=50)

#--------------------Buttons---------------------------------
# def reportSummary():

#     file = open("/home/pi/data_log.csv", "a")


# button = Label(win, text="ReportSummary", fg="blue", cursor="hand2",font=('times',12, 'bold' ))
# button.bind("<Button-1>",lambda e: reportSummary('/home/pi/data_log.csv'))
# button.pack()
# button.place(x=90, y=0)

# def thingSpeak(url):
#     webbrowser.open_new(url)

# button = Label(win, text="ThingSpeak", fg="blue", cursor="hand2",font=('times',12, 'bold' ))
# button.bind("<Button-1>",lambda e: thingSpeak("https://thingspeak.com/channels/1318645"))
# button.pack()
# button.place(x=0, y=0)
#----------------------------End of buttons--------------------------------------

#---------------------------Clock ----------------------------------------------------------------
class Clock:
    def __init__(self):
        self.time1 = ''
        self.time2 = time.strftime('%d-%m-%y %H:%M:%S:%p:%Z')

        self.mFrame = Frame()
        self.mFrame.pack(expand=YES,fill=X)
        self.mFrame.place(x=560, y=0)
        self.watch = Label(self.mFrame, text=self.time2, font=('times',14, 'bold' ),background='#DcDcDc', fg="black")

        self.watch.pack()
        
        self.changeLabel() #first call it manually

    def changeLabel(self): 
        self.time2 = time.strftime('%Y-%m-%d %H:%M:%S:%p:%Z')
        self.watch.configure(text=self.time2)
        self.mFrame.after(200, self.changeLabel) #it'll call itself continuously


#-------------------------------End clock--------------------------------- 

canv = FigureCanvasTkAgg(fig, master = win)
canv._tkcanvas.pack(side=tk.BOTTOM)
canv.draw()
get_widz = canv.get_tk_widget()
get_widz.pack()

win.attributes("-fullscreen",True)             #Fullscreen when executed 
win.bind("<Escape>",exit)                      #ESC to exit

def exit():                                    #Exit fullscreen
	win.quit() 

#Call animate() function in interval of 1 second


#Warnings background color change



Clock()


#---------------------------------End Of GUI -------------------------------------------------------------------------------
#____________________________________________________________________________________________________________________


#__________________________________________________________________________________________________________________
#-------------------------------Creating Threads--------------------------------------------------------------------
# Create two threads as follows
try:
    print("test")
    _thread.start_new_thread( sensor0, ("sensor_1", 2, ) )#starts recording sensor on D4
    _thread.start_new_thread( sensor1, ("sensor_2", 2, ) )#starts recording sensor on D18
    _thread.start_new_thread( avg,     ("average" , 4, ) )
    _thread.start_new_thread( cloud,   ("upload"  , 10, ) )
    ani = animation.FuncAnimation(fig, animate, interval=1000, fargs=(xs, ys,xs2,ys2) )
except:
    print ("Error: unable to start thread")

#-----------------------------End of Starting Threads----------------------------------------------------
#_________________________________________________________________________________________________________




win.mainloop()


#______________________________________________________________________________________________
#-------------------main loop for the programe------------------------------------------------- 

while 1:#True loop to run code forever 
    
    #keeps threads running in background           
    pass 
    
#-------------------------End of Main Loop-----------------------------------------------------
#_______________________________________________________________________________________________


#end of code 
