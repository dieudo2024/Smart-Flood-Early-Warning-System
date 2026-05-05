# input/fan.py
from gpiozero import Motor

_motor = None

def init(forward_pin = 27, backward_pin = 6):
    global _motor
    _motor = Motor(forward=forward_pin, backward=backward_pin)

def set_on(on, speed=0.8):
    if _motor is None:
        return
    if on:
        _motor.forward(speed=speed)
    else:
        _motor.stop()