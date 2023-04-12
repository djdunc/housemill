from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import paho.mqtt.client as mqtt
import config

# Set the MQTT broker address and port
broker_address = "mqtt.cetools.org"
broker_port = 1884

# set up the headless browser using ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

# navigate to the web page
url = "http://www.pla.co.uk/hydrographics/ltoverview.cfm"
driver.get(url)

# wait for the page to load and the content to be rendered dynamically
driver.implicitly_wait(10)  # wait for 10 seconds

# get the page source after it's loaded
html = driver.page_source

# parse the HTML using BeautifulSoup
plawebpage = BeautifulSoup(html, 'html.parser')

# find the elements containing the dynamically loaded content
tidetable = plawebpage.find('tbody')

# Set the MQTT client ID and credentials
client = mqtt.Client(client_id="tide-house-mill")
client.username_pw_set(username=config.mqttusername, password=config.mqttpassword)
# Connect to the MQTT broker
client.connect(broker_address, broker_port)

row_num = 1  # initialize row number to 1
for row in tidetable.find_all('tr'):
    if row_num == 7 or row_num >= 10:
        children = row.find_all('td')
        tide_gauge_name = children[0].get_text().strip()
        observed = children[1].get_text().strip()
        predicted = children[2].get_text().strip()
        surge = children[3].get_text().strip()
        state = children[6].get_text().strip()
        print(tide_gauge_name + ": observed " + observed + " predicted " 
              + predicted + " surge " + surge + "state " + state)
        # Publish a message to a topic
        topic = "personal/ucjtdjw/housemill/" + tide_gauge_name + "/observed"
        message = observed
        client.publish(topic, message)
        topic = "personal/ucjtdjw/housemill/" + tide_gauge_name + "/predicted"
        message = predicted
        client.publish(topic, message)
        topic = "personal/ucjtdjw/housemill/" + tide_gauge_name + "/surge"
        message = surge
        client.publish(topic, message)
        topic = "personal/ucjtdjw/housemill/" + tide_gauge_name + "/state"
        message = state
        client.publish(topic, message)            
    row_num += 1  # increment row number for next iteration


# close the browser
driver.quit()

# Disconnect from the MQTT broker
client.disconnect()