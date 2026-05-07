from gpiozero import RotaryEncoder

rotor = RotaryEncoder(19, 13)
base_threshold = 10 

def increase():
    global base_threshold
    base_threshold = base_threshold + 0.01
    print(f"Threshold increased to: {base_threshold:.2f} cm")
def decrease():
    global base_threshold
    base_threshold = base_threshold - 0.01
    print(f"Threshold decreased to: {base_threshold:.2f} cm")
    
def get_threshold():
    
    rotor.when_rotated_clockwise = increase
    rotor.when_rotated_counter_clockwise = decrease
    set_threshold(base_threshold)
    return base_threshold

def set_threshold(value):
    global base_threshold
    base_threshold = value