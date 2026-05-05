from enum import Enum
import sys
from timeit import Timer
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import Flood_Monitoring_System_GUI
from input.rotary_controller import get_threshold
from sensors.ds18b20 import read_temp
from sensors.distance import read_water_level
from gpiozero import LED
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import config
import json
import time
from datetime import datetime
_debug = True
from output import buzzer, fan
import threading


# Hardware setup

green_led = LED(24)     # Normal state
yellow_led = LED(18)    # Warning state
red_led = LED(23)       # Flood risk state

# buzzer = Buzzer(17)     # Buzzer for warning and flood risk states


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

# State definitions
class State(Enum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    FLOOD_RISK = "FLOOD_RISK"

# Thresholds (in cm)
current_threshold = get_threshold() # Reading the threshold from the rotary encoder

W_warn = get_threshold() / 2    # Warning level
W_crit = get_threshold()   # Critical level (flood risk)

# State determination based on water level
def determine_state(water_level):
    global W_warn, W_crit
    print(f"Determining state with water level: {water_level:.2f} cm, W_warn: {W_warn:.2f} cm, W_crit: {W_crit:.2f} cm")
    if water_level < W_warn:
        return State.NORMAL
    elif water_level < W_crit:
        return State.WARNING
    else:
        return State.FLOOD_RISK


water_level = read_water_level() # Reading the water level from the sensor

current_state = determine_state(water_level) # Determine the current state based on the water level

current_temp = read_temp() # Reading the temperature from the sensor

def update_state():
    global current_state
    current_state = determine_state(water_level)
    _w1.stateLabel.config(text=current_state.value)
    # Update colors based on state
    if current_state == State.NORMAL:
        _w1.stateLabel.config(background="#00ff00")  # Green
    elif current_state == State.WARNING:
        _w1.stateLabel.config(background="#ffff00")  # Yellow
    elif current_state == State.FLOOD_RISK:
        _w1.stateLabel.config(background="#ff0000")  # Red
    root.after(200, update_state)

def update_threshold():
    global current_threshold
    current_threshold = get_threshold()
    _w1.thresholdLabel.config(text=f"{current_threshold:.2f} cm")
    root.after(200, update_threshold)

def update_temperature():
    global current_temp
    current_temp = read_temp()
    if current_temp is None:
        _w1.temperatureLabel.config(text="-- °C")
    else:
        _w1.temperatureLabel.config(text=f"{current_temp:.2f} °C")
    root.after(200, update_temperature)

def update_water():
    global water_level, current_state
    water_level = read_water_level()
    if water_level is None:
        _w1.waterLevelLabel.config(text="-- cm")
    else:
        _w1.waterLevelLabel.config(text=f"{water_level:.2f} cm")
        fan.set_on(current_state == State.FLOOD_RISK)

    root.after(200, update_water)

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
        update_state()          # Start the state update loop

        loop_thread = threading.Thread(target=loop) # Create a separate thread for the loop function to avoid blocking the GUI
        loop_thread.start()

        publish_thread = threading.Thread(target=publish_data) # Create a separate thread for the publish_data function to avoid blocking the GUI
        publish_thread.start()

        root.mainloop() # Start the GUI event loop

    except Exception as e:
        print(f"An error occurred from the main function in GUI Support: {e}")

def publish_data():
    print("Starting data publish loop...")
    while True:
        global water_level, current_state, current_temp
        try:
            current_temp = read_temp() # Reading the temperature from the sensor

            payload=json.dumps({
                                "device_id": "team_01",
                                "water_level": water_level,
                                "temperature": current_temp,
                                "state": current_state.value
                                })
            
            published = myMQTTClient.publish(publish_topic, payload, 1)
            if published:
                print(f"Published to {publish_topic}: {payload}")
            else:
                print(f"Publish failed for topic {publish_topic}")
            time.sleep(5)  # To send a message every 5 seconds. 
        except Exception as e:
            print(f"An error occurred while publishing data: {e}")

def loop():
    print("Starting main loop...")   
    
    # Reset all outputs before applying the new state
    green_led.off()
    yellow_led.off()
    red_led.off()
    buzzer.reset_silence() # Ensure buzzer is silenced before applying new state
    while True:
            # Determine the current state based on the water level
            global current_state

            if current_state == State.NORMAL:
                green_led.on()
                buzzer.silence_alarm() # Ensure buzzer is silenced in NORMAL state
            elif current_state == State.WARNING:
                yellow_led.on()
                buzzer._warning_beep(current_state, root) # Start the warning beep loop
            elif current_state == State.FLOOD_RISK:
                red_led.on()
                buzzer.on() # Continuous alert        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n Exiting the program!")   # Handle the keyboard interrupt (Ctrl+C) to exit the program gracefully
    except Exception as e:
        print(f"An error occurred from the main function in GUI Support: {e}")
