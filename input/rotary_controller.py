from gpiozero import RotaryEncoder

rotor = RotaryEncoder(19, 13)
base_threshold = 10 

def increase():
    global base_threshold
    base_threshold = base_threshold + 0.01

def decrease():
    global base_threshold
    base_threshold = base_threshold - 0.01

def get_threshold():
    # Checking if the rotary value is different from the last rotary value to avoid unnecessary updates
    rotor.when_rotated_clockwise = increase
    rotor.when_rotated_counter_clockwise = decrease

    return base_threshold

