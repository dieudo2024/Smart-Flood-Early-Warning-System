import os
import time


def read_temp():
    """Read temperature from DS18B20 sensor. Returns temperature in Celsius or None if there's an error."""
    try:
        device_folder = "/sys/bus/w1/devices/"      # Base directory where 1-wire devices are listed in the Linux filesystem

        devs = []       # List to hold the device directories for DS18B20 sensors, which start with "28-"
        for name in os.listdir(device_folder):      # Iterate through the device directories in the base directory
            if name.startswith("28-"):              # If the directory name starts with "28-", it's a DS18B20 sensor, so we add it to the list of devices
                devs.append(name)                   # Add the device directory to the list of devices

        if not devs:
            return None         # If no DS18B20 sensor is found, return None to indicate we cannot read the temperature
        
        sensor_file = os.path.join(device_folder, devs[0], "w1_slave")      # Construct the path to the sensor's data file, 
                                                                            # using the first device found (devs[0]) since we only expect one sensor
        with open(sensor_file, "r") as f:       # Open the sensor's data file for reading
            lines = f.readlines()       # Read the lines from the sensor's data file, which contains the raw data from the sensor.

        if len(lines) < 2:      # If the sensor data file doesn't contain at least 2 lines, it's not in the expected format, 
                                # so we return None to indicate we cannot read the temperature
            return None
        if "YES" not in lines[0]: # If the first line of the sensor data doesn't contain "YES", indicate a CRC check failure, meaning the data is not valid,
            return None
        if "t=" not in lines[1]:    # If the second line of the sensor data doesn't contain "t=", it doesn't have the temperature data in the expected format,
            return None

        # Extract the temperature value from the second line of the sensor data
        temp_string = lines[1].split("t=")[-1].strip()
        temp_c = float(temp_string) / 1000

        # Return the temperature in Celsius. The raw value from the sensor is in thousandths of a degree, 
        # so we divide by 1000 to get the actual temperature in Celsius.
        return temp_c
    
    except OSError: 
        # OSError can occur if there's an issue with the sensor or the file system, such as the sensor being disconnected.
        print("[ERROR] OSError occurred while reading temperature.")
        return None

def loop():
    """Loop to continuously read and print the temperature every 3 seconds. Press Ctrl+C to stop."""
    print("=== DS18B20 Temperature Reader ===")

    try:
        while True: # Loop indefinitely to read and print the temperature every 3 seconds until interrupted by the user (e.g., by pressing Ctrl+C)
            temp_c = read_temp()
            if temp_c is None:      # If the temperature reading is None, it indicates an error occurred while reading the temperature, so we print an error message and continue to the next iteration of the loop to try reading again.
                print("[ERROR] Could not read temperature (None). Retrying...")
            else:
                print(f"Temperature: {temp_c:.3f} °C")
            time.sleep(3.0)     # Sleep for 3 seconds before reading the temperature
    except KeyboardInterrupt:
        print("\nStopping reader. Goodbye!")