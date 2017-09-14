#!/usr/bin/python
#--------------------------------------


# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4y
# 12: Button Input
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND


###IMPORTS###
import RPi.GPIO as GPIO
import time
import os
from picamera import PiCamera
from time import sleep
from gps import *
#import gps
import threading

import numpy as np
## import matplotlib.pyplot as plt
import Adafruit_DHT as dht

###GPIO SETUP###
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)

###Start Camera###
camera = PiCamera()
#camera.start_preview()

###Set Global Variable###
os.system('sudo gpsd /dev/serial0 -F /var/run/gpsd.sock')
gpsd = None
#os.system('clear')

###GPS Class###
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd
    gpsd = gps(mode=WATCH_ENABLE)
    self.current_value = None
    self.running=True

  def run(self):
    global gpsd
    while self.running: #gpsp
      gpsd.next()
##session = gps.gps()

###Get Temperature Data###
##def temp_raw():
##    f = open(temp_sensor, 'r')
##    lines = f.readlines()
##    f.close()
##    return lines
##
##def read_temp():
##    lines = temp_raw()
##    while lines[0].strip()[-3:] != 'YES':
##        time.sleep(0.2)
##        lines = temp_raw()
##    temp_output = lines[1].find('t=')
##
##    if temp_output != -1:
##        temp_string = lines[1].strip()[temp_output+2:]
##        temp_c = float(temp_string)/1000.0
##        temp_f = temp_c * 9.0/5.0 +32.00
##        return temp_c 

#tempData = []

###Temperature Sensor Init###
##os.system('modprobe.w1.gpio')
##os.system('modprobe.w1-therm')
##
##temp_sensor = ('/sys/bus/w1/devices/28-0000071d2761/w1_slave')

###Output File Init###
tempFile = open('/home/pi/Desktop/data/temp.txt','w')
timeFile = open('/home/pi/Desktop/data/time.txt','w')
gpsFile = open('/home/pi/Desktop/data/gps.txt','w')
humFile = open('/home/pi/Desktop/data/hum.txt','w')



###DATA COLLECTION LOOP###
def collectData():

    gpsp = GpsPoller()
    #gpsd = None
    gpsp.start()
    #os.system('clear')
    print("Data collection start")
    ##session.query('admosy')
    for i in range(0,100): # Data collection loop happens(every ~8.5 seconds)
        print("----------------")
        time.sleep(1)
        h,currTemp = dht.read_retry(dht.DHT22, 20)
        print("Temp: "+str(currTemp))
        print("Hum: "+str(h))
        tempFile.write(str(currTemp)+"\n") # Write temp to file
        timeFile.write(str(time.ctime())+"\n") # Write time to file
        print("Time: "+time.ctime())
        gpsFile.write(str(gpsd.fix.latitude) + " " + str(gpsd.fix.longitude)+ " " + str(gpsd.fix.altitude) +"\n") # Write gps data to file
        print(str(gpsd.fix.latitude) + " " + str(gpsd.fix.longitude) + " " + str(gpsd.fix.altitude))
        camera.capture(str(time.ctime()+".jpg")) # Take picture
        humFile.write(str(h)+"\n")        
        

        time.sleep(1)

    # Close files
    print("Closing files...")
    tempFile.close()
    timeFile.close()
    gpsFile.close()
    humFile.close()
    print("Done")
    os._exit(0)
    return



###Main Program Block###

print("Ready to collect data. Press button to start.")
while True:
    input_state = GPIO.input(12)
    if input_state == False:
        print('Button Pressed')
        time.sleep(0.2)
        collectData()
        time.sleep(20)
