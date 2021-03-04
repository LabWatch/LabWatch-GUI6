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

        
        # prints to terminal for error checking 
        print(
                "Temp_avg:  {:.1f} C    Humidity_avg: {:.1f}%   sensor0: {}   Sensor1: {} ".format(
                    temp_avg, humid_avg,sensor_fault0,sensor_fault1
                )
            ) 
        time.sleep(delay)#sleeps for set delay time 




# 
#-----------------------------------End of sensor Data read and error Check------------------------------------------------------------------------
#______________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________

#Thingspeak Function Validation
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
#__________________________________________________________________________________________________________________
#GUI to local User Code















#---------------------------------End Of GUI -------------------------------------------------------------------------------
#____________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________



#_____________________________Creating Threads___________________________________________________________
# Create two threads as follows
try:
    _thread.start_new_thread( sensor0, ("sensor_1", 2, ) )#starts recording sensor on D4
    _thread.start_new_thread( sensor1, ("sensor_2", 2, ) )#starts recording sensor on D18
    _thread.start_new_thread( avg,     ("average" , 4, ) )
    _thread.start_new_thread( cloud,   ("upload"  , 10, ) )
except:
    print ("Error: unable to start thread")

#-----------------------------End of Starting Threads----------------------------------------------------
#_________________________________________________________________________________________________________








#_______________________main loop for the programe____________________________________________ 
while 1:#True loop to run code forever 
    
    #keeps threads running in background           
    pass 
#-------------------------End of Main Loop-----------------------------------------------------
#_______________________________________________________________________________________________

#end of code 
