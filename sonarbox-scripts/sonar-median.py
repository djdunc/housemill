#!/usr/bin/env python3
import serial
import statistics

# Initialize the list to store the sensor readings
sensor_readings = []

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

# Take 20 sensor readings
while(len(sensor_readings) < 21):
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
