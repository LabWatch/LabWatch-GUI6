#importing data for the AdaFruit GPIO Board (RPI4)
import board
import adafruit_dht

import settings

#import Time 
import time

dhtDevice0 = adafruit_dht.DHT22(board.D4)
dhtDevice1 = adafruit_dht.DHT22(board.D18)




def sensor0(index, delay):
    fault = 1 
    while True:
        for x in range(5):
            try:
                # Print the values to the serial port
                temperature_c = dhtDevice0.temperature
                humidity = dhtDevice0.humidity
                
                if (abs(settings.sensor_data[index][0] - temperature_c ) < 4):
                    fault = 1
                break            
            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                time.sleep(delay)
                
            except Exception as error:
                dhtDevice0.exit()
                raise error
            if (x > 3):
                fault = 0
                temperature_c = 0
                humidity = 0 
                break
        settings.sensor_data[index][0] = temperature_c
        settings.sensor_data[index][1] = humidity
        settings.sensor_data[index][2] = fault
        # print("Sensor 1: {}".format(settings.sensor_data[index][0]))
        time.sleep(delay)

def sensor1(index, delay):
    fault = 1 
    while True:
        for x in range(5):
            try:
                # Print the values to the serial port
                temperature_c = dhtDevice1.temperature
                humidity = dhtDevice1.humidity
                
                if (abs(settings.sensor_data[index][0] - temperature_c ) < 4):
                    fault = 1
                break            
            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                time.sleep(delay)
                
            except Exception as error:
                dhtDevice0.exit()
                raise error
            if (x > 3):
                fault = 0
                temperature_c = 0
                humidity = 0 
                break
        settings.sensor_data[index][0] = temperature_c
        settings.sensor_data[index][1] = humidity
        settings.sensor_data[index][2] = fault
        # print("Sensor 2: {}".format(settings.sensor_data[index][0]))
        time.sleep(delay)



# to calculate the avg and error check between two sensors 
def avg(delay):
    
    while True: #runs the avg loop forever 
        
        temp_last_avg = settings.data[0] #stores current avgerage as last avg 
        humid_last_avg = settings.data[1]

        # mutltiple statments checking different sinarios for faulty sensor 
        if (settings.sensor_data[0][2] == 1 and settings.sensor_data[1][2] == 1) :#both good
            tempdiff = abs(settings.sensor_data[0][0]-settings.sensor_data[1][0])
            humiddiff = abs(settings.sensor_data[0][1]-settings.sensor_data[1][1])

            if (tempdiff < 4 and humiddiff < 10) :# they are roughly the same value 
                settings.data[0] = (settings.sensor_data[0][0]+settings.sensor_data[1][0] + temp_last_avg) / 3
                settings.data[1] = (settings.sensor_data[0][1]+settings.sensor_data[1][1] + humid_last_avg) / 3


        elif (settings.sensor_data[0][2] == 1 and settings.sensor_data[1][2] == 0) :#D4 OK D18 Bad
            settings.data[0] = (settings.sensor_data[0][0]+ temp_last_avg) / 2
            settings.data[1] = (settings.sensor_data[0][1]+ humid_last_avg) / 2

        elif (settings.sensor_data[0][2] == 0 and settings.sensor_data[1][2] == 1): #D4 Bad D18 OK
            settings.data[0] = (settings.sensor_data[1][0]+ temp_last_avg) / 2
            settings.data[1] = (settings.sensor_data[1][1]+ humid_last_avg) / 2
            
        else: #both Bad set to 0 , 0 
            settings.data[0] = 0
            settings.data[1] = 0
            

        settings.data[0] = round(settings.data[0],1)
        settings.data[1] = round(settings.data[1],1)
        # print("avg temp {} avg himid {}".format(settings.data[0], settings.data[1]))
        # # prints to terminal for error checking 
        # print(
        #         "Temp_avg:  {:.1f} C    Humidity_avg: {:.1f}%   sensor0: {}   Sensor1: {} ".format(
        #             temp_avg, humid_avg,sensor_fault0,sensor_fault1
        #         )
        #     ) 
        time.sleep(delay)#sleeps for set delay time 
