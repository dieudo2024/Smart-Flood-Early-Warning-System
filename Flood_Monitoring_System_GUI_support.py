import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import Flood_Monitoring_System_GUI
from input.rotary_controller import get_threshold
from sensors.ds18b20 import read_temp
from gpiozero import DistanceSensor

_debug = True

SENSOR_HEIGHT_CM = 30.0

try:
    _dist_sensor = DistanceSensor(echo=5, trigger=22)
    _dist_available = True
    print("[DISTANCE] Sensor ready on echo=5, trigger=22.")
except Exception as e:
    _dist_sensor = None
    _dist_available = False
    print(f"[DISTANCE] Not available: {e}")


def read_water_level():
    if not _dist_available or _dist_sensor is None:
        return None
    try:
        distance_cm = _dist_sensor.distance * 100
        level = SENSOR_HEIGHT_CM - distance_cm
        return round(max(level, 0.0), 2)
    except Exception as e:
        print(f"[ERROR] Water level read failed: {e}")
        return None


def update_threshold():
    threshold = get_threshold()
    _w1.thresholdLabel.config(text=f"{threshold:.0f} cm")
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
    root.after(5000, update_water)


def main(*args):
    global root, _top1, _w1

    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)

    _top1 = root
    _w1 = Flood_Monitoring_System_GUI.Toplevel1(_top1)

    update_threshold()
    update_temperature()
    update_water()

    root.mainloop()


if __name__ == '__main__':
    main()
