from gpiozero import RotaryEncoder

rotor = RotaryEncoder(19, 13)
base_threshold = 10 

def get_threshold():
    return base_threshold + rotor.steps
