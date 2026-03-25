import paho.mqtt.client as mqtt
from xml.etree import ElementTree as ET
import requests
import config

# Note: April 2024, web page changed, now using calls to an API:
# https://pla.co.uk/api-proxy/api_one_minute?_api_proxy_uri=/tides/height-xml/14571

# Set the MQTT broker address and port
broker_address = "mqtt.cetools.org"
broker_port = 1884

# Set the MQTT client ID and credentials
client = mqtt.Client(client_id="tide-house-mill-api")
client.username_pw_set(username=config.mqttusername, password=config.mqttpassword)
# Connect to the MQTT broker
client.connect(broker_address, broker_port)


# Function to parse the XML data
def parse_xml(xml_data):
  root = ET.fromstring(xml_data)
  gauges = []
  for gauge in root.findall("gauges/gauge"):
    gauge_data = {
      "id": gauge.find("id").text,
      "name": gauge.find("name").text,
      "bolHeightAvailable": gauge.find("bolHeightAvailable").text,
      "date": gauge.find("date").text,
      "time": gauge.find("time").text,
      "height": gauge.find("height").text,
      "predicted": gauge.find("predicted").text,
      "surge": gauge.find("surge").text,
    }
    gauges.append(gauge_data)
  return gauges


# Define your list of IDs
# 14571 Tower
# 14512 Charlton
# 14551 Silvertown
# 14561 Tilbury

ids = [14571, 14512, 14561, 14551, 14551]

# Loop through each ID
for gauge_id in ids:
  url = f"https://pla.co.uk/api-proxy/api_one_minute?_api_proxy_uri=/tides/height-xml/{gauge_id}"  # Use f-string for URL construction
  response = requests.get(url)

  xml_data = response.content

  # Parse the XML data
  parsed_data = parse_xml(xml_data)

  for gauge_data in parsed_data:
    print("Name:", gauge_data["name"])

    print("Observed:", gauge_data["height"])
    topic = "personal/ucjtdjw/housemill/" + gauge_data["name"] + "/observed"
    message = gauge_data["height"]
    client.publish(topic, message)

    print("Predicted:", gauge_data["predicted"])
    topic = "personal/ucjtdjw/housemill/" + gauge_data["name"] + "/predicted"
    message = gauge_data["predicted"]
    client.publish(topic, message)
  
    print("Surge:", gauge_data["surge"])
    topic = "personal/ucjtdjw/housemill/" + gauge_data["name"] + "/surge"
    message = gauge_data["surge"]
    client.publish(topic, message)  

# Disconnect from the MQTT broker
client.disconnect()