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

#System Restart 
import subprocess

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
from tkinter import messagebox
from tkinter import filedialog
#import for email
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart  # New line
from email.mime.base import MIMEBase  # New line
from email import encoders  # New line

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

#file timer
filetimer = datetime.now()

#-----------------------------------------------------------------
#----------------ThingSpeak Global Variables----------------------
#ThingSpeak credentrials 
myAPI = '4M4MSZ8ZYP18AU3E' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

# temp limit for warning display and email sending
lowerlimit=10
upperlimit=25

#-------------------------------------------------------------------
#-------------------Tkinter Variables-----------------------------------------
#Tkinter window
win = tk.Tk()

#Live update plot of temp and humidity

#Parameters
x_len = 200         # Number of points to display
y_range = [10, 40]  # Range of possible Y values to display
y_rangehumid = [20, 80] # Range of possible Y values to display for HUMIDITY

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
ax2.set_ylim(y_rangehumid)

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
    global filetimer
    while True:
        try:
            timenow = datetime.now()
            yrnow = filetimer.year
            monow = filetimer.month
            daynow = filetimer.day

            file = open("/home/pi/data_log.csv", "a")
            if os.stat("/home/pi/data_log.csv").st_size == 0:
                file.write("File date: " + "," + str(yrnow) + "," + str(monow) + "," + str(daynow)+"\n")
                file.write("Time,S1TempC,S1Humid,S2TempC,S2Humid,\n")

            file.write(str(timenow.strftime("%m/%d/%Y %H:%M:%S"))+","+str(temp0)+","+str(humid0)+","+str(temp1)+","+str(humid1)+"\n")
            file.flush()
            file.close()

            file = open("/home/pi/data_log.csv", "r")
            data=list(csv.reader(file))
            infiletimer = int(data[0][3])
            file.close()

            if timenow.day > infiletimer:
                # check if directory exists
                if not os.path.exists("/home/pi/{}/".format(
                    filetimer.year)
                ):
                    # make directory if not exist
                    os.makedirs("/home/pi/{}/".format(
                        filetimer.year)
                    )
                # move file to according folder
                os.rename("/home/pi/data_log.csv","/home/pi/{}/.csv".format(
                        filetimer.year
                    )
                )
                filetimer = datetime.now()
        except:
            print("Logging Failed")
        time.sleep(delay)

#-------------------------------------End of Local Logging ---------------------------------------------------------------------------
#____________________________________________________________________________________________________________________


#-------------------------------------Start of Emailing ---------------------------------------------------------------------------
def email(threadName, delay):
    global temp_avg
    global upperlimit
    global lowerlimit
    while True:
        if(temp_avg>upperlimit or temp_avg<upperlimit):
            sender_email = 'laose152@gmail.com' #dump email, gmail only and remember to turn on less secure app access on setting
            sender_name = 'LAB WATCH'
            password = 'Xx1387011247'
            receiver_email = 'laose152@gmail.com'
            receiver_name = 'Rob'
            # Email text
            email_body = '''
                Hi the lab room temp is unusual 
            '''
            filename = '/home/pi/Desktop/LabWatchGUI6-Master/test.pdf' # for testing change it to the path of the file u want to send
            print("Sending the email...")
            # Configurating user's info
            msg = MIMEMultipart()
            msg['To'] = formataddr((receiver_name, receiver_email))
            msg['From'] = formataddr((sender_name, sender_email))
            msg['Subject'] = 'Hello, my friend ' + receiver_name
            msg.attach(MIMEText(email_body, 'plain')
            try:
                    # Open PDF file in binary mode
                    with open(filename, "rb") as attachment:
                                    part = MIMEBase("application", "octet-stream")
                                    part.set_payload(attachment.read())

                    # Encode file in ASCII characters to send by email
                    encoders.encode_base64(part)

                    # Add header as key/value pair to attachment part
                    part.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {filename}",
                    )

                    msg.attach(part)
            except Exception as e:
                    print(f'Oh no! We didn't found the attachment!n{e}')
                    break                       
            try:
                    # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    # Encrypts the email
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                    # We log in into our Google account
                    server.login(sender_email, password)
                    # Sending email from sender, to receiver with the email body
                    server.sendmail(sender_email, receiver_email, msg.as_string())
                    print('Email sent!')
            except Exception as e:
                    print(f'Oh no! Something bad happened!n {e}')
            finally:
                    print('Closing the server...')
                    server.quit()
            time.sleep(delay)
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
    max_value=70.0,
    min_value=10.0,
    size=250,
    bg_col='#DCDCDC',
    unit = "Humidity %",bg_sel = 2)

p1.pack()
p1.place(x=100, y=50)
p2.pack()
p2.place(x=500, y=50)

#--------------------Buttons---------------------------------
def Report():
    return filedialog.askopenfile()

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
        self.watch = Label(self.mFrame, text=self.time2, font=('times',14, 'bold' ),background='#DcDcDc', fg="black")

        self.watch.pack()
        
        self.changeLabel() #first call it manually

    def changeLabel(self): 
        self.time2 = time.strftime('%Y-%m-%d %H:%M:%S:%p:%Z')
        self.watch.configure(text=self.time2)
        self.mFrame.after(200, self.changeLabel) #it'll call itself continuously

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
    _thread.start_new_thread( sensor0, ("sensor_1", 2, ) )#starts recording sensor on D4
    _thread.start_new_thread( sensor1, ("sensor_2", 2, ) )#starts recording sensor on D18
    _thread.start_new_thread( avg,     ("average" , 4, ) )
    _thread.start_new_thread( cloud,   ("upload"  , 10, ) )
    _thread.start_new_thread( local,   ("local"  , 300, ) )
    _thread.start_new_thread( email,   ("email"  , 300, ) )
    ani = animation.FuncAnimation(fig, animate, interval=1000, fargs=(xs, ys,xs2,ys2) )
    
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
