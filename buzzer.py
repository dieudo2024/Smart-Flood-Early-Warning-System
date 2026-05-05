from gpiozero import Buzzer, Button

# Buzzer setup
buzzer = Buzzer(17)

silence_button = Button(12)
silence_button.when_pressed = silence_alarm


# Becomes True when "Silence Alarm" button is pressed
buzzer_silenced = False
_beep_running = False


def update_buzzer():
    global _beep_running

    # If the user silenced the alarm, keep buzzer off and check again in 500ms
    if buzzer_silenced:
        buzzer.off()
        root.after(5000, update_buzzer)
        return

    if current_state == "NORMAL":
        buzzer.off()      
        _beep_running = False

    elif current_state == "WARNING":
        buzzer.off()          
        if not _beep_running: # Starts one beep loop at a time
            _beep_running = True
            _warning_beep()   

    elif current_state == "FLOOD_RISK":
        _beep_running = False # Stops the warning beep loop
        buzzer.on()           # Flood risk sound

    root.after(5000, update_buzzer)


def _warning_beep():
    global _beep_running

    # Stops the beep loop
    if current_state != "WARNING" or buzzer_silenced:
        _beep_running = False
        buzzer.off()
        return

    buzzer.on()                         
    root.after(200, buzzer.off)          
    root.after(2000, _warning_beep)     


def silence_alarm():
    # Called when "Silence Alarm" button is pressed
    global buzzer_silenced
    buzzer_silenced = True
    buzzer.off()
    print("[BUZZER] Silenced by user.")


def reset_silence():
    # Called when state goes back to NORMAL
    global buzzer_silenced
    buzzer_silenced = False
    print("[BUZZER] Silence reset.")