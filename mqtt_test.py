import json

import paho.mqtt.client as mqtt
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("oki/lr/ac/mode/set")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.payload)


# Define constants
MQTT_SERVER = "192.168.0.95"
MQTT_PORT = 1883
DEVICE_ID = "ledScreen"

# Define MQTT Topics
TOPIC_STATE = "oki/lr/screen/"
TOPIC_COMMAND = "oki/lr/screen/set"

#Discovery JSON
dict1 = {
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

dict2 = {
    "name" : "brightness",
    "unique_id": "ledscreen_brightness",
    "command_topic": "oki/screen/bright/set",
    "mode": "slider",
    "device" : {
        "name" : "RPi LED Device",
        "identifiers": "ledscreen"
    }
}

json_object_1 = json.dumps(dict1)
json_object_2 = json.dumps(dict2)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.0.95", 1883, 60)
mqttc.publish("homeassistant/switch/ledscreen/config", json_object_1)
mqttc.publish("homeassistant/number/ledscreen/config", json_object_2)
mqttc.subscribe("oki/screen/bright/set")
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()