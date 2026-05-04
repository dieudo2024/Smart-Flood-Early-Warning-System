from sensors.ds18b20 import read_temp
import sensors.ds18b20 as ds18b20
from time import sleep
from datetime import datetime
from gpiozero import PWMLED, LED, DistanceSensor, Device
from gpiozero.exc import BadPinFactory
from gpiozero.pins.mock import MockFactory
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from enum import Enum
from gpiozero import LED, Buzzer

import config
import json
import time
import random
import warnings

import os

# Hardware setup

green_led = LED(24)     # Normal state
yellow_led = LED(18)    # Warning state
red_led = LED(23)       # Flood risk state

buzzer = Buzzer(17)     # Buzzer for warning and flood risk states


# State definitions
class State(Enum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    FLOOD_RISK = "FLOOD_RISK"

# Thresholds (in cm)
W_warn = 5.0    # Warning level
W_crit = 10.0   # Critical level (flood risk)

# State determination based on water level
def determine_state(water_level):
    if water_level < W_warn:
        return State.NORMAL
    elif water_level < W_crit:
        return State.WARNING
    else:
        return State.FLOOD_RISK

try: # import of the rotary controller for setup if available
    from input import rotary_controller as rotary
except ImportError:
    rotary = None

def setup():
    ds18b20.setup() # Setting up the DS18B20 sensor

tmp = 0.0 # To hold the temperature

# Functions to increase and decrease the temperature using the rotary encoder
def increase():
    global tmp
    tmp = tmp + 1

def decrease():
    global tmp
    tmp = tmp - 1

################################################################################

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

#################################################################################


from sensors import distance as dist, ds18b20

def loop():
    global tmp
    tmp_threshold = 25.0 # 25 °C - Default threshold, can be adjusted by the rotary encoder
    started = False # To check if the temperature has been read at least once, to avoid printing "Temperature: read failed" repeatedly if the sensor is not working properly
    while True:
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Get the current timestamp in a human-readable format for testing purposes.
        # temp_c = read_temp() # Reading the temperature from the sensor
        distance = dist.read_water_level() # Reading the water level from the sensor
        
        if not started:
            tmp = ds18b20.read_temp() # Reading the temperature from the sensor for the first time
            if tmp is None:
                print("Printed from main file -- Temperature: read failed")
            else:
                started = True
        else:
            print(f"Temperature - Celsius: {tmp:.2f} °C - Fahrenheit: {(tmp * 9/5) + 32:.2f} °F") 
            ######################################################################
            
            # Determine the current state based on the water level
            state = determine_state(distance)

            # Reset all outputs before applying the new state
            green_led.off()
            yellow_led.off()
            red_led.off()
            buzzer.off()

            if state == State.NORMAL:
                green_led.on()
            
            elif state == State.WARNING:
                yellow_led.on()
                buzzer.beep(on_time=0.1, off_time=2, background=True) # Short beep every 2 seconds

            elif state == State.FLOOD_RISK:
                red_led.on()
                buzzer.on() # Continuous alert
            
            payload=json.dumps({
                                "device_id": "team_01",
                                "water_level": distance,
                                "temperature": tmp,
                                "state": state
                                })
            published = myMQTTClient.publish(publish_topic, payload, 1)
            if published:
                print(f"Published to {publish_topic}: {payload}")
            else:
                print(f"Publish failed for topic {publish_topic}")
            time.sleep(2)  # To send a message every 10 seconds. 
##########################################################################################

        #     # Increasing the temperature using the rotary encorder
        #     if rotary is not None and hasattr(rotary, "rotor") and rotary.rotor is not None:
        #         # Checking if the rotary value is different from the last rotary value to avoid unnecessary updates
        #         rotary.rotor.when_rotated_clockwise = increase
        #         rotary.rotor.when_rotated_counter_clockwise = decrease

        #     if tmp > tmp_threshold:
        #         print("Temperature exceeds threshold!", tmp, "°C >", tmp_threshold, "°C")
        #         # rotary.led.blink(on_time=0.2, off_time=0.2)  # Blinking
        #         sleep(0.3)
        #     else:
        #         # rotary.led.off()  # Turn off the LED if the temperature is below the threshold
        #         sleep(0.1)
        # sleep(0.1)

if __name__ == '__main__':
    # setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("Exiting the program!")