#!/usr/bin/python3

#--------------------------------------Import Libraries---------------------------------------------#

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

#Tkinter Library
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

sendto=""
#-----------End of Import Libraries------------------------#

#-----------Sensor Global Variables------------------------#

#----------------------------------Sensor Global Variables-------------------------------------------#
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

#------------------------------------------------------------------------------------------------------#
#---------------------------------------ThingSpeak Global Variables------------------------------------#
#ThingSpeak credentrials 
myAPI = 'RXXLLQDW8BV1S7WW' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
link = "https://thingspeak.com/channels/1311268"
#------------------------------------------------------------------------------------------------------#

#-----------------------------------Tkinter Variables + Plot attributes--------------------------------#




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

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

ax2 = fig.add_subplot(1,2,2)
xs2 = []
ys2 = [] 

ax2.tick_params(axis='x', colors='white')
ax2.tick_params(axis='y', colors='white')

#---------------------------------Digital readings color display------------------------------------------#
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




Toffset = 0
Hoffset = 0
tempToff = Toffset
tempHoff = Hoffset


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
    global sendto
    global Toffset
    global Hoffset
    global email
    try:
        cwd = os.getcwd()
        path = cwd+ "/load.txt"
        f = open(path,'r')
        
        TUpper_green = int(f.readline())
        TLower_green = int(f.readline())
        TUpper_yellow = int(f.readline())
        TLower_yellow = int(f.readline())
        HUpper_green = int(f.readline())
        HLower_green = int(f.readline())
        HUpper_yellow = int(f.readline())
        HLower_yellow = int(f.readline())
        Toffset = float(f.readline())
        Hoffset = float(f.readline())
        myAPI =  str(f.readline())
        link = str(f.readline())
        sendto = str(f.readline())
        f.close()
        myAPI=  myAPI.rstrip('\n')
        baseURL = baseURL.rstrip('\n')
        sendto = sendto.rstrip('\n')
        
        baseURL = 'https://api.thingspeak.com/update?api_key=%s'% myAPI
        # print(myAPI)
        # print(baseURL)
        # print(sendto)
    except Exception as e:
        TUpper_green = 22 #for temp ranges 
        TLower_green = 19

        TUpper_yellow = 25 
        TLower_yellow = 17

        HUpper_green = 42 #for humid ranges 
        HLower_green = 36

        HUpper_yellow = 46 
        HLower_yellow = 32
        sendto="labwatchmonitoring@gmail.com"
        myAPI = 'RXXLLQDW8BV1S7WW' 
        # URL where we will send the data, Don't change it
        baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
        link = "https://thingspeak.com/channels/1311268"
        email = False
        # print(f'Error Read: {e}')

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
    global Toffset
    global Hoffset
    global link
    global sendto
    global email
    # print(sendto)
    if(email):
        try:
            cwd = os.getcwd()
            path = cwd+ "/load.txt"
            
            f = open(path,'w')
            f.write( str(TUpper_green) + "\n" + str(TLower_green) + "\n" + str(TUpper_yellow) 
                    + "\n" + str(TLower_yellow) + "\n" + str(HUpper_green) + "\n" + str(HLower_green) + "\n" 
                        + str(HUpper_yellow) + "\n" + str(HLower_yellow )+ "\n" + str(Toffset ) + "\n" + str(Hoffset)+ "\n"+ myAPI + "\n" + link + "" + sendto)
            f.close()
        except Exception as e:
                # print(f'Error Write: {e}')
                pass
    else:
        try:
            cwd = os.getcwd()
            path = cwd+ "/load.txt"
            
            f = open(path,'w')
            f.write(str(TUpper_green) + "\n" + str(TLower_green) + "\n" + str(TUpper_yellow) 
                    + "\n" + str(TLower_yellow) + "\n" + str(HUpper_green) + "\n" + str(HLower_green) + "\n" 
                        + str(HUpper_yellow) + "\n" + str(HLower_yellow )+ "\n" + str(Toffset ) + "\n" + str(Hoffset))
            f.close()
        except Exception as e:
                # print(f'Error Write: {e}')
                pass
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
    global temp0
    global humid0
    global temp1
    global humid1
    global sensor_fault0
    global sensor_fault1
    global Toffset
    global Hoffset
    temp = -Toffset
    humid = -Hoffset
    while True: #runs the avg loop forever 
        
        temp_last_avg = temp #stores current avgerage as last avg 
        humid_last_avg = humid
        # mutltiple statments checking different sinarios for faulty sensor 
        if (sensor_fault0 == False and sensor_fault1 == False) :#both good
            tempdiff = abs(temp0-temp1)
            humiddiff = abs(humid0-humid1)
            # print(tempdiff)
            if (tempdiff < 4 and humiddiff < 10) :# they are roughly the same value 
                temp = (temp0 + temp1 + temp_last_avg) / 3
                humid = (humid0 + humid1 + humid_last_avg) / 3
                # print(temp)
                # print(humid)
        elif (sensor_fault0 == False and sensor_fault1 == True) :#D4 OK D18 Bad
            temp = (temp0 + temp_last_avg) / 2
            humid = (humid0 + humid_last_avg) / 2
            # messagebox.showerror("SENSOR ERROR", "SENSOR 2 FAULT ON D18")
            
        elif (sensor_fault0 == True and sensor_fault1 == False): #D4 Bad D18 OK
            temp = (temp1 + temp_last_avg) / 2
            humid = (humid1 + humid_last_avg) / 2 
            # messagebox.showerror("SENSOR ERROR", "SENSOR 1 FAULT ON D4")
        else: #both Bad set to 0 , 0 
            temp = -Toffset
            humid = -Hoffset
            # messagebox.showerror("SENSOR ERROR", "SENSOR 1 AND 2 FAULT")
        
        temp_avg = round(temp + Toffset,1)
        humid_avg = round(humid + Hoffset,1)
        # prints to terminal for error checking 
        # print(
        #         "Temp_avg:  {:.1f} C    Humidity_avg: {:.1f}%   sensor0: {}   Sensor1: {} ".format(
        #             temp_avg, humid_avg,sensor_fault0,sensor_fault1
        #         )
        #     ) 
        time.sleep(delay)#sleeps for set delay time 

#-----------------------------------End of sensor Data read and error Check---------------------------#
#______________________________________________________________________________________________________
#______________________________________________________________________________________________________

#--------------------------------------Thingspeak Function Validation---------------------------------#
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
            # print(f'Error: {e}')
            # print("Connection Failed")
            pass
        local0()
        time.sleep(delay)

#-------------------------------------End of Thingspeak Uploading ------------------------------------#
#______________________________________________________________________________________________________
#______________________________________________________________________________________________________

#-------------------------------------Sensor read aler error message----------------------------------#
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
#-----------------------------------------------End---------------------------------------------------#
#______________________________________________________________________________________________________
#______________________________________________________________________________________________________
#---------------------------------------------Emailing------------------------------------------------#
#Enter email for sending reports to

def email(threadName,delay):
    global temp_avg
    global humid_avg
    global TUpper_yellow
    global TLower_yellow
    global HUpper_yellow
    global HLower_yellow
    global sendto
    lastrun = datetime.now()
    global is_on
    while True: 
        now = datetime.now()
        date_diff = now - lastrun   
        total_time = date_diff.total_seconds()
        # print(total_time)
        if(TUpper_yellow < temp_avg or TLower_yellow > temp_avg or HUpper_yellow < humid_avg or HLower_yellow > humid_avg ):
            if (total_time > 3600 and is_on): #3600 hour
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
#-------------------------------------End of Emailing ---------------------------------------------#
#___________________________________________________________________________________________________
#___________________________________________________________________________________________________

#-------------------------------------Local Logging------------------------------------------------#

def local0():
    global temp0
    global humid0
    global temp1
    global humid1
    
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
    



#-------------------------------------End of Local Logging -----------------------------------------#
#____________________________________________________________________________________________________
#____________________________________________________________________________________________________
#-----------------------------------GUI to local User Code------------------------------------------#

#Digital readings for GUI
temperature = StringVar()                       #is a class that provides helper functions for directly creating and accessing such variables in that interpreter.
temperature.set("----"+ "°C")	                #Temperature set to store multiple items in a single variable	

humidity = StringVar()
humidity.set("----"+" %")		                #Humidity set to store multiple items in a single variable	

temperatureLabel = Label(win, fg=temp_colour, background="black", textvariable=temperature, font=("Segoe UI", 60,"bold")) #bg color,font and font size
temperatureLabel.place(x=70, y=130)             #Character "----C" placement and attributes

humidityLabel = Label(win, fg=humid_colour, background="black", textvariable=humidity, font=("Segoe UI", 60,"bold"))       #bg color,font and font size
humidityLabel.place(x=485, y=130)              #Character "----%" placement and attributes
#-------------------------------End of Digital readings for GUI--------------------------------------#
#_____________________________________________________________________________________________________
#_____________________________________________________________________________________________________
#------------------------------------Animate function------------------------------------------------#
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
    #------------------------------Temperature Plot ---------------------------------------------#
    #Append sensor reading data
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(temp_avg)

    #axis limits
    xs = xs[-4:]
    ys = ys[-4:]
    
    #Plot graph and clear (update new reading)
    ax.clear()

    #Plot Labels
    ax.set_title('Temperature over Time', color='w', fontsize=14)
    ax.set_xlabel('Time',color ='w', fontsize=14)
    ax.set_ylabel('Temp °C', color='w', fontsize=14)
    
    ax.plot(xs,ys)
    ax.grid(True)
    #--------------------------------------End----------------------------------------------------#
    
    #---------------------------------Humidity Plot ----------------------------------------------#
    #Append sensor reading data
    xs2.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys2.append(humid_avg)

    #axis limits
    xs2 = xs2[-4:]
    ys2 = ys2[-4:]
    
    #Plot graph clear and label (update new reading)
    ax2.clear()
    #Plot Labels
    ax2.set_title('Humidity over time', color='w', fontsize=14)
    ax2.set_xlabel('Time',color ='w', fontsize=14)
    ax2.set_ylabel('Hum %', color='w', fontsize=14)
    
    ax2.plot(xs2,ys2)
    ax2.grid(True)
    fig.tight_layout()
    #-----------------------------------------End---------------------------------------------------#
    
    #---------------------------------Digital readings color range display--------------------------#
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
    
#------------------------------------------End of Animate function-----------------------------------#
#_____________________________________________________________________________________________________
#_____________________________________________________________________________________________________
#-------------------------------------------Main Buttons code ---------------------------------------#
def SendReport():
    global sendto
    path = zip1.zipping()
    email_sending.sendall(sendto,path)
    tk.messagebox.showinfo("REPORTS", "All of reports sent!")
    
def Report():
    global sendto
    date_file = datetime.today()
    sent = email_sending.sendfile(sendto,date_file)
    tk.messagebox.showinfo("REPORTS", "Current report sent!")
    
def ThingSpeak():
    global link
    webbrowser.open_new(link)


def settings0():
    global Toffset
    global Hoffset
    global tempHoff
    global tempToff
    tempToff = Toffset
    tempHoff = Hoffset
    
    #Window
    sus = Toplevel() 

    sus.overrideredirect(True)  
    sus.title("Offset Adjustment Window")  
    sus.geometry("800x600")
    sus.configure(bg='black')
    #win.config(cursor="none")
    
    def TU():
        global tempToff
        tempToff = tempToff + 0.5
        text2 = str(tempToff)+" °C "
        NUGS = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=160,y=295)
        return tempToff

    def TD():
        global tempToff
        tempToff = tempToff - 0.5
        text2 = str(tempToff)+" °C "
        NUGS = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=160,y=295)
        return tempToff

    def HU():
        global tempHoff 
        tempHoff = tempHoff + 0.5
        text2 = str(tempHoff)+" % "
        NUG = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=560,y=295)
        return tempHoff

    def HD():
        global tempHoff
        tempHoff = tempHoff - 0.5
        text2 = str(tempHoff)+" % "
        NUG = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=560,y=295)
        return tempHoff

    def Exit():
        global tempHoff
        global tempToff
        global Toffset
        global Hoffset
        Toffset = tempToff
        Hoffset = tempHoff
        sus.destroy()
        write_file()

    #Labels
    Label(sus,text ='OFFSET ADJUSTMENT',font=("Segoe UI", 24,"bold"),bg='black', fg='white').place(in_=sus,x=200,y=20)
    Label(sus,text ='Tempature',font=("Segoe UI", 22),bg='black', fg='white').place(in_=sus,x=110,y=160)
    Label(sus,text ='Humidity',font=("Segoe UI", 22),bg='black', fg='white').place(in_=sus,x=520,y=160)
    
    NUG = Label(sus,text =str(tempHoff)+" % ",font=("Segoe UI", 22),bg='black', fg='white').place(in_=sus,x=560,y=295)
    NUGS = Label(sus,text =str(tempToff)+" °C ",font=("Segoe UI", 22),bg='black', fg='white').place(in_=sus,x=160,y=295)
    
    #Up/Down Buttons
    up_button1 = tk.Button(sus, text = "↑",fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black",font=("Segoe UI", 22),
                        command=TU).place(in_=sus,x=170,y=220)
    
    down_button1 = tk.Button(sus, text = "↓",fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black",font=("Segoe UI", 22),
                        command=TD).place(in_=sus,x=170,y=360)

    up_button1 = tk.Button(sus, text = "↑",fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black",font=("Segoe UI", 22),
                        command=HU).place(in_=sus,x=560,y=220)
    
    down_button1 = tk.Button(sus, text = "↓",fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black",font=("Segoe UI", 22),
                        command=HD).place(in_=sus,x=560,y=360)
    
    #Exit Button
    tk.Button(sus,text ='Exit',width = 10,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black",
                        command=Exit,font=("Segoe UI", 18)).place(in_=sus,x=300,y=80)


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
    sus.geometry("800x600") 
    sus.configure(bg='black')
    #win.config(cursor="none")

    def TUGU():
        global tempTUG
        global tempTUY
        if tempTUY > tempTUG +1 : 
            tempTUG = tempTUG + 1
        text2 = str(tempTUG)+"°C"
        NUG = Label(sus,text = text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=475,y=215)
        return tempTUG

    def TUGD():
        global tempTUG
        global tempTLG
        if tempTLG < tempTUG-1 :
            tempTUG = tempTUG - 1
        text2 = str(tempTUG)+"°C"
        NUG = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=475,y=215)
        return tempTUG

    def TLGU():
        global tempTLG
        global tempTUG
        if tempTLG < tempTUG-1 :
            tempTLG = tempTLG + 1
        text2 = str(tempTLG)+"°C"
        NLG = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=265,y=215)
        return tempTLG

    def TLGD():
        global tempTLG
        global tempTLY
        if tempTLG > tempTLY +1 : 
            tempTLG = tempTLG - 1
        text2 = str(tempTLG)+"°C"
        NLG = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=265,y=215)
        return tempTLG

    def TUYU():
        global tempTUY
        tempTUY = tempTUY + 1
        text2 =str(tempTUY)+"°C"
        NUY = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=670,y=215)
        return tempTUY

    def TUYD():
        global tempTUY
        global tempTUG
        if tempTUG < tempTUY-1 : 
            tempTUY = tempTUY - 1
        text2 =str(tempTUY)+"°C"
        NUY = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=670,y=215)
        return tempTUY

    def TLYU():
        global tempTLY
        global tempTLG
        if tempTLG > tempTLY +1 : 
            tempTLY = tempTLY + 1
        text2 =str(tempTLY)+"°C"
        NLY = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=60,y=215)
        return tempTLY

    def TLYD():
        global tempTLY
        tempTLY = tempTLY - 1
        text2 =str(tempTLY)+"°C"
        NLY = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=60,y=215)
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

    #Window Title
    Label(sus,text ='TEMPERATURE RANGE SETTINGS',font=("Segoe UI", 24,"bold"),bg='black',fg='white').place(in_=sus,x=100,y=25)
    
    #Upper/lower limits
    Label(sus,text ="Upper",bg='black',fg='white',font=("Segoe UI", 22)).place(in_=sus,x=470,y=160)
    
    NUG = Label(sus,text =str(tempTUG)+"°C",bg="black",fg='white',font=("Segoe UI", 22)).place(in_=sus,x=475,y=215)

    Label(sus,text ="Lower",fg='white',bg='black',font=("Segoe UI", 22)).place(in_=sus,x=255,y=160)
    
    NLG = Label(sus,text =str(tempTLG)+"°C",bg="black",fg='white',font=("Segoe UI", 22)).place(in_=sus,x=265,y=215)

    Label(sus,text ="Upper",bg='black',fg='white',font=("Segoe UI", 22)).place(in_=sus,x=660,y=160)
    
    NUY = Label(sus,text =str(tempTUY)+"°C",bg="black",fg='white',font=("Segoe UI", 22)).place(in_=sus,x=670,y=215)

    Label(sus,text ="Lower",bg='black',fg='white',font=("Segoe UI", 22)).place(in_=sus,x=55,y=160)
    
    NLY = Label(sus,text =str(tempTLY)+"°C",bg="black",fg='white',font=("Segoe UI", 22)).place(in_=sus,x=60,y=215)
    
    #Up/Down buttons
    up_button1 = tk.Button(sus, text = "↑",bg = '#ffcc00',fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                        command=TLYU).place(in_=sus,x=72,y=275)
    down_button1 = tk.Button(sus,bg = '#ffcc00', text = "↓", fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=TLYD).place(in_=sus,x=72,y=350)

    up_button2 = tk.Button(sus,bg = '#12c702', text = "↑",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=TLGU).place(in_=sus,x=268,y=275)
    down_button2 = tk.Button(sus,bg = '#12c702', text = "↓",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=TLGD).place(in_=sus,x=268,y=350)

    up_button1 = tk.Button(sus,bg = '#12c702', text = "↑",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=TUGU).place(in_=sus,x=485,y=275)
    down_button1 = tk.Button(sus,bg = '#12c702', text = "↓",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=TUGD).place(in_=sus,x=485,y=350)

    up_button2 = tk.Button(sus,bg = '#ffcc00', text = "↑",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=TUYU).place(in_=sus,x=675,y=275)
    down_button2 = tk.Button(sus,bg = '#ffcc00', text = "↓",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=TUYD).place(in_=sus,x=675,y=350)

    exit = tk.Button(sus, text = "Exit",font=("Segoe UI", 18),width = 10,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black",
                    command=SaveHum).place(in_=sus,x=300,y=85)

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
    sus.configure(bg='black')
    # sets the geometry of toplevel 
    sus.geometry("800x600") 
    #win.config(cursor="none")
    def HUGU():
        global tempHUG
        global tempHUY
        if tempHUY > tempHUG +1: 
            tempHUG = tempHUG + 1
        text2=str(tempHUG)+"%"
        NUG = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=480,y=215)
        return tempHUG

    def HUGD():
        global tempHUG
        global tempHLG
        if tempHUG-1 > tempHLG :
            tempHUG = tempHUG - 1
        text2=str(tempHUG)+"%"
        NUG = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=480,y=215)
        return tempHUG

    def HLGU():
        global tempHLG
        global tempHUG
        if tempHUG > tempHLG+1:
            tempHLG = tempHLG + 1
        text2=str(tempHLG)+"%"
        NLG = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=265,y=215)
        return tempHLG

    def HLGD():
        global tempHLG
        global tempHLY
        if tempHLG > tempHLY+1:
            tempHLG = tempHLG - 1
        text2=str(tempHLG)+"%"
        NLG = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=265,y=215)
        return tempHLG

    def HUYU():
        global tempHUY
        tempHUY = tempHUY + 1
        text2 =str(tempHUY)+"%"
        NUY = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=670,y=215)
        return tempHUY

    def HUYD():
        global tempHUY
        global tempHUG
        if tempHUY > tempHUG +1:
            tempHUY = tempHUY - 1
        text2 =str(tempHUY)+"%"
        NUY = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=670,y=215)
        return tempHUY

    def HLYU():
        global tempHLY
        global tempHLG
        if tempHLY<tempHLG-1:
            tempHLY = tempHLY + 1
        text2=str(tempHLY)+"%"
        NLY = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=65,y=215)
        return tempHLY

    def HLYD():
        global tempHLY
        tempHLY = tempHLY - 1
        text2=str(tempHLY)+"%"
        NLY = Label(sus,text =text2,font=("Segoe UI", 22), bg='black', fg='white').place(in_=sus,x=65,y=215)
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

    #Window Title
    Label(sus,text ='HUMIDITY RANGE SETTINGS',font=("Segoe UI", 24,"bold"),bg='black',fg='white').place(in_=sus,x=150,y=25)

    #Limit Titles
    Label(sus,text ="Upper",bg='black',fg='white',font=("Segoe UI", 22)).place(in_=sus,x=470,y=160)
    NUG = Label(sus,text =str(tempHUG)+"%",bg='black',fg='white',font=("Segoe UI", 22)).place(in_=sus,x=480,y=215)

    Label(sus,text ="Lower",bg='black',fg='white',font=("Segoe UI", 22)).place(in_=sus,x=255,y=160)
    NLG = Label(sus,text =str(tempHLG)+"%",bg='black',fg='white',font=("Segoe UI", 22)).place(in_=sus,x=265,y=215)

    Label(sus,text ="Upper",bg='black',fg='white',font=("Segoe UI", 22)).place(in_=sus,x=660,y=160)
    NUY = Label(sus,text =str(tempHUY)+"%",bg='black',fg='white',font=("Segoe UI", 22)).place(in_=sus,x=670,y=215)

    Label(sus,text ="Lower",bg='black',fg='white',font=("Segoe UI", 22)).place(in_=sus,x=55,y=160)
    NLY = Label(sus,text =str(tempHLY)+"%",bg='black',fg='white',font=("Segoe UI", 22)).place(in_=sus,x=65,y=215)
    
    #Up/Down buttons
    up_button1 = tk.Button(sus,bg = '#ffcc00', text = "↑",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=HLYU).place(in_=sus,x=70,y=275)
    down_button1 = tk.Button(sus,bg = '#ffcc00', text = "↓",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=HLYD).place(in_=sus,x=70,y=350)

    up_button2 = tk.Button(sus,bg = '#12c702', text = "↑",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=HLGU).place(in_=sus,x=268,y=275)
    down_button2 = tk.Button(sus,bg = '#12c702', text = "↓",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=HLGD).place(in_=sus,x=268,y=350)

    up_button1 = tk.Button(sus,bg = '#12c702', text = "↑",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=HUGU).place(in_=sus,x=485,y=275)
    down_button1 = tk.Button(sus,bg = '#12c702', text = "↓",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=HUGD).place(in_=sus,x=485,y=350)

    up_button2 = tk.Button(sus,bg = '#ffcc00', text = "↑",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=HUYU).place(in_=sus,x=675,y=275)
    down_button2 = tk.Button(sus,bg = '#ffcc00', text = "↓",fg="black",borderwidth=3, highlightcolor="white",relief="solid",font=("Segoe UI", 22),
                            command=HUYD).place(in_=sus,x=675,y=350)
    
    exit = tk.Button(sus, text = "Exit",font=("Segoe UI", 18),width = 10,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black",
                        command=SaveHum).place(in_=sus,x=300,y=85)
    
    # Exit = tk.Button(sus, text = "Exit Withoug Saving",command=nonSaveHum).place(in_=sus,x=500,y=750)

#--------------------------------------------Report Button------------------------------------------#
def Reports():
    # Toplevel object which will  
    # be treated as a new window 
    sus = Toplevel() 
    # sets the title of the 
    # Toplevel widget 
    sus.overrideredirect(True)  
    sus.configure(bg='black')
    # sets the geometry of toplevel 
    sus.geometry("241x285") 
    
    #win.config(cursor="none")
    
    Label(sus,text ='REPORTS', font=("Segoe UI", 20,"bold"), bg='black', fg='white').place(in_=sus,x=50,y=10)
    
    current_report_button = tk.Button(sus, text="Current Report",width = 16,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 14),
                        command=Report)
    current_report_button.place(x=10,y=115)

    thingspeak_button = tk.Button(sus, text="ThingSpeak",   width = 16, fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 14),
                        command=ThingSpeak)
    thingspeak_button.place(x=10,y=65)
    
    sendall_button = tk.Button(sus, text="All Reports", width = 16,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 14),
                        command=SendReport)
    sendall_button.place(x=10,y=165)
    
    def ExitWin():
        sus.destroy()
        
    tk.Button(sus, text = "Exit",width = 16,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 14),
                        command=ExitWin).place(in_=sus,x=10,y=210)

report_button = tk.Button(win, text="Report",fg="white",borderwidth=3, width=7,highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 13, 'bold'),
                        command=Reports)
report_button.pack()
report_button.place(x=125,y=0)

is_on = True

#--------------------------------------------Settings Button--------------------------------------------#
def Settings():
    # Toplevel object which will  
    # be treated as a new window 
    sus = Toplevel() 
    
    # sets the title of the 
    # Toplevel widget 
    sus.overrideredirect(True) 
    #win.config(cursor="none")
    sus.configure(bg='black')
    
    # sets the geometry of toplevel 
    sus.geometry("241x285")
    
    def switch():
        global is_on
        
        # Determin is on or off
        if is_on:
            
            notification_button.config(text = "Email Notifications off", 
                            fg = "white", bg='#DC143C')
            is_on = False
            tk.messagebox.showinfo("Email Notification", "Email Notificaion is now Off")
        else:
            
            notification_button.config(text = "Email Notifications On", fg = "white", bg='#397D02')
            is_on = True
            tk.messagebox.showinfo("Email Notification", "Email notificaion is now on")
            
    Label(sus,text ='SETTINGS', font=("Segoe UI", 20,"bold"), bg='black', fg='white').place(in_=sus,x=50,y=10)
    
    offset_button = tk.Button(sus, text="Offset",  width = 16,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 14),
                            command=settings0)
    offset_button.place(x=10,y=60)
    
    temp_button = tk.Button(sus,text="Temp Range Adjust",width = 16,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 14),
                            command=settings1)
    temp_button.place(x=10,y=105)

    humid_button = tk.Button(sus, text="Humid Range Adjust",  width = 16,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 14),
                            command=settings2)
    humid_button.place(x=10,y=150)
    
    if is_on:
        notification_button = tk.Button(sus, text="Email Notification On",  width = 16,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="#397D02", font=("Segoe UI", 14),
                                command=switch)
        notification_button.place(x=10,y=195)
    else:
        notification_button = tk.Button(sus, text="Email Notification Off",  width = 16,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="#DC143C", font=("Segoe UI", 14),
                            command=switch)
        notification_button.place(x=10,y=195)
    def ExitWin():
        sus.destroy()
        
    tk.Button(sus, text = "Exit",width = 16,fg="white",borderwidth=3, highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 14),
                            command=ExitWin).place(in_=sus,x=10,y=240)

settings_button = tk.Button(win, text="Settings",fg="white",borderwidth=3, width=7,highlightcolor="white",relief="solid",bg="black", font=("Segoe UI", 13, 'bold'), 
                            command=Settings)
settings_button.pack()
settings_button.place(x=0,y=0)


#---------------------------------------End of buttons-------------------------------------------------#

#------------------------------------------Clock-------------------------------------------------------#
class Clock:
    def __init__(self):
        self.time1 = ''
        self.time2 = time.strftime('%d-%m-%y %H:%M:%S:%p:%Z')

        self.mFrame = Frame()
        self.mFrame.pack(expand=YES,fill=X)
        self.mFrame.place(x=520, y=0)
        self.watch = Label(self.mFrame, text=self.time2, font=('Segoe UI',14 ),background='black', fg="white")

        self.watch.pack()
        
        self.changeLabel() #first we call it manually

    def changeLabel(self): 
        self.time2 = time.strftime('%Y-%m-%d %H:%M:%S:%p:%Z')
        self.watch.configure(text=self.time2)
        self.mFrame.after(200, self.changeLabel) #it will call itself continuously
Clock()
#-----------------------------------------End Clock-----------------------------------------------------#
#________________________________________________________________________________________________________
#-------------------------------------Tkinter window options--------------------------------------------# 

canv = FigureCanvasTkAgg(fig, master = win)
canv._tkcanvas.pack(side=tk.BOTTOM)
canv.draw()

get_widz = canv.get_tk_widget()
get_widz.pack()

def exit_(event):                                    #Exit fullscreen
    win.quit() 

win.attributes("-fullscreen",True)             #Fullscreen when executed 
win.bind('<Escape>',exit_)                      #ESC to exit

#----------------------------------------End Of GUI-----------------------------------------------------#
#________________________________________________________________________________________________________



#________________________________________________________________________________________________________
#-----------------------------------------Creating Threads---------=------------------------------------#
# Creates threads and starts all functions as needed
try:
    os.chdir('/home/pi/LabWatchGUI6')    
    read_file()
    _thread.start_new_thread( sensor0, ("sensor_1", 2, ) )#starts recording sensor on D4
    _thread.start_new_thread( sensor1, ("sensor_2", 2, ) )#starts recording sensor on D18
    _thread.start_new_thread( avg,     ("average" , 4, ) )
    _thread.start_new_thread( cloud,   ("upload"  , 300, ) )
    _thread.start_new_thread( email,   ("Warning" , 45, ) )
    _thread.start_new_thread( alert,   (            45, ) )

    ani = animation.FuncAnimation(fig, animate, interval=2000, fargs=(xs,ys,xs2,ys2) )

except:
    print ("Error: unable to start thread")

#-------------------------------------End of Starting Threads--------------------------------------------#
#_________________________________________________________________________________________________________

#_________________________________________________________________________________________________________
#------------------------------------Main loop for the program-------------------------------------------# 

#Tkinter Window Backgorund color
win.configure(background='black')
#win.config(cursor="none")

    
try:
    # Window
    splash_screen= Toplevel()
    splash_screen.overrideredirect(True) 
    splash_screen.geometry("800x600")
    splash_screen.configure(bg='black')

    #background image
    bg = PhotoImage(file = "LabWatchLogo.PNG")
    background=Label(splash_screen, image=bg)
    background.place(x=220,y=70)  

    #Splash screen timer and close
    splash_screen.after(6000,lambda: splash_screen.destroy())

    win.mainloop()
except:
    subprocess.run('~/LabWatchGUI6/runme.sh', shell=True)
    quit()
finally:
    pass
#----------------------------------------End of Main Loop------------------------------------------------#

#----------------------------------------End of code ----------------------------------------------------#
#_________________________________________________________________________________________________________