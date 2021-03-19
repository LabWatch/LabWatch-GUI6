#thingspeak
import settings

import time 

#thingspeak imports 
from urllib.request import urlopen 

#ThingSpeak credentrials 
#myAPI = '4M4MSZ8ZYP18AU3E' 
# URL where we will send the data, Don't change it
#baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 



def cloud(delay):   
    #getting api key from settings script
    myAPI = settings.api
    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    
    while True:
        try:
            conn = urlopen(baseURL + '&field1=%s&field2=%s' % (settings.data[0], settings.data[1]))
            conn.close()
            # print("data sent")
        except:
            print("Connection Failed")
        time.sleep(delay)

