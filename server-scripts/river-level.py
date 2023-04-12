## River / Tide data from:
## https://riverlevels.uk/thames-tideway-tower-pier-tidal

import logging
from datetime import datetime, timedelta

import pytz
import requests
from bs4 import BeautifulSoup

import paho.mqtt.client as mqtt

import config

# Set the MQTT broker address and port
broker_address = "mqtt.cetools.org"
broker_port = 1884

get_time = pytz.utc.localize(datetime.utcnow())
request = BeautifulSoup(
    requests.get("https://riverlevels.uk/thames-tideway-london-silvertown-tidal").content,
    "html.parser",
)

tide = request.find("h2", attrs={"class": "value"})

tidelevel = tide.text.strip() # strip() is used to remove starting and trailing
SilvertownTidal = tidelevel[:-1]

request = BeautifulSoup(
    requests.get("https://riverlevels.uk/thames-tideway-tower-pier-tidal").content,
    "html.parser",
)

tide = request.find("h2", attrs={"class": "value"})

tidelevel = tide.text.strip() # strip() is used to remove starting and trailing
TowerPierTidal = tidelevel[:-1]

request = BeautifulSoup(
    requests.get("https://riverlevels.uk/lee-lea-bridge").content,
    "html.parser",
)

tide = request.find("h2", attrs={"class": "value"})

tidelevel = tide.text.strip() # strip() is used to remove starting and trailing
LeaBridgeRiver = tidelevel[:-1]

print(SilvertownTidal)
print(TowerPierTidal)
print(LeaBridgeRiver)

# Set the MQTT client ID and credentials
client = mqtt.Client(client_id="tide-house-mill")
client.username_pw_set(username=config.mqttusername, password=config.mqttpassword)
# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Publish a message to a topic
topic = "personal/ucjtdjw/housemill/SilvertownTidal/height"
message = SilvertownTidal
client.publish(topic, message)

# Publish a message to a topic
topic = "personal/ucjtdjw/housemill/TowerPierTidal/height"
message = TowerPierTidal
client.publish(topic, message)

# Publish a message to a topic
topic = "personal/ucjtdjw/housemill/LeaBridgeRiver/height"
message = LeaBridgeRiver
client.publish(topic, message)

# Disconnect from the MQTT broker
client.disconnect()
