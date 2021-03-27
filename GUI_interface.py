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

#System Restart 
import subprocess


from tkinter import messagebox
from tkinter import filedialog

#email sending 
import email_sending
from dateutil.relativedelta import relativedelta
import zip1

sendto="saltydick61@gmail.com"
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
myAPI = 'DLSQ0NFWVP2CQU4N' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
link = "https://thingspeak.com/channels/1318645"
#-------------------------------------------------------------------
#-------------------Tkinter Variables + Plot attributes-----------------------------------------
#Tkinter window
win = tk.Tk()

#Live update plot of temp and humidity

#Create figure for plotting
fig = plt.figure()
fig.patch.set_facecolor('black')
fig.set_size_inches(8, 1.8)

ax = fig.add_subplot(1,2,1)
xs = []
ys = []

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

ax2 = fig.add_subplot(1,2,2)
xs2 = []
ys2 = [] 

ax2.tick_params(axis='x', colors='white')
ax2.tick_params(axis='y', colors='white')

#upper lower bounds for ranges 
TUpper_green = 22 #for temp ranges 
TLower_green = 19

TUpper_yellow = 25 
TLower_yellow = 17

HUpper_green = 42 #for humid ranges 
HLower_green = 36

HUpper_yellow = 46 
HLower_yellow = 32

tempHUG = HUpper_green
tempHLG = HLower_green
tempHUY = HUpper_yellow
tempHLY = HLower_yellow

tempTUG = TUpper_green
tempTLG = TLower_green
tempTUY = TUpper_yellow
tempTLY = TLower_yellow

temp_colour = "#000000"
humid_colour = "#000000"


#______________________________________________________________________________________________________________________________
#-------------------------------------------Text File Read And Write Function------------------------------------------------

def read_file():
    global myAPI
    global TUpper_green
    global TLower_green
    global TUpper_yellow
    global TLower_yellow
    global HUpper_green
    global HLower_green
    global HUpper_yellow
    global HLower_yellow
    global link
    global baseURL
    global sentdo
    try:
        cwd = os.getcwd()
        path = cwd+ "/load.txt"
        f = open(path,'r')
        myAPI =  str(f.readline())
        TUpper_green = int(f.readline())
        TLower_green = int(f.readline())
        TUpper_yellow = int(f.readline())
        TLower_yellow = int(f.readline())
        HUpper_green = int(f.readline())
        HLower_green = int(f.readline())
        HUpper_yellow = int(f.readline())
        HLower_yellow = int(f.readline())
        link = str(f.readline())
        sendto = str(f.readline())
        f.close()
        myAPI=  myAPI.rstrip('\n')
        baseURL = baseURL.rstrip('\n')
        sendto = sendto.rstrip('\n')
        # print(myAPI)
        baseURL = 'https://api.thingspeak.com/update?api_key=%s'% myAPI
        # print(baseURL)
        # print(sendto)
    except Exception as e:
            print(f'Error Read: {e}')

def write_file():
    # print("write run")
    global myAPI
    global TUpper_green
    global TLower_green
    global TUpper_yellow
    global TLower_yellow
    global HUpper_green
    global HLower_green
    global HUpper_yellow
    global HLower_yellow
    global link
    global sendto
    try:
        cwd = os.getcwd()
        path = cwd+ "/load.txt"
        
        f = open(path,'w')
        f.write(myAPI + "\n" + str(TUpper_green) + "\n" + str(TLower_green) + "\n" + str(TUpper_yellow) + "\n" + str(TLower_yellow) + "\n" + str(HUpper_green) + "\n" + str(HLower_green) + "\n" + str(HUpper_yellow) + "\n" + str(HLower_yellow )+ "\n" + link + "" + sendto)
        f.close()
    except Exception as e:
            print(f'Error Write: {e}')

 

#----------------------------------------------------------------------------------------------------------------------------
#______________________________________________________________________________________________________________________________


#______________________________________________________________________________________________________________________________
#------------------Everything Between lines for Sensor read Data and error checking--------------------------------------------- 


# DHT22 Sensor on Pin D4 
def sensor0( threadName, delay):
    global temp0
    global humid0
    global sensor_fault0
    global temp_avg
    fault = bool(0)
    temp = 0
    while True:
        for x in range(10):
            try:
                # Print the values to the serial port
                temperature_c = dhtDevice0.temperature
                humidity = dhtDevice0.humidity
                if (abs(temp - temperature_c ) < 4):
                    fault = bool(0)
                temp = temperature_c 
                break       
                
            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                time.sleep(delay)
                
            except Exception as error:
                dhtDevice0.exit()
                raise error
            if (x > 8):
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
    temp = 0 
    while True: #runs forever 
        for x in range(10):#tries 5 times before thorwing fault for sensor 
            try:
                # Print the values to the serial port
                temperature_c = dhtDevice1.temperature
                humidity = dhtDevice1.humidity
                if (abs(temp - temperature_c ) < 4): # if the sensor is within a certain range it will be used again 
                    fault = bool(0)
                temp = temperature_c 
                break       
                    
            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                time.sleep(delay)
                
            except Exception as error:
                dhtDevice1.exit()
                raise error
            if (x > 8):
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
            # messagebox.showerror("SENSOR ERROR", "SENSOR 2 FAULT ON D18")
            
        elif (sensor_fault0 == True and sensor_fault1 == False): #D4 Bad D18 OK
            temp_avg = (temp1 + temp_last_avg) / 2
            humid_avg = (humid1 + humid_last_avg) / 2 
            # messagebox.showerror("SENSOR ERROR", "SENSOR 1 FAULT ON D4")
            
        else: #both Bad set to 0 , 0 
            temp_avg = 0
            humid_avg = 0
            # messagebox.showerror("SENSOR ERROR", "SENSOR 1 AND 2 FAULT")

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
    time.sleep(17)
    while True:

        try:
            conn = urlopen(baseURL + '&field1=%s&field2=%s' % (temp_avg, humid_avg))
            conn.close()
        except Exception as e:
            print(f'Error: {e}')
            print("Connection Failed")
        time.sleep(delay)




#-------------------------------------End of Thingspeak Uploading ---------------------------------------------------------------------------
#____________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

#---------------------------------------------Emailing-------------------------------------------------
def alert( delay):
    global sensor_fault0
    global sensor_fault1
    time.sleep(30)
    while True: #runs the avg loop forever 
        
        # mutltiple statments checking different sinarios for faulty sensor 
        if (sensor_fault0 == True and sensor_fault1 == True) :#both good
            messagebox.showerror("SENSOR ERROR", "SENSOR 1 AND 2 FAULT")
    
            
        elif (sensor_fault0 == False and sensor_fault1 == True) :#D4 OK D18 Bad
            messagebox.showerror("SENSOR ERROR", "SENSOR 2 FAULT ON D18")
            
        elif (sensor_fault0 == True and sensor_fault1 == False): #D4 Bad D18 OK
            messagebox.showerror("SENSOR ERROR", "SENSOR 1 FAULT ON D4")
            
        time.sleep(delay)#sleeps for set delay time 

def email(threadName,delay):
    global temp_avg
    global humid_avg
    global TUpper_yellow
    global TLower_yellow
    global HUpper_yellow
    global HLower_yellow
    global sendto
    lastrun = datetime.now()
    
    while True: 
        
        
        now = datetime.now()
        date_diff = now - lastrun   
        total_time = date_diff.total_seconds()
        # print(total_time)
        if(TUpper_yellow < temp_avg or TLower_yellow > temp_avg or HUpper_yellow < humid_avg or HLower_yellow > humid_avg ):
            if (total_time > 3600): #3600 hour
                email_sending.sendwarning(sendto, temp_avg, humid_avg)
                lastrun = datetime.now()
        
        date_time = now.strftime("%d, %H:%M")
        # print(date_time)
        if(date_time == "01, 04:00"):
            date_file = datetime.today() + relativedelta(months=-1)
            # print(date_file)
            sent = True
            x = 0
            while sent:
                sent = email_sending.sendfile(sendto,date_file)
                if x>6:
                    sent = False
                x= x+1   
            time.sleep(120)
        time.sleep(delay)




#-------------------------------------End of Emailing ---------------------------------------------------------------------------
#____________________________________________________________________________________________________________________

#________________________________________________________________________________________________________________________________

#-------------------------------------Local Logging-------------------------------------------------

def local(threadName, delay):
    global temp0
    global humid0
    global temp1
    global humid1
    time.sleep(20)
    while True:
        try:
            # print(os.getcwd())
            cwd = os.getcwd()
            timenow = datetime.now()
            yrnow = timenow.strftime("%Y")
            monow = timenow.strftime("%m")
            daynow = timenow.strftime("%d")
            path = cwd+ "/Logging/{}-{}.csv".format(yrnow,monow)
            # path = "/home/pi/LabWatchGUI6/Logging/{}-{}.csv".format(yrnow,monow)
            # print(path)
            file = open(path, "a")
            file = open(path, "a")
            if os.stat(path).st_size == 0:
                file.write("Time,S1TempC,S1Humid,S2TempC,S2Humid,\n")

            file.write(str(timenow.strftime("%m/%d/%Y %H:%M"))+","+str(temp0)+","+str(humid0)+","+str(temp1)+","+str(humid1)+"\n")
            file.flush()
            file.close()
        except Exception as e:
            pass
            # print(f'Error: {e}')
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
temperatureLabel.place(x=70, y=130)             #Character "----C" placement and attributes

humidityLabel = Label(win, fg=humid_colour, background="black", textvariable=humidity, font=("Segoe UI", 60,"bold"))       #bg color,font and font size
humidityLabel.place(x=485, y=130)              #Character "----%" placement and attributes
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
    temperature.set(str(temp_avg)+"°C")            
    #Send variables from hum to StringVar for temperatur.set above in---->Digital readings for GUI
    humidity.set(str(humid_avg)+"%" )        

    #Live Plotting
    #---------------------Temperature Plot ------------------#
    #Append sensor reading data
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(temp_avg)

    #axis limits
    xs = xs[-4:]
    ys = ys[-4:]
    
    #Plot graph and clear (update new reading)
    ax.clear()

    #Plot Labels
    ax.set_title('Temperature over Time', color='w')
    ax.set_xlabel('Time',color ='w')
    ax.set_ylabel('Temp °C', color='w')
    
    ax.plot(xs,ys)
    ax.grid(True)
    #--------------------- End ------------------------------#

    #---------------------Humidity Plot ---------------------#
    #Append sensor reading data
    xs2.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys2.append(humid_avg)

    #axis limits
    xs2 = xs2[-4:]
    ys2 = ys2[-4:]
    
    #Plot graph clear and label (update new reading)
    ax2.clear()
    #Plot Labels
    ax2.set_title('Humidity over time', color='w')
    ax2.set_xlabel('Time',color ='w')
    ax2.set_ylabel('Hum %', color='w')
    
    ax2.plot(xs2,ys2)
    ax2.grid(True)
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

win.configure(background='black')

#--------------------Buttons----------------------------------#
def SendReport():
    global sendto
    path = zip1.zipping()
    email_sending.sendall(sendto,path)

def Report():
    global sendto
    date_file = datetime.today()
    sent = email_sending.sendfile(sendto,date_file)

def ThingSpeak():
    global link
    webbrowser.open_new(link)




def settings1():
    global tempTUG
    global tempTLG
    global tempTUY
    global tempTLY
    global TUpper_green
    global TLower_green
    global TUpper_yellow
    global TLower_yellow
    tempTUG = TUpper_green
    tempTLG = TLower_green
    tempTUY = TUpper_yellow
    tempTLY = TLower_yellow
    # Toplevel object which will  
    # be treated as a new window 
    sus = Toplevel() 
    sus.overrideredirect(True) 
    # sets the title of the 
    # Toplevel widget 
    sus.title("Tempature Range Adjustments Window") 
    
    # sets the geometry of toplevel 
    sus.geometry("800x800") 

    Label(sus,text ='Tempature Range Settings',font=("Segoe UI", 14,"bold")).place(in_=sus,x=250,y=70)
    
    
    def TUGU():
        global tempTUG
        global tempTUY
        if tempTUY > tempTUG +1 : 
            tempTUG = tempTUG + 1
        NUG = Label(sus,text =tempTUG).place(in_=sus,x=550,y=250)
        return tempTUG

    def TUGD():
        global tempTUG
        global tempTLG
        if tempTLG < tempTUG-1 :
            tempTUG = tempTUG - 1
        NUG = Label(sus,text =tempTUG).place(in_=sus,x=550,y=250)
        return tempTUG

    def TLGU():
        global tempTLG
        global tempTUG
        if tempTLG < tempTUG-1 :
            tempTLG = tempTLG + 1
        NLG = Label(sus,text =tempTLG).place(in_=sus,x=275,y=250)
        return tempTLG

    def TLGD():
        global tempTLG
        global tempTLY
        if tempTLG > tempTLY +1 : 
            tempTLG = tempTLG - 1
        NLG = Label(sus,text =tempTLG).place(in_=sus,x=275,y=250)
        return tempTLG

    def TUYU():
        global tempTUY
        tempTUY = tempTUY + 1
        NUY = Label(sus,text =tempTUY).place(in_=sus,x=750,y=250)
        return tempTUY

    def TUYD():
        global tempTUY
        global tempTUG
        if tempTUG < tempTUY-1 : 
            tempTUY = tempTUY - 1
        NUY = Label(sus,text =tempTUY).place(in_=sus,x=750,y=250)
        return tempTUY

    def TLYU():
        global tempTLY
        global tempTLG
        if tempTLG > tempTLY +1 : 
            tempTLY = tempTLY + 1
        NLY = Label(sus,text =tempTLY).place(in_=sus,x=50,y=250)
        return tempTLY

    def TLYD():
        global tempTLY
        tempTLY = tempTLY - 1
        NLY = Label(sus,text =tempTLY).place(in_=sus,x=50,y=250)
        return tempTLY

    def SaveHum():
        global tempTUG
        global tempTLG
        global tempTUY
        global tempTLY
        global TUpper_green
        global TLower_green
        global TUpper_yellow
        global TLower_yellow
        TUpper_green = tempTUG
        TLower_green = tempTLG
        TUpper_yellow = tempTUY
        TLower_yellow = tempTLY
        sus.destroy()
        write_file()

    # A Label widget to show in toplevel 

    Label(sus,text ="Set Upper Limit").place(in_=sus,x=500,y=200)
    NUG = Label(sus,text =tempTUG).place(in_=sus,x=550,y=250)

    Label(sus,text ="Set Lower Limit").place(in_=sus,x=225,y=200)
    NLG = Label(sus,text =tempTLG).place(in_=sus,x=275,y=250)

    Label(sus,text ="Set Upper Limit").place(in_=sus,x=690,y=200)
    NUY = Label(sus,text =tempTUY).place(in_=sus,x=750,y=250)

    Label(sus,text ="Set Lower Limit").place(in_=sus,x=0,y=200)
    NLY = Label(sus,text =tempTLY).place(in_=sus,x=50,y=250)
    
    up_button1 = tk.Button(sus,bg = 'yellow', text = "↑",command=TLYU).place(in_=sus,x=42,y=300)
    down_button1 = tk.Button(sus,bg = 'yellow', text = "↓",command=TLYD).place(in_=sus,x=42,y=350)

    up_button2 = tk.Button(sus,bg = 'green', text = "↑",command=TLGU).place(in_=sus,x=268,y=300)
    down_button2 = tk.Button(sus,bg = 'green', text = "↓",command=TLGD).place(in_=sus,x=268,y=350)

    up_button1 = tk.Button(sus,bg = 'green', text = "↑",command=TUGU).place(in_=sus,x=542,y=300)
    down_button1 = tk.Button(sus,bg = 'green', text = "↓",command=TUGD).place(in_=sus,x=542,y=350)

    up_button2 = tk.Button(sus,bg = 'yellow', text = "↑",command=TUYU).place(in_=sus,x=742,y=300)
    down_button2 = tk.Button(sus,bg = 'yellow', text = "↓",command=TUYD).place(in_=sus,x=742,y=350)

    exit = tk.Button(sus, text = "Exit",command=SaveHum).place(in_=sus,x=370,y=110)





def settings2():
    global tempHUG
    global tempHLG
    global tempHUY
    global tempHLY
    global HUpper_green
    global HLower_green
    global HUpper_yellow
    global HLower_yellow
    
    tempHUG = HUpper_green
    tempHLG = HLower_green
    tempHUY = HUpper_yellow
    tempHLY = HLower_yellow
    # Toplevel object which will  
    # be treated as a new window 
    sus = Toplevel() 
    sus.overrideredirect(True) 
    # sets the title of the 
    # Toplevel widget 
    sus.title("Humidity Range Adjustments Window") 
    
    # sets the geometry of toplevel 
    sus.geometry("800x800") 

    Label(sus,text ='Humidity Range Settings',font=("Segoe UI", 14,"bold")).place(in_=sus,x=250,y=70)
    
    
    def HUGU():
        global tempHUG
        global tempHUY
        if tempHUY > tempHUG +1: 
            tempHUG = tempHUG + 1
        NUG = Label(sus,text =tempHUG).place(in_=sus,x=550,y=250)
        return tempHUG

    def HUGD():
        global tempHUG
        global tempHLG
        if tempHUG-1 > tempHLG :
            tempHUG = tempHUG - 1
        NUG = Label(sus,text =tempHUG).place(in_=sus,x=550,y=250)
        return tempHUG

    def HLGU():
        global tempHLG
        global tempHUG
        if tempHUG > tempHLG+1:
            tempHLG = tempHLG + 1
        NLG = Label(sus,text =tempHLG).place(in_=sus,x=275,y=250)
        return tempHLG

    def HLGD():
        global tempHLG
        global tempHLY
        if tempHLG > tempHLY+1:
            tempHLG = tempHLG - 1
        NLG = Label(sus,text =tempHLG).place(in_=sus,x=275,y=250)
        return tempHLG

    def HUYU():
        global tempHUY
        tempHUY = tempHUY + 1
        NUY = Label(sus,text =tempHUY).place(in_=sus,x=750,y=250)
        return tempHUY

    def HUYD():
        global tempHUY
        global tempHUG
        if tempHUY > tempHUG +1:
            tempHUY = tempHUY - 1
        NUY = Label(sus,text =tempHUY).place(in_=sus,x=750,y=250)
        return tempHUY

    def HLYU():
        global tempHLY
        global tempHLG
        if tempHLY<tempHLG-1:
            tempHLY = tempHLY + 1
        NLY = Label(sus,text =tempHLY).place(in_=sus,x=50,y=250)
        return tempHLY

    def HLYD():
        global tempHLY
        tempHLY = tempHLY - 1
        NLY = Label(sus,text =tempHLY).place(in_=sus,x=50,y=250)
        return tempHLY

    def SaveHum():
        global tempHUG
        global tempHLG
        global tempHUY
        global tempHLY
        global HUpper_green
        global HLower_green
        global HUpper_yellow
        global HLower_yellow
        HUpper_green = tempHUG
        HLower_green = tempHLG
        HUpper_yellow = tempHUY
        HLower_yellow = tempHLY
        sus.destroy()
        write_file()


    Label(sus,text ="Set Upper Limit").place(in_=sus,x=500,y=200)
    NUG = Label(sus,text =tempHUG).place(in_=sus,x=550,y=250)

    Label(sus,text ="Set Lower Limit").place(in_=sus,x=225,y=200)
    NLG = Label(sus,text =tempHLG).place(in_=sus,x=275,y=250)

    Label(sus,text ="Set Upper Limit").place(in_=sus,x=690,y=200)
    NUY = Label(sus,text =tempHUY).place(in_=sus,x=750,y=250)

    Label(sus,text ="Set Lower Limit").place(in_=sus,x=0,y=200)
    NLY = Label(sus,text =tempHLY).place(in_=sus,x=50,y=250)
    
    up_button1 = tk.Button(sus,bg = 'yellow', text = "↑",command=HLYU).place(in_=sus,x=42,y=300)
    down_button1 = tk.Button(sus,bg = 'yellow', text = "↓",command=HLYD).place(in_=sus,x=42,y=350)

    up_button2 = tk.Button(sus,bg = 'green', text = "↑",command=HLGU).place(in_=sus,x=268,y=300)
    down_button2 = tk.Button(sus,bg = 'green', text = "↓",command=HLGD).place(in_=sus,x=268,y=350)

    up_button1 = tk.Button(sus,bg = 'green', text = "↑",command=HUGU).place(in_=sus,x=542,y=300)
    down_button1 = tk.Button(sus,bg = 'green', text = "↓",command=HUGD).place(in_=sus,x=542,y=350)

    up_button2 = tk.Button(sus,bg = 'yellow', text = "↑",command=HUYU).place(in_=sus,x=742,y=300)
    down_button2 = tk.Button(sus,bg = 'yellow', text = "↓",command=HUYD).place(in_=sus,x=742,y=350)
    
    exit = tk.Button(sus, text = "Exit",command=SaveHum).place(in_=sus,x=370,y=110)
    
    # Exit = tk.Button(sus, text = "Exit Withoug Saving",command=nonSaveHum).place(in_=sus,x=500,y=750)

def Reports():
    # Toplevel object which will  
    # be treated as a new window 
    sus = Toplevel() 
    
    # sets the title of the 
    # Toplevel widget 
    sus.overrideredirect(True)  
    sus.configure(bg='black')
    # sets the geometry of toplevel 
    sus.geometry("270x300") 

    Label(sus,text ='Reports', font=("Segoe UI", 20,"bold"), bg='black', fg='white').place(in_=sus,x=78,y=10)
    
    report_button = tk.Button(sus, text="Report",fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 12,"bold"), command=Report)
    report_button.place(x=95,y=70)

    thingspeak_button = tk.Button(sus, text="ThingSpeak",  fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 12,"bold"),command=ThingSpeak)
    thingspeak_button.place(x=75,y=120)
    
    sendall_button = tk.Button(sus, text="Send all report", fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 12,"bold"),command=SendReport)
    sendall_button.place(x=60,y=170)
    
    def ExitWin():
        sus.destroy()
        
    tk.Button(sus, text = "Exit",font=("Segoe UI", 12,"bold"), relief="solid",activebackground='black',activeforeground='white',command=ExitWin).place(in_=sus,x=110,y=230)
    
report_button = tk.Button(win, text="Report",fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 12,"bold"),command=Reports)
report_button.pack()
report_button.place(x=120,y=0)

def Settings():
    # Toplevel object which will  
    # be treated as a new window 
    sus = Toplevel() 
    
    # sets the title of the 
    # Toplevel widget 
    sus.overrideredirect(True) 
    
    sus.configure(bg='black')
    # sets the geometry of toplevel 
    sus.geometry("300x300")

    Label(sus,text ='Settings', font=("Segoe UI", 20,"bold"), bg='black', fg='white').place(in_=sus,x=85,y=10)
    
    report_button = tk.Button(sus, text="Temp Rang Adjust",fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 12,"bold"), command=settings1)
    report_button.place(x=60,y=70)

    thingspeak_button = tk.Button(sus, text="Humi Rang Adjust",  fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 12,"bold"),command=settings2)
    thingspeak_button.place(x=60,y=120)
    
    def ExitWin():
        sus.destroy()
        
    tk.Button(sus, text = "Exit",font=("Segoe UI", 12,"bold"), relief="solid",activebackground='black',activeforeground='white',command=ExitWin).place(in_=sus,x=125,y=190)

b1 = tk.Button(win, text="Settings",fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 12,"bold"), command=Settings)
b1.pack()
b1.place(x=0,y=0)

# b1 = tk.Button(win, text="Humidity Range Adjustments", bg="white",command=settings2)
# b1.pack()
# b1.place(x=200,y=50)

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
    os.chdir('/home/pi/LabWatchGUI6')    
    read_file()
    _thread.start_new_thread( sensor0, ("sensor_1", 2, ) )#starts recording sensor on D4
    _thread.start_new_thread( sensor1, ("sensor_2", 2, ) )#starts recording sensor on D18
    _thread.start_new_thread( avg,     ("average" , 4, ) )
    _thread.start_new_thread( cloud,   ("upload"  , 300, ) )
    _thread.start_new_thread( local,   ("local"   , 300, ) )
    _thread.start_new_thread( email,   ("Warning" , 45, ) )
    _thread.start_new_thread( alert,   (            45, ) )
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

