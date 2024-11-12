import json
import os
import time

import paho.mqtt.client as mqtt
# The callback for when the client receives a CONNACK response from the server.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # This function is the general MQTT callback. If the message is unidentified it
    # will handle the data
    print("An unidentified message was detected")
    print(msg.payload.decode("utf-8"))

def power_callback(client, userdata, msg):
    # Handles power toggle for the LED Screen
    print("A power message was received")
    print(msg.payload.decode("utf-8"))
    data['button_on'] = msg.payload.decode("utf-8") == 'ON'
    with open(os.getcwd() + '/temp/settings.json', 'w') as outfile:
        json.dump(data, outfile)

def bright_callback(client, userdata, msg):
    # Handles brightness settings for the LED Screen
    print("A brightness message was received")
    print(msg.payload.decode("utf-8"))
    data['slider_brightness'] = msg.payload.decode("utf-8")
    with open(os.getcwd() + '/temp/settings.json', 'w') as outfile:
        json.dump(data, outfile)

def picture_callback(client, userdata, msg):
    # Handles brightness settings for the LED Screen
    print("A picture message was received")
    print(msg.payload.decode("utf-8"))
    data['button_img'] = msg.payload.decode("utf-8") == 'ON'
    with open(os.getcwd() + '/temp/settings.json', 'w') as outfile:
        json.dump(data, outfile)

def weather_callback(client, userdata, msg):
    # Handles brightness settings for the LED Screen
    print("A weather message was received")
    print(msg.payload.decode("utf-8"))
    data['button_time'] = msg.payload.decode("utf-8") == 'ON'
    with open(os.getcwd() + '/temp/settings.json', 'w') as outfile:
        json.dump(data, outfile)

def calendar_callback(client, userdata, msg):
    # Handles brightness settings for the LED Screen
    print("A calendar message was received")
    print(msg.payload.decode("utf-8"))
    data['button_cal'] = msg.payload.decode("utf-8") == 'ON'
    with open(os.getcwd() + '/temp/settings.json', 'w') as outfile:
        json.dump(data, outfile)

def spotify_callback(client, userdata, msg):
    # Handles brightness settings for the LED Screen
    print("A spotify message was received")
    print(msg.payload.decode("utf-8"))
    data['button_spot'] = msg.payload.decode("utf-8") == 'ON'
    with open(os.getcwd() + '/temp/settings.json', 'w') as outfile:
        json.dump(data, outfile)


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("oki/screen/#")

    client.message_callback_add("oki/screen/power/set", power_callback)
    client.message_callback_add("oki/screen/bright/set", bright_callback)
    client.message_callback_add("oki/screen/pic/set", picture_callback)
    client.message_callback_add("oki/screen/cal/set", calendar_callback)
    client.message_callback_add("oki/screen/weather/set", weather_callback)
    client.message_callback_add("oki/screen/spot/set", spotify_callback)

    create_and_publish_discovery(client)

def create_and_publish_discovery(client):
    f = open('mqtt_discovery.json')
    data = json.load(f)
    client.publish("homeassistant/switch/ledscreen_power/config", json.dumps(data['power_discovery']))
    client.publish("homeassistant/number/ledscreen/config", json.dumps(data['brightness_discovery']))
    client.publish("homeassistant/switch/ledscreen_picture_sw/config", json.dumps((data['picture_discovery'])))
    client.publish("homeassistant/switch/ledscreen_weather_sw/config", json.dumps(data['weather_discovery']))
    client.publish("homeassistant/switch/ledscreen_calednar_sw/config", json.dumps(data['calendar_discovery']))
    client.publish("homeassistant/switch/ledscreen_spotify_sw/config", json.dumps(data['spotify_discovery']))
    f.close()

# Define constants
MQTT_SERVER = "192.168.0.95"
MQTT_PORT = 1883
DEVICE_ID = "ledScreen"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.95", 1883, 60)

try:
    print(os.getcwd())
    with open(os.getcwd() + '/temp/settings.json') as json_file:
        data = json.load(json_file)
        print("Settings loaded successfully")
except:
    print("Settings file doesn't exist, run main.py first!")


client.loop_start()
while 1:
    time.sleep(1)
