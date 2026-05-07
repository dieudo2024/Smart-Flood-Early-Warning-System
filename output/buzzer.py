from shutil import which

from gpiozero import Buzzer, Button
 
# Buzzer setup
_buzzer = Buzzer(17)    # GPIO pin for the buzzer
silence_button = Button(12) # GPIO pin for the silence button
 
# Becomes True when "Silence Alarm" button or GUI button is pressed
buzzer_silenced = False # Flag to track if the buzzer is silenced
_beep_running = False   # Flag to track if the warning beep is currently running

_root = None    # Placeholder for the Tkinter root window, will be set in init() function
 
current_state = "NORMAL"    # Variable to track the current state of the system (NORMAL, WARNING, CRITICAL)
silenced_state = None   # Variable to track the state at which the buzzer was silenced, used to prevent re-silencing if the state changes while silenced
_previous_state = "NORMAL"  # Variable to track the previous state, used to detect state changes and update the buzzer accordingly
 
 
def init(root): # Function to initialize the buzzer module with the Tkinter root window
    global _root
    _root = root

def update_buzzer():
    global _beep_running, _previous_state, silenced_state   # Declare global variables to modify them within the function
 
    if buzzer_silenced and current_state != silenced_state: # If the buzzer is silenced but the state has changed since it was silenced, reset the silence
        reset_silence()
 
    if buzzer_silenced:     # If the buzzer is silenced, ensure it stays off and schedule the next check
        _buzzer.off()
        _root.after(500, update_buzzer) # Schedule the next check after 500ms
        return
 
    if current_state == "NORMAL":       # If the state is NORMAL, ensure the buzzer is off and stop any warning beeps
        _buzzer.off()                   # Ensure buzzer is off in NORMAL state
        _beep_running = False           # Stop any warning beeps if we return to NORMAL state
 
    elif current_state == "WARNING":    # If the state is WARNING, start the warning beep if it's not already running
        
        _buzzer.off()               # Ensure buzzer is off before starting the warning beep pattern
        if not _beep_running:       # Only start the warning beep pattern if it's not already running to avoid multiple overlapping beeps
            _beep_running = True    # Set the flag to indicate the warning beep is running
            _warning_beep()     # Start the warning beep pattern, which will continue to call itself every 2 seconds until the state changes or the buzzer is silenced

    else:
        _beep_running = False       # Stop any warning beeps if we enter CRITICAL state, as the buzzer will be continuously on
        _buzzer.on()                # In CRITICAL state, the buzzer should be continuously on
 
    _previous_state = current_state # Update the previous state to the current state for the next check
    _root.after(500, update_buzzer) # Schedule the next check after 500ms to continuously monitor the state and update the buzzer accordingly
 
 
def _warning_beep():    # Function to handle the warning beep pattern, which beeps every 2 seconds when in WARNING state
    global _beep_running
 
    if current_state != "WARNING" or buzzer_silenced:   # If the state is no longer WARNING or the buzzer has been silenced, stop the warning beep pattern
        _beep_running = False
        _buzzer.off()       # Ensure the buzzer is off when stopping the warning beep pattern
        return
 
    _buzzer.on()        # Turn the buzzer on for the warning beep
    _root.after(200, _buzzer.off)       # Schedule the buzzer to turn off after 200ms for a short beep
    _root.after(2000, _warning_beep)    # Schedule the next warning beep after 2 seconds, 
                                        # creating a continuous beep pattern while in WARNING state
 
def silence_alarm():        # Function to handle silencing the alarm when the silence button is pressed, 
                            # which sets the buzzer_silenced flag and turns off the buzzer
    global buzzer_silenced  # Declare global variable to modify it within the function
    global _beep_running    # Declare global variable to modify it within the function
    global silenced_state   # Declare global variable to modify it within the function

    buzzer_silenced = True  # Set the flag to indicate the buzzer is silenced
    silenced_state = current_state  # Record the state at which the buzzer was silenced to prevent re-silencing if the state changes while silenced
    _buzzer.off()   # Ensure the buzzer is turned off when silenced
    print("[BUZZER] Silenced by user.")     # Print a message to the console indicating the buzzer has been silenced by the user
    _beep_running = False       # Stop any warning beeps when the alarm is silenced

def reset_silence():
    global buzzer_silenced
    global silenced_state

    buzzer_silenced = False     # Reset the flag to indicate the buzzer is no longer silenced
    silenced_state = None       # Reset the silenced state to None since the buzzer is no longer silenced 

silence_button.when_pressed = silence_alarm     # Set the function to be called when the silence button is pressed, which will silence the alarm and update the buzzer state accordingly