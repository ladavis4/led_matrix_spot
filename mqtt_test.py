import json

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

def bright_callback(client, userdata, msg):
    # Handles brightness settings for the LED Screen
    print("A brightness message was received")
    print(msg.payload.decode("utf-8"))

def picture_callback(client, userdata, msg):
    # Handles brightness settings for the LED Screen
    print("A picture message was received")
    print(msg.payload.decode("utf-8"))

def weather_callback(client, userdata, msg):
    # Handles brightness settings for the LED Screen
    print("A weather message was received")
    print(msg.payload.decode("utf-8"))

def calendar_callback(client, userdata, msg):
    # Handles brightness settings for the LED Screen
    print("A calendar message was received")
    print(msg.payload.decode("utf-8"))

def spotify_callback(client, userdata, msg):
    # Handles brightness settings for the LED Screen
    print("A spotify message was received")
    print(msg.payload.decode("utf-8"))

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("oki/screen/#")

    client.publish("homeassistant/switch/ledscreen_power/config", power_json_obj)
    client.publish("homeassistant/number/ledscreen/config", bright_json_obj)
    client.publish("homeassistant/switch/ledscreen_picture_sw/config", picture_json_obj)
    client.publish("homeassistant/switch/ledscreen_weather_sw/config", weather_json_obj)
    client.publish("homeassistant/switch/ledscreen_calednar_sw/config", calendar_json_obj)
    client.publish("homeassistant/switch/ledscreen_spotify_sw/config", spotify_json_obj)

    client.message_callback_add("oki/screen/power/set", power_callback)
    client.message_callback_add("oki/screen/bright/set", bright_callback)
    client.message_callback_add("oki/screen/pic/set", picture_callback)
    client.message_callback_add("oki/screen/cal/set", calendar_callback)
    client.message_callback_add("oki/screen/weather/set", weather_callback)
    client.message_callback_add("oki/screen/spot/set", spotify_callback)

# Define constants
MQTT_SERVER = "192.168.0.95"
MQTT_PORT = 1883
DEVICE_ID = "ledScreen"

#Discovery JSON
power_json = {
    "name" : "power",
    "unique_id": "ledscreen_power",
    "command_topic": "oki/screen/power/set",
    "optimistic": "true",
    "device" : {
        "name" : "RPi LED Device",
        "identifiers": "ledscreen",
        "manufacturer" : "Lenny Davis",
        "model" : "Raspberry Pi 4B",
    }
}

bright_json = {
    "name" : "brightness",
    "unique_id": "ledscreen_brightness",
    "command_topic": "oki/screen/bright/set",
    "mode": "slider",
    "device" : {
        "name" : "RPi LED Device",
        "identifiers": "ledscreen"
    }
}

picture_json = {
    "name" : "pictures_sw",
    "unique_id": "ledscreen_picture_sw",
    "command_topic": "oki/screen/pic/set",
    "device" : {
        "name" : "RPi LED Device",
        "identifiers": "ledscreen"
    }
}

weather_json = {
    "name" : "weather_sw",
    "unique_id": "ledscreen_weather_sw",
    "command_topic": "oki/screen/weather/set",
    "device" : {
        "name" : "RPi LED Device",
        "identifiers": "ledscreen"
    }
}

calendar_json = {
    "name" : "calendar_sw",
    "unique_id": "ledscreen_calendar_sw",
    "command_topic": "oki/screen/cal/set",
    "device" : {
        "name" : "RPi LED Device",
        "identifiers": "ledscreen"
    }
}

spotify_json = {
    "name" : "spotify_sw",
    "unique_id": "ledscreen_spotify_sw",
    "command_topic": "oki/screen/spot/set",
    "device" : {
        "name" : "RPi LED Device",
        "identifiers": "ledscreen"
    }
}

power_json_obj = json.dumps(power_json)
bright_json_obj = json.dumps(bright_json)
picture_json_obj = json.dumps(picture_json)
weather_json_obj = json.dumps(weather_json)
calendar_json_obj = json.dumps(calendar_json)
spotify_json_obj = json.dumps(spotify_json)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.95", 1883, 60)


client.loop_forever()
