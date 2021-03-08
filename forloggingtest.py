# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import os
import sys
import time
import board
import adafruit_dht
from urllib.request import urlopen
from datetime import datetime
# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)
# Enter Your API key here
myAPI = '1Y9PTSUDVZ7QOACU' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

 
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

filename=datetime.date(datetime.now())

while True:
    try:
        # Print the values to the serial port
        f= open(filename.strftime("%d %B %Y")+".txt", "a") 
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        f.write("Temp: {:.1f} F / {:.1f} C    Humidity: {}%\n ".format(temperature_f, temperature_c, humidity))
        f.close()
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        conn = urlopen(baseURL + '&field1=%s&field2=%s' % (temperature_c, humidity))
        print (conn.read())
        conn.close()

 
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(5)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
 
    time.sleep(5)