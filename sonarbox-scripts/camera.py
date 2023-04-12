#!/usr/bin/python3
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time

timestr = time.strftime("%Y%m%d-%H%M")

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

GPIO.output(4, GPIO.HIGH)

picam2 = Picamera2()
time.sleep(2) # seconds
picam2.start_and_capture_file("/home/pi/Desktop/timelapse/"+timestr+".jpg",delay=0,show_preview=False)

GPIO.output(4, GPIO.LOW)
