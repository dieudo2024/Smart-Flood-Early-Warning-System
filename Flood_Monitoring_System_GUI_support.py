import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import Flood_Monitoring_System_GUI
from input.rotary_controller import get_threshold
from sensors.ds18b20 import read_temp
from sensors.distance import read_water_level
from gpiozero import DistanceSensor
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import config
import json
import time
from datetime import datetime
from input import fan
_debug = True

# user specified callback function
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# configure the MQTT client
myMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
myMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
myMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
myMQTTClient.configureOfflinePublishQueueing(config.OFFLINE_QUEUE_SIZE)
myMQTTClient.configureDrainingFrequency(config.DRAINING_FREQ)
myMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
myMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)

#Connect to MQTT Host
if myMQTTClient.connect():
    print('AWS connection succeeded')
else:
    raise RuntimeError("AWS connection failed. Check endpoint, certificates, and network access.")

publish_topic = getattr(config, "LEVEL_TOPIC", config.TOPIC)
subscribe_topic = getattr(config, "SUB_TOPIC", config.TOPIC)

# Subscribe to topic
myMQTTClient.subscribe(subscribe_topic, 1, customCallback)
time.sleep(2)

def update_threshold():
    threshold = get_threshold()
    _w1.thresholdLabel.config(text=f"{threshold:.2f} cm")
    root.after(200, update_threshold)

def update_temperature():
    temp = read_temp()
    if temp is None:
        _w1.temperatureLabel.config(text="-- °C")
    else:
        _w1.temperatureLabel.config(text=f"{temp:.2f} °C")
    root.after(5000, update_temperature)

def update_water():
    water = read_water_level()
    if water is None:
        _w1.waterLevelLabel.config(text="-- cm")
    else:
        _w1.waterLevelLabel.config(text=f"{water:.2f} cm")
        # state = determine_state(water)
        # fan.set_on(state == "FLOOD_RISK")

    root.after(5000, update_water)

def main(*args):
    global root, _top1, _w1
    
    try:
        root = tk.Tk()
        root.protocol('WM_DELETE_WINDOW', root.destroy)

        _top1 = root
        _w1 = Flood_Monitoring_System_GUI.Toplevel1(_top1)

        fan.init()  # Initializing the fan
        update_temperature()    # Start the temperature update loop
        update_water()       # Start the water level update loop
        update_threshold()      # Start the threshold update loop
        publish_data() # publishes just once for now
        root.mainloop() # Start the GUI event loop
    except Exception as e:
        print(f"An error occurred from the main function in GUI Support: {e}")

def publish_data():
        try:
            temp_c = read_temp() # Reading the temperature from the sensor
            distance = read_water_level() # Reading the water level from the sensor

            payload=json.dumps({
                                "device_id": "team_01",
                                "water_level": distance,
                                "temperature": temp_c,
                                "state": "WARNING"
                                })
            
            published = myMQTTClient.publish(publish_topic, payload, 1)
            if published:
                print(f"Published to {publish_topic}: {payload}")
            else:
                print(f"Publish failed for topic {publish_topic}")
            time.sleep(5)  # To send a message every 5 seconds. 
        except Exception as e:
            print(f"An error occurred while publishing data: {e}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n Exiting the program!")   # Handle the keyboard interrupt (Ctrl+C) to exit the program gracefully
    except Exception as e:
        print(f"An error occurred from the main function in GUI Support: {e}")
