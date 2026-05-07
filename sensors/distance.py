from gpiozero import DistanceSensor

_debug = True

SENSOR_HEIGHT_CM = 30.0

class MyDistanceSensor(DistanceSensor):
    """Custom DistanceSensor that returns max_distance instead of raising an error when out of range."""
    def _read(self):
        try:
            return super()._read()
        except Exception:
            return self.max_distance

try:
    """Attempt to initialize the distance sensor. If it fails (e.g., due to hardware issues), 
    we set a flag to indicate it's not available and handle it gracefully in the rest of the code."""

    _dist_sensor = MyDistanceSensor(echo=5, trigger=22, queue_len=1, partial=True) # GPIO pins for the sensor, 
                                                                    # with a queue length of 1 to always get the most recent reading 
                                                                    # and partial=True to allow for out-of-range readings without errors
    _dist_available = True      # Flag to indicate the distance sensor is available and initialized successfully
except Exception as e:
    _dist_sensor = None
    _dist_available = False
    print(f"[DISTANCE] Not available: {e}")

def read_water_level():
    """Read the water level in cm. Returns None if the sensor is not available or if there's an error reading the distance."""

    if not _dist_available or _dist_sensor is None:
        return None     # If the distance sensor is not available, return None to indicate we cannot read the water level
    try:
        # Read the distance from the sensor, convert it to water level by subtracting from the sensor height, and return the result in cm.
        distance_cm = _dist_sensor.distance * 100
        level = SENSOR_HEIGHT_CM - distance_cm
        return round(max(level, 0.0), 2)        # Ensure we don't return negative water levels if the distance exceeds the sensor height, 
                                                # and round to 2 decimal places for cleaner output
    except Exception as e:
        print(f"[ERROR] Water level read failed: {e}")
        return None     # If there's an error reading the distance, return None to indicate we cannot read the water level