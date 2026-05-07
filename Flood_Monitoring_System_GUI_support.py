from enum import Enum
import sys
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
from output import buzzer, fan
import threading

_debug = True

#LEDs setup
blue_led  = LED(24)   
yellow_led = LED(23)   
red_led    = LED(18)  

"""This module contains the main logic for the flood monitoring system, including reading sensor data, determining the current state based on thresholds, updating the GUI, controlling the LEDs and fan, and publishing data to AWS IoT Core. It also includes error handling to ensure that the system continues to operate even if there are issues with the sensors or AWS connection."""
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

"""AWS IoT Core setup. We create an MQTT client, configure it with our AWS endpoint and credentials, and connect to AWS. We also subscribe to a topic to receive messages from AWS if needed."""
myMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
myMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
myMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
myMQTTClient.configureOfflinePublishQueueing(config.OFFLINE_QUEUE_SIZE)
myMQTTClient.configureDrainingFrequency(config.DRAINING_FREQ)
myMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
myMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)

"""We attempt to connect to AWS IoT Core. If the connection is successful, we print a success message. If it fails, we raise a RuntimeError with a message indicating that the connection failed and suggesting to check the endpoint, certificates, and network access."""
if myMQTTClient.connect():
    print('AWS connection succeeded')
else:
    raise RuntimeError("AWS connection failed. Check endpoint, certificates, and network access.")

"""We set the publish topic and subscribe topic for AWS IoT Core. We use getattr to allow for optional configuration of these topics in the config module, defaulting to config.TOPIC if not specified. We then subscribe to the subscribe topic with a custom callback function to handle incoming messages from AWS."""
publish_topic  = getattr(config, "LEVEL_TOPIC", config.TOPIC)
subscribe_topic = getattr(config, "SUB_TOPIC",   config.TOPIC)

myMQTTClient.subscribe(subscribe_topic, 1, customCallback)
time.sleep(2)       # Sleep for a short time to ensure the subscription is set up before we start publishing data to AWS

# State definitions 
class State(Enum):
    NORMAL     = "NORMAL"
    WARNING    = "WARNING"
    FLOOD_RISK = "FLOOD_RISK"

# Thresholds 
W_crit = get_threshold()   
W_warn = W_crit / 2

def determine_state(water_level):
    """Determines the current state of the system based on the water level and defined thresholds. Returns a State enum value indicating whether the system is in NORMAL, WARNING, or FLOOD_RISK state."""
    global W_warn, W_crit
    if water_level < W_warn:
        return State.NORMAL
    elif water_level < W_crit:
        return State.WARNING
    else:
        return State.FLOOD_RISK

# Sensor values
water_level   = 0.0
current_state = State.NORMAL
current_temp  = None


def update_state():
    """Updates state label color and text, LEDs, and buzzer's current_state."""
    global current_state

    current_state = determine_state(water_level)

    # Update buzzer module's current_state so it reacts to changes
    buzzer.current_state = current_state.value

    # Reset silence when back to NORMAL
    if current_state == State.NORMAL:
        buzzer.reset_silence()

    # Update state label text and color
    STATE_COLORS = {
        State.NORMAL:     "#00ff00",
        State.WARNING:    "#ffff00",
        State.FLOOD_RISK: "#ff0000",
    }
    
    """Update the state label in the GUI with the current state and corresponding color. We use the STATE_COLORS dictionary to map each state to a specific color, and we update the label's text and background color accordingly. We then schedule this function to run again after 200ms to continuously monitor for changes in state and update the GUI."""
    _w1.stateLabel.config(
        text=current_state.value,
        background=STATE_COLORS[current_state]
    )

    root.after(200, update_state)       # Schedule this function to run again after 200ms to continuously monitor for changes in state and update the GUI accordingly

def update_threshold():
    """Update the threshold value from the rotary encoder and update the corresponding label in the GUI."""
    global W_warn, W_crit
    W_crit = get_threshold()        # Update the critical threshold value from the rotary encoder
    W_warn = W_crit / 2             # Update the warning threshold to be half of the critical threshold
    _w1.thresholdLabel.config(text=f"{W_crit:.2f} cm")
    root.after(200, update_threshold)   # Schedule this function to run again after 200ms to continuously monitor for changes

def update_temperature():
    """Update the temperature value from the DS18B20 sensor and update the corresponding label in the GUI. """
    global current_temp
    current_temp = read_temp()    # Read the current temperature from the DS18B20 sensor and store it in the global variable current_temp
    if current_temp is None:
        _w1.temperatureLabel.config(text="-- °C")  
    else:
        _w1.temperatureLabel.config(text=f"{current_temp:.2f} °C")
    root.after(3000, update_temperature)   # Schedule this function to run again after 3000ms (3 seconds) to continuously monitor for changes in temperature 

def update_water():
    """Update the water level value from the distance sensor and update the corresponding label in the GUI. """
    global water_level
    water_level = read_water_level()        # Read the current water level from the distance sensor and store it in the global variable water_level
    
    if water_level is None:
        water_level = 0.0
        _w1.waterLevelLabel.config(text="-- cm")
    else:
        _w1.waterLevelLabel.config(text=f"{water_level:.2f} cm")
        fan.set_on(current_state == State.FLOOD_RISK)       # Set the fan on if we're in FLOOD_RISK state, otherwise it will be turned off.
    root.after(3000, update_water)      # Schedule this function to run again after 3000ms (3 seconds) to continuously monitor for changes in water level and update the GUI accordingly


# LED loop
def loop():
    """Loop to continuously update the LEDs based on the current state. 
    The blue LED is on in NORMAL state, the yellow LED is on in WARNING state, 
    and the red LED is on in FLOOD_RISK state. We also control the fan based on the current state, 
    turning it on in FLOOD_RISK state and off otherwise. This loop runs indefinitely with a short sleep to prevent it from consuming too much CPU."""

    blue_led.off()
    yellow_led.off()
    red_led.off()

    while True:
        if current_state == State.NORMAL:   # In NORMAL state, we turn on the blue LED and ensure the fan is off
            blue_led.on()
            yellow_led.off()
            red_led.off()
            fan.set_on(False)
        elif current_state == State.WARNING:    # In WARNING state, we turn on the yellow LED and ensure the fan is off
            blue_led.off()
            yellow_led.on()
            red_led.off()
            fan.set_on(False)
        elif current_state == State.FLOOD_RISK: # In FLOOD_RISK state, we turn on the red LED and turn on the fan
            blue_led.off()
            yellow_led.off()
            red_led.on()
            fan.set_on(True)
        time.sleep(0.2)     # Sleep for a short time to prevent this loop from consuming too much CPU


def publish_data():
    """Publishes sensor data to AWS every 5 seconds."""
    print("Starting data publish loop...")
    while True:
        try:
            # We construct a JSON payload with the device ID, water level, temperature, and current state, and publish it to the configured AWS IoT Core topic.
            payload = json.dumps({
                "device_id":   "team_01",
                "water_level": water_level,
                "temperature": current_temp,
                "state":       current_state.value,
            })

            published = myMQTTClient.publish(publish_topic, payload, 1)  # Publish the payload to AWS IoT Core with QoS level 1
            if published:
                print(f"Published to {publish_topic}: {payload}")
            else:
                print(f"Publish failed for topic {publish_topic}")
        except Exception as e:
            print(f"An error occurred while publishing data: {e}")
        time.sleep(5)       # Sleep for 5 seconds before publishing the next set of data to AWS to avoid overwhelming the network and AWS with too many messages in a short period of time

def main(*args):

    """Main function to initialize the GUI, set up the buzzer and fan controls, 
    start the sensor update loops, and start the background threads for the LED loop and AWS publishing. 
    We also include error handling to catch any exceptions that occur during initialization and print an error message to the console."""

    global root, _top1, _w1

    try:
        root = tk.Tk()
        root.protocol('WM_DELETE_WINDOW', root.destroy)

        _top1 = root
        _w1 = Flood_Monitoring_System_GUI.Toplevel1(_top1)

        # Buzzer setup
        buzzer.init(root)
        _w1.alarmButton.config(command=buzzer.silence_alarm)  
        root.after(500, buzzer.update_buzzer)                

        fan.init(root)              # initialize fan motor
        _w1.gateButton.config(command=fan.toggle)  # Set fan button to toggle the fan
        
        # sensor label and LED loop
        update_temperature()    # start sensor label loops
        update_water()
        update_threshold()
        update_state()          # start state + LED color loop

        # Background threads for LEDs and MQTT
        threading.Thread(target=loop,         daemon=True).start()
        threading.Thread(target=publish_data, daemon=True).start()

        root.mainloop()

    except Exception as e:
        print(f"An error occurred from the main function in GUI Support: {e}")


if __name__ == '__main__':
    """When the script is run directly, we call the main function to start the application. """
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n Exiting the program!")
    except Exception as e:
        print(f"An error occurred: {e}")