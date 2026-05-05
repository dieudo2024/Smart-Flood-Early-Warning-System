import os
import time


def read_temp():
    try:
        device_folder = "/sys/bus/w1/devices/"

        devs = []
        for name in os.listdir(device_folder):
            if name.startswith("28-"):
                devs.append(name)
        if not devs:
            return None
        sensor_file = os.path.join(device_folder, devs[0], "w1_slave")
        with open(sensor_file, "r") as f:
            lines = f.readlines()

        if len(lines) < 2:
            return None
        if "YES" not in lines[0]:
            return None
        if "t=" not in lines[1]:
            return None

        temp_string = lines[1].split("t=")[-1].strip()
        temp_c = float(temp_string) / 1000

        return temp_c
    except OSError:
        print("[ERROR] OSError occurred while reading temperature.")
        return None

def loop():
    print("=== DS18B20 Temperature Reader ===")

    try:
        while True:
            temp_c = read_temp()
            if temp_c is None:
                print("[ERROR] Could not read temperature (None). Retrying...")
            else:
                print(f"Temperature: {temp_c:.3f} °C")
            time.sleep(3.0)
    except KeyboardInterrupt:
        print("\nStopping reader. Goodbye!")