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


def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

myMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
myMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
myMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
myMQTTClient.configureOfflinePublishQueueing(config.OFFLINE_QUEUE_SIZE)
myMQTTClient.configureDrainingFrequency(config.DRAINING_FREQ)
myMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
myMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)

if myMQTTClient.connect():
    print('AWS connection succeeded')
else:
    raise RuntimeError("AWS connection failed. Check endpoint, certificates, and network access.")

publish_topic  = getattr(config, "LEVEL_TOPIC", config.TOPIC)
subscribe_topic = getattr(config, "SUB_TOPIC",   config.TOPIC)

myMQTTClient.subscribe(subscribe_topic, 1, customCallback)
time.sleep(2)

# State definitions 
class State(Enum):
    NORMAL     = "NORMAL"
    WARNING    = "WARNING"
    FLOOD_RISK = "FLOOD_RISK"

# Thresholds 
W_crit = get_threshold()   
W_warn = W_crit / 2

def determine_state(water_level):
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
    _w1.stateLabel.config(
        text=current_state.value,
        background=STATE_COLORS[current_state]
    )

    root.after(200, update_state)


def update_threshold():
    global W_warn, W_crit
    W_crit = get_threshold()
    W_warn = W_crit / 2
    _w1.thresholdLabel.config(text=f"{W_crit:.2f} cm")
    root.after(200, update_threshold)


def update_temperature():
    global current_temp
    current_temp = read_temp()
    if current_temp is None:
        _w1.temperatureLabel.config(text="-- °C")
    else:
        _w1.temperatureLabel.config(text=f"{current_temp:.2f} °C")
    root.after(3000, update_temperature)



def update_water():
    global water_level
    water_level = read_water_level()
    if water_level is None:
        water_level = 0.0
        _w1.waterLevelLabel.config(text="-- cm")
    else:
        _w1.waterLevelLabel.config(text=f"{water_level:.2f} cm")
        fan.set_on(current_state == State.FLOOD_RISK)
    root.after(3000, update_water)

    


# LED loop
def loop():
    blue_led.off()
    yellow_led.off()
    red_led.off()

    while True:
        if current_state == State.NORMAL:
            blue_led.on()
            yellow_led.off()
            red_led.off()
            fan.set_on(False)
        elif current_state == State.WARNING:
            blue_led.off()
            yellow_led.on()
            red_led.off()
            fan.set_on(False)
        elif current_state == State.FLOOD_RISK:
            blue_led.off()
            yellow_led.off()
            red_led.on()
            fan.set_on(True)
        time.sleep(0.2)    


def publish_data():
    """Publishes sensor data to AWS every 5 seconds."""
    print("Starting data publish loop...")
    while True:
        try:
            payload = json.dumps({
                "device_id":   "team_01",
                "water_level": water_level,
                "temperature": current_temp,
                "state":       current_state.value,
            })
            published = myMQTTClient.publish(publish_topic, payload, 1)
            if published:
                print(f"Published to {publish_topic}: {payload}")
            else:
                print(f"Publish failed for topic {publish_topic}")
        except Exception as e:
            print(f"An error occurred while publishing data: {e}")
        time.sleep(5)



def main(*args):
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
    try:
        main()
    except KeyboardInterrupt:
        print("\n Exiting the program!")
    except Exception as e:
        print(f"An error occurred: {e}")