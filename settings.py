#settings.py 
import board
import adafruit_dht
 
from array import *

def init():
    global emailto
    global sensor_data 
    global data
    global api
    global link
    global temp_bounds
    global humid_bounds
    #thingspeak keys
    
    api = '4M4MSZ8ZYP18AU3E' 
    link = "https://thingspeak.com/channels/1318645"

    #Who the email is sent too 
    emailto = "saltydick61@gmail.com"
    

    sensor_data = [[0, 0, 0], [0, 0, 0]]
    
    data = [0, 0]
    

    #setting up limits 
    temp_bounds = [17,19,22,25]
    humid_bounds = [32,36,42,46]
    
    

    