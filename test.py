#!/usr/bin/python3

#importing threading
import _thread
#import Time 
import time

#importing for the AdaFruit Board
import board
import adafruit_dht

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

def sensor1( threadName, delay):
    global temp1
    global humid1
    global sensor_fault1
    global temp_avg
    fault = bool(0)
    while True:
        for x in range(5):
            try:
                # Print the values to the serial port
                temperature_c = dhtDevice1.temperature
                humidity = dhtDevice1.humidity
                if (abs(temp_avg - temperature_c ) < 4):
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

        temp1 = temperature_c
        humid1 = humidity
        sensor_fault1 = fault
        time.sleep(delay)        

def avg(threadName, delay):
    global temp_avg
    global humid_avg
    global temp_last_avg
    global humid_last_avg
    global temp0
    global humid0
    global temp1
    global humid1
    global sensor_fault0
    global sensor_fault1
    
    while True:
        temp_last_avg = temp_avg
        humid_last_avg = humid_avg

        if (sensor_fault0 == False and sensor_fault1 == False) :
            tempdiff = abs(temp0-temp1)
            humiddiff = abs(humid0-humid1)

            if (tempdiff < 4 and humiddiff < 10) :
                temp_avg = (temp0 + temp1) / 2
                humid_avg = (humid0 + humid1) / 2

        elif (sensor_fault0 == False and sensor_fault1 == True) :
            temp_avg = (temp0 + temp_last_avg) / 2
            humid_avg = (humid0 + humid_last_avg) / 2

        elif (sensor_fault0 == True and sensor_fault1 == False): 
            temp_avg = (temp1 + temp_last_avg) / 2
            humid_avg = (humid1 + humid_last_avg) / 2 
        else: 
            temp_avg = 0
            humid_avg = 0

        print(
                "Temp_avg:  {:.1f} C    Humidity_avg: {}%   sensor0: {}   Sensor1: {} ".format(
                    temp_avg, humid_avg,sensor_fault0,sensor_fault1
                )
            ) 
        time.sleep(delay)




# Create two threads as follows
try:
    _thread.start_new_thread( sensor0, ("sensor_1", 2, ) )#starts recording sensor on D4
    _thread.start_new_thread( sensor1, ("sensor_2", 2, ) )#starts recording sensor on D18
    _thread.start_new_thread( avg,     ("average" , 4, ) )
except:
    print ("Error: unable to start thread")







#main loop for the programe 
while 1:

    # print(
    #         "Sensor_0 Temp:  {:.1f} C    Humidity: {}%  sensor Fault: {}".format(
    #             temp0, humid0,sensor_fault0
    #         )
    #     )
    # print(
    #         "Sensor_1 Temp:  {:.1f} C    Humidity: {}%  sensor Fault: {}".format(
    #             temp1, humid1,sensor_fault1
    #         )
    #     )  
        
        
    #time.sleep(6.0)           
    pass