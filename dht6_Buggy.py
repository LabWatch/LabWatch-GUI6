
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import *           #Tkinter Library/ install Tkinter - Python 3. sudo apt-get install python3-tk
import tkinter as tk            #Tkinter Library
import threading                #For running mulitple threads(task,fucntion calls) 
import tkinter.font             #Tkinter font library
import adafruit_dht             #DHT22 temp/hum sensor library
import time                     #Timing
import board                    #RPi4 board pins schematic(D4 pin must be active for DHT22 sensor)
import random
import webbrowser
import csv
import os
from time import sleep
from datetime import datetime
from urllib.request import urlopen 
import gaugelib

#Temperature and Humidity Data input/output
aDHTDevice = adafruit_dht.DHT22(board.D4)
temp = aDHTDevice.temperature 
hum = aDHTDevice.humidity 

#ThingSpeak credentrials 
myAPI = 'RXXLLQDW8BV1S7WW' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

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

#animate() function
def animate(i, xs, xs2, ys, ys2):
    #file = open("/home/pi/data_log.csv", "a")
    #if os.stat("/home/pi/data_log.csv").st_size == 0:
        #file.write("Time,Temperature °C,Humidity\n")

    while True:
        try:
            #temp and Hum data 
            temp = aDHTDevice.temperature
            hum = aDHTDevice.humidity
            #temperature.set(str(temp)+"°C")  
            #humidity.set(str(hum)+"%" )
            
            p1.set_value(float(temp))
            p2.set_value(float(hum))
            
            conn = urlopen(baseURL + '&field1=%s&field2=%s' % (temp, hum))
            conn.close()
            
            #now = datetime.now()
            #file.write(str(now)+","+str(temp)+","+str(hum)+"\n")
            #file.flush()

            #Ignore errors, wait for real value and keep going
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(1.0)
            continue
        except Exception as error:
            aDHTDevice.exit()
            raise error
        break 

    # Add y to list
    ys.append(temp)
    ys2.append(hum)

    # Limit y list to set number of items
    ys = ys[-x_len:]
    ys2 = ys2[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)
    line2.set_ydata(ys2)
    return line,
    return line2,
#End of animate() function and live plot update
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
#Buttons
def reportSummary():

    file = open("/home/pi/data_log.csv", "a")


button = Label(win, text="ReportSummary", fg="blue", cursor="hand2",font=('times',12, 'bold' ))
button.bind("<Button-1>",lambda e: reportSummary('/home/pi/data_log.csv'))
button.pack()
button.place(x=90, y=0)

def thingSpeak(url):
    webbrowser.open_new(url)

button = Label(win, text="ThingSpeak", fg="blue", cursor="hand2",font=('times',12, 'bold' ))
button.bind("<Button-1>",lambda e: thingSpeak("https://thingspeak.com/channels/1311268"))
button.pack()
button.place(x=0, y=0)
#End of buttons

#Clock 
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

timedisplay = Clock()
#End clock 

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
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys,xs2,ys2), interval=1000)

#Warnings background color change
if temp<10.0:
    
    win.configure(background='#FF0000')

else:
    win.configure(background='#DcDcDc')
    
win.mainloop()
#End of Code
