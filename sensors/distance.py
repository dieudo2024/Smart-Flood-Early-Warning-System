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