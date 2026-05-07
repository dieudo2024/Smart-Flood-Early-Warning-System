# input/fan.py
from gpiozero import Button, Motor
import threading
import time

_motor = Motor(forward=27, backward=6)  # GPIO pins for the motor driver
gate_button = Button(16)    # GPIO pin for the gate control button
_root = None    # Placeholder for the Tkinter root window, will be set in init() function
speed = 0.2     # Speed value for the motor (0 to 1), adjust as needed for your specific motor and application
_manual_override = False    # Flag to indicate if manual override is active, starts as False
_manual_state = None    # Variable to track the manual state of the fan (True for on, False for off), used when manual override is active
_override_timeout = 30  # seconds, set to None for indefinite

def init(root):     # Function to initialize the fan module with the Tkinter root window
    global _motor, _root

    _root = root        # Store the root window for scheduling tasks

def set_on(on=False, speed_val=speed):      # Function to set the fan on or off, with respect to manual override
    """Set fan on/off. Respects manual override from button."""

    if _motor is None:  # Motor not initialized, cannot control fan
        return
    
    # Prioritize manual button override
    if _manual_override:
        # Manual state is already set, don't override it
        return

    if on:
        # If turning on, ensure we stop any reverse motion first to prevent damage, then start the fan
        _motor.forward(speed=speed_val)
    else:
        stop_with_reverse(speed_val)    # Stop the fan with a brief reverse motion to brake faster when turning off

def stop_with_reverse(speed_val=speed, reverse_time=1.0):       # Function to stop the fan with a brief reverse motion to brake faster
    """Stop the fan with a brief reverse motion to brake faster."""

    if _motor is None or not _motor.is_active:
        return  # If the motor is not initialized or already stopped, do nothing
    
    # Start reverse motion
    _motor.backward(speed_val)
    
    # Schedule stop after reverse_time seconds
    if _root is not None:
        _root.after(int(reverse_time * 1000), _motor.stop)

def toggle():
    """Toggle fan and enable manual override."""
    global _manual_override, _manual_state
    
    # If the motor is currently active, we want to stop it with reverse breaking. 
    # If it's not active, we want to start it. This allows the button to toggle the state of the fan.
    if _motor.is_active:
        stop_with_reverse(speed, 2.0)  # 2 second reverse brake
        _manual_state = False
    else:
        _motor.forward(speed=speed)     # Start the fan at the configured speed
        _manual_state = True            # Set manual state to True when the fan is turned on by the button
    
    # Enable manual override
    _manual_override = True
    
    # Schedule timeout to reset override
    if _override_timeout is not None and _root is not None:
        _root.after(_override_timeout * 1000, reset_override)

def reset_override():
    """Reset manual override after timeout."""
    global _manual_override
    _manual_override = False

gate_button.when_pressed = toggle
