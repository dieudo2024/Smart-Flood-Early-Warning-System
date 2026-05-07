# input/fan.py
from gpiozero import Button, Motor
import threading
import time

_motor = Motor(forward=27, backward=6)
gate_button = Button(16)
_root = None
speed = 0.2
_manual_override = False
_manual_state = None
_override_timeout = 30  # seconds, set to None for indefinite

def init(root):
    global _motor, _root
    _root = root

def set_on(on=False, speed_val=speed):
    """Set fan on/off. Respects manual override from button."""
    if _motor is None:
        return
    
    # Prioritize manual button override
    if _manual_override:
        # Manual state is already set, don't override it
        return
    
    # No manual override, apply automatic control
    if on:
        _motor.forward(speed=speed_val)
    else:
        stop_with_reverse(speed_val)

def stop_with_reverse(speed_val=speed, reverse_time=1.0):
    """Stop the fan with a brief reverse motion to brake faster."""
    if _motor is None or not _motor.is_active:
        return
    
    # Start reverse motion
    _motor.backward(speed_val)
    
    # Schedule stop after reverse_time seconds
    if _root is not None:
        _root.after(int(reverse_time * 1000), _motor.stop)

def toggle():
    """Toggle fan and enable manual override."""
    global _manual_override, _manual_state
    
    if _motor.is_active:
        stop_with_reverse(speed, 2.0)  # 2 second reverse brake
        _manual_state = False
    else:
        _motor.forward(speed=speed)
        _manual_state = True
    
    # Enable manual override
    _manual_override = True
    
    # Schedule timeout to reset override (if configured)
    if _override_timeout is not None and _root is not None:
        _root.after(_override_timeout * 1000, reset_override)

def reset_override():
    """Reset manual override after timeout."""
    global _manual_override
    _manual_override = False

gate_button.when_pressed = toggle
