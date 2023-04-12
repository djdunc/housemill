#!/usr/bin/env python3
import serial
import statistics
import paho.mqtt.client as mqtt

import config

# Initialize the list to store the sensor readings
sensor_readings = []

# Set the MQTT broker address and port
broker_address = "mqtt.cetools.org"
broker_port = 1884

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

# Take 20 sensor readings
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

# Set the MQTT client ID and credentials
client = mqtt.Client(client_id="sonar-house-mill")
client.username_pw_set(username=config.mqttusername, password=config.mqttpassword)

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Publish a message to a topic
topic = "personal/ucjtdjw/housemill/sonar/distance"
message = median_value
client.publish(topic, message)

# Disconnect from the MQTT broker
client.disconnect()
