from gpiozero import RotaryEncoder

rotor = RotaryEncoder(19, 13)   # GPIO pins for the rotary encoder
base_threshold = 10 # Initial threshold value in cm

def increase(): # Function to increase the threshold value
    global base_threshold   # Declare base_threshold as global to modify it within the function
    base_threshold = base_threshold + 0.01  # Increment the threshold by 0.01 cm for each clockwise rotation
    print(f"Threshold increased to: {base_threshold:.2f} cm")

def decrease(): # Function to decrease the threshold value
    global base_threshold   # Declare base_threshold as global to modify it within the function
    base_threshold = base_threshold - 0.01  # Decrement the threshold by 0.01 cm for each counter-clockwise rotation
    print(f"Threshold decreased to: {base_threshold:.2f} cm")
    
def get_threshold():
    
    rotor.when_rotated_clockwise = increase # Set the function to be called when the rotary encoder is rotated clockwise
    rotor.when_rotated_counter_clockwise = decrease # Set the function to be called when the rotary encoder is rotated counter-clockwise
    set_threshold(base_threshold)   # Initialize the threshold value
    return base_threshold

def set_threshold(value):   # Function to set the threshold value
    global base_threshold   # Declare base_threshold as global to modify it within the function
    base_threshold = value  # Update the base_threshold with the new value