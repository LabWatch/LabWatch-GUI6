#importing all functions
from email_sending import sendfile, sendwarning
import settings
import Sensor_Read
import thingspeak
import Local_logging

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

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

ax2 = fig.add_subplot(1,2,2)
xs2 = []
ys2 = [] 

ax2.tick_params(axis='x', colors='white')
ax2.tick_params(axis='y', colors='white')


temp_colour = "#000000"
humid_colour = "#000000"
#_______________________________________________________________________________________________________________________________
#-----------------------------------GUI to local User Code-----------------------------------------------------------------------


#------------------------p-----Digital readings for GUI----------------------------------------------------#

temperature = StringVar()                       #is a class that provides helper functions for directly creating and accessing such variables in that interpreter.
temperature.set("----"+ "°C")	                #Temperature set to store multiple items in a single variable	

humidity = StringVar()
humidity.set("----"+" %")		                #Humidity set to store multiple items in a single variable	

temperatureLabel = Label(win, fg=temp_colour, background="black", textvariable=temperature, font=("Segoe UI", 60,"bold")) #bg color,font and font size
temperatureLabel.place(x=70, y=130)             #Character "----C" placement and attributes

humidityLabel = Label(win, fg=humid_colour, background="black", textvariable=humidity, font=("Segoe UI", 60,"bold"))       #bg color,font and font size
humidityLabel.place(x=485, y=130)              #Character "----%" placement and attributes
#----------------------------------------End-----------------------------------------------------------# 


#-------------------------------------------Animate function ------------------------------------------#
def animate(i, xs, xs2, ys, ys2):
        
    #Send variables from temp to StringVar for temperatur.set above in---->Digital readings for GUI
    temperature.set(str(settings.data[0])+"°C")            
    #Send variables from hum to StringVar for temperatur.set above in---->Digital readings for GUI
    humidity.set(str(settings.data[1])+"%" )        

    #Live Plotting
    #---------------------Temperature Plot ------------------#
    #Append sensor reading data
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(settings.data[0])

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
    ys2.append(settings.data[1])

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
    
    #------------------Digital readings colors---------------#
    # try:
    
    if settings.temp_bounds[1] <= settings.data[0] <= settings.temp_bounds[2] : 
        temp_colour = "#12c702"
    elif  settings.temp_bounds[0] <= settings.data[0] <= settings.temp_bounds[3] :
        temp_colour = "#ffcc00"
    else: 
        temp_colour = "#ff0000"

    if settings.humid_bounds[1] <= settings.data[1] <= settings.humid_bounds[2] : 
        humid_colour = "#12c702"
    elif  settings.humid_bounds[0] <= settings.data[1] <= settings.humid_bounds[3]:
        humid_colour = "#ffcc00"
    else: 
        humid_colour = "#ff0000"
    # except:
    #     humid_colour = "#12c702"
    #     temp_colour = "#12c702"

    temperatureLabel.config(fg = temp_colour)
    humidityLabel.config(fg = humid_colour)
    win.update()
#--------------------------------End-------------------------------------------------#

#--------------------------------Buttons---------------------------------------------------------#

def Report():

    filedialog.askopenfile(parent=win,
                                    filetypes = (("Text files", "*.txt"), ("All files", "*")))

def ThingSpeak():
    webbrowser.open_new(settings.link)

report_button = tk.Button(win, text="Report", command=Report)
report_button.pack()
report_button.place(x=100,y=0)

thingspeak_button = tk.Button(win, text="ThingSpeak", command=ThingSpeak)
thingspeak_button.pack()
thingspeak_button.place(x=0,y=0)

#----------------------------End--------------------------------------#

#----------------------------------Clock-----------------------------------------------------------------#
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

#-------------------------------End clock---------------------------------# 

canv = FigureCanvasTkAgg(fig, master = win)
canv._tkcanvas.pack(side=tk.BOTTOM)
canv.draw()

get_widz = canv.get_tk_widget()
get_widz.pack()

def exit_(event):                                    #Exit fullscreen
    win.quit() 

win.attributes("-fullscreen",True)             #Fullscreen when executed 
win.bind('<Escape>',exit_)                      #ESC to exit

#---------------------------------End Of GUI ------------------------------------------------------------------------
#____________________________________________________________________________________________________________________




try: 
    settings.init()
    _thread.start_new_thread( Sensor_Read.sensor0, (0,2 ) )#starts recording sensor on D4
    _thread.start_new_thread( Sensor_Read.sensor1, (1,2 ) )#starts recording sensor on D18
    _thread.start_new_thread( Sensor_Read.avg,     (2, ) )
    _thread.start_new_thread( thingspeak.cloud,    (300, ) )
    _thread.start_new_thread( Local_logging.local,       (300, ) )
    
    ani = animation.FuncAnimation(fig, animate, interval=2000, fargs=(xs,ys,xs2,ys2) )
    win.configure(background='black')

except:
    print ("Error: unable to start thread")

#-----------------------------End of Starting Threads----------------------------------------------------
#_________________________________________________________________________________________________________

#______________________________________________________________________________________________
#-------------------main loop for the programe------------------------------------------------- 

#Tkinter window backgorund color
# while True: 
try:
    
    win.mainloop()
    
except:
    subprocess.run('~/LabWatchGUI6/runme.sh', shell=True)
    quit()
finally:
    pass


