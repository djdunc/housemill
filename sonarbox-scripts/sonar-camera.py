#!/usr/bin/python3
from picamera2 import Picamera2
import RPi.GPIO as GPIO # used to turn IR leds on and off
import time
import serial
import statistics

# run as crontab every odd minute so that it runs separately
# to the sonar job - cron: 1-59/2 * * * *

# Initialize the list to store the sensor readings
sensor_readings = []

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

# Take 11 sensor readings
while(len(sensor_readings) < 11):
  if ser.in_waiting > 0:
    line = ser.readline().decode('utf-8').rstrip()
    distance = int(line)
    print(distance)

    # Append the sensor value to the list
    sensor_readings.append(distance)

# Sort the list
sorted_readings = sorted(sensor_readings)

# Calculate the median value
median_value = statistics.median(sorted_readings)

# Print the median value
print("Median value:", median_value)

if median_value < 1000:
  print("less than")
  timestr = time.strftime("%Y%m%d-%H%M")
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(4, GPIO.OUT)
  GPIO.output(4, GPIO.HIGH)
  picam2 = Picamera2()
  time.sleep(1) # seconds
  picam2.start_and_capture_file("/home/pi/Desktop/timelapse/"+timestr+".jpg",delay=0,show_preview=False)
  GPIO.output(4, GPIO.LOW)
