#!/usr/bin/python3

#-----------Import Libraries------------------------#

#thingspeak imports 
from urllib.request import urlopen 

#importing threading
import _thread

#import Time 
import time
import datetime as dt
from datetime import datetime 

#importing data for the AdaFruit GPIO Board (RPI4)
import board
import adafruit_dht

#System Restart 
import subprocess

#import libraries for GUI 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from tkinter import *           #Tkinter Library/ install Tkinter - Python 3. sudo apt-get install python3-tk
import tkinter as tk            #Tkinter Library
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font             #Tkinter font library

import threading                #For running mulitple threads(task,fucntion calls) 
import random
import webbrowser
import csv
import os


#-----------End of Import Libraries------------------------#

#-----------Sensor Global Variables------------------------#

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
#-------------------Tkinter Variables + Plot attributes-----------------------------------------
#Tkinter window
win = tk.Tk()

#Live update plot of temp and humidity

#Create figure for plotting
fig = plt.figure()
fig.patch.set_facecolor('black')
fig.set_size_inches(8, 2)

ax = fig.add_subplot(1,2,1)
xs = []
ys = [] 

ax2 = fig.add_subplot(1,2,2)
xs2 = []
ys2 = [] 

#upper lower bounds for ranges 
TUpper_green = 22 #for temp ranges 
TLower_green = 19

TUpper_yellow = 25 
TLower_yellow = 17

HUpper_green = 42 #for humid ranges 
HLower_green = 36

HUpper_yellow = 46 
HLower_yellow = 32

temp_colour = "#000000"
humid_colour = "#000000"

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
                if (abs(temp0 - temperature_c ) < 4):
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
                if (abs(temp1 - temperature_c ) < 4): # if the sensor is within a certain range it will be used again 
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
                temp_avg = (temp0 + temp1 + temp_last_avg) / 3
                humid_avg = (humid0 + humid1 + humid_last_avg) / 3

        elif (sensor_fault0 == False and sensor_fault1 == True) :#D4 OK D18 Bad
            temp_avg = (temp0 + temp_last_avg) / 2
            humid_avg = (humid0 + humid_last_avg) / 2
            messagebox.showerror("SENSOR ERROR", "SENSOR 2 FAULT ON D18")
            
        elif (sensor_fault0 == True and sensor_fault1 == False): #D4 Bad D18 OK
            temp_avg = (temp1 + temp_last_avg) / 2
            humid_avg = (humid1 + humid_last_avg) / 2 
            messagebox.showerror("SENSOR ERROR", "SENSOR 1 FAULT ON D4")
            
        else: #both Bad set to 0 , 0 
            temp_avg = 0
            humid_avg = 0
            messagebox.showerror("SENSOR ERROR", "SENSOR 1 AND 2 FAULT")

        temp_avg = round(temp_avg,1)
        humid_avg = round(humid_avg,1)
        # # prints to terminal for error checking 
        # print(
        #         "Temp_avg:  {:.1f} C    Humidity_avg: {:.1f}%   sensor0: {}   Sensor1: {} ".format(
        #             temp_avg, humid_avg,sensor_fault0,sensor_fault1
        #         )
        #     ) 
        time.sleep(delay)#sleeps for set delay time 

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
#________________________________________________________________________________________________________________________________

#-------------------------------------Local Logging-------------------------------------------------

def local(threadName, delay):
    global temp0
    global humid0
    global temp1
    global humid1
    
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

            file.write(str(timenow.strftime("%m/%d/%Y %H:%M:%S"))+","+str(temp0)+","+str(humid0)+","+str(temp1)+","+str(humid1)+"\n")
            file.flush()
            file.close()
        except:
            print("Logging Failed")
        time.sleep(delay)



#-------------------------------------End of Local Logging ---------------------------------------------------------------------------
#____________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________
#-----------------------------------GUI to local User Code-----------------------------------------------------------------------


#Digital readings for GUI
temperature = StringVar()                       #is a class that provides helper functions for directly creating and accessing such variables in that interpreter.
temperature.set("----"+ "°C")	                #Temperature set to store multiple items in a single variable	

humidity = StringVar()
humidity.set("----"+" %")		                #Humidity set to store multiple items in a single variable	

temperatureLabel = Label(win, fg=temp_colour, background="black", textvariable=temperature, font=("Segoe UI", 60,"bold")) #bg color,font and font size
temperatureLabel.place(x=70, y=110)             #Character "----C" placement and attributes

humidityLabel = Label(win, fg=humid_colour, background="black", textvariable=humidity, font=("Segoe UI", 60,"bold"))       #bg color,font and font size
humidityLabel.place(x=485, y=110)              #Character "----%" placement and attributes
#End of Digital readings for GUI

def animate(i, xs, xs2, ys, ys2):
    global temp_avg
    global humid_avg
    global TUpper_green  #for temp ranges 
    global TLower_green 

    global TUpper_yellow  
    global TLower_yellow 

    global HUpper_green  #for humid ranges 
    global HLower_green 

    global HUpper_yellow  
    global HLower_yellow 
    
    #Send variables from temp to StringVar for temperatur.set above in---->Digital readings for GUI
    temperature.set(str(round(temp_avg,1))+"°C")            
    #Send variables from hum to StringVar for temperatur.set above in---->Digital readings for GUI
    humidity.set(str(round(humid_avg,1))+"%" )        
    
    #Live Plotting
    #---------------------Temperature Plot ------------------#
    #Append sensor reading data
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append((temp_avg))
    
    #axis limits
    xs = xs[-5:]
    ys = ys[-5:]

    # Update line with new Y values
    ax.clear()
    ax.plot(xs,ys)
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.title('Temperature over Time', color='w')
    plt.ylabel('Temp C', color='w')
    plt.grid(True)
    #--------------------- End ------------------------------#
    
    #---------------------Humidity Plot ---------------------#
    #Append sensor reading data
    xs2.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys2.append((humid_avg))
    
    #axis limits
    xs2 = xs2[-5:]
    ys2 = ys2[-5:]
    
    ax2.clear()
    ax2.plot(xs2,ys2)

    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    plt.title('Humidity over Time', color='w')
    plt.ylabel('%', color='w')
    plt.grid(True)
    #--------------------- End ------------------------------#
    
    fig.tight_layout()
    
    
    if TLower_green <= temp_avg <= TUpper_green : 
        temp_colour = "#12c702"
    elif  TLower_yellow <= temp_avg <= TUpper_yellow :
        temp_colour = "#ffcc00"
    else: 
        temp_colour = "#ff0000"

    if HLower_green <= humid_avg <= HUpper_green : 
        humid_colour = "#12c702"
    elif  HLower_yellow <= humid_avg <= HUpper_yellow :
        humid_colour = "#ffcc00"
    else: 
        humid_colour = "#ff0000"

    temperatureLabel.config(fg = temp_colour)
    humidityLabel.config(fg = humid_colour)
    win.update()
    #Warning message
    if temp_avg<10.0:
        win.configure(background='#FF0000')
    else:
        win.configure(background='black')
    

#--------------------Buttons----------------------------------#

def Report():

    filedialog.askopenfile(parent=win,
                                    filetypes = (("Text files", "*.txt"), ("All files", "*")))

def ThingSpeak():
    webbrowser.open_new("https://thingspeak.com/channels/1318645")

report_button = tk.Button(win, text="Report", command=Report)
report_button.pack()
report_button.place(x=100,y=0)

thingspeak_button = tk.Button(win, text="ThingSpeak", command=ThingSpeak)
thingspeak_button.pack()
thingspeak_button.place(x=0,y=0)

#----------------------------End of buttons--------------------------------------

#---------------------------Clock ----------------------------------------------------------------
class Clock:
    def __init__(self):
        self.time1 = ''
        self.time2 = time.strftime('%d-%m-%y %H:%M:%S:%p:%Z')

        self.mFrame = Frame()
        self.mFrame.pack(expand=YES,fill=X)
        self.mFrame.place(x=560, y=0)
        self.watch = Label(self.mFrame, text=self.time2, font=('times',14, 'bold' ),background='black', fg="white")

        self.watch.pack()
        
        self.changeLabel() #first we call it manually

    def changeLabel(self): 
        self.time2 = time.strftime('%Y-%m-%d %H:%M:%S:%p:%Z')
        self.watch.configure(text=self.time2)
        self.mFrame.after(200, self.changeLabel) #it will call itself continuously
Clock()

#-------------------------------End clock--------------------------------- 

canv = FigureCanvasTkAgg(fig, master = win)
canv._tkcanvas.pack(side=tk.BOTTOM)
canv.draw()

get_widz = canv.get_tk_widget()
get_widz.pack()

def exit_(event):                                    #Exit fullscreen
    win.quit() 

win.attributes("-fullscreen",True)             #Fullscreen when executed 
win.bind('<Escape>',exit_)                      #ESC to exit
#---------------------------------End Of GUI -------------------------------------------------------------------------------
#____________________________________________________________________________________________________________________


#__________________________________________________________________________________________________________________
#-------------------------------Creating Threads--------------------------------------------------------------------
# Creates threads and starts all functions as needed
try:
    print("test")
    _thread.start_new_thread( sensor0, ("sensor_1", 2, ) )#starts recording sensor on D4
    _thread.start_new_thread( sensor1, ("sensor_2", 2, ) )#starts recording sensor on D18
    _thread.start_new_thread( avg,     ("average" , 4, ) )
    _thread.start_new_thread( cloud,   ("upload"  , 300, ) )
    _thread.start_new_thread( local,   ("local"   , 300, ) )
    ani = animation.FuncAnimation(fig, animate, interval=2000, fargs=(xs,ys,xs2,ys2) )
    
except:
    print ("Error: unable to start thread")



#-----------------------------End of Starting Threads----------------------------------------------------
#_________________________________________________________________________________________________________

#______________________________________________________________________________________________
#-------------------main loop for the programe------------------------------------------------- 



try:
    win.mainloop()
except:
    subprocess.run('~/LabWatchGUI6/runme.sh', shell=True)
    quit()
finally:
    pass
#-------------------------End of Main Loop-----------------------------------------------------
#_______________________________________________________________________________________________


#end of code 
