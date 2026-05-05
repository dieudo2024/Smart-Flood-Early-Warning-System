from gpiozero import Buzzer, Button

# Buzzer setup
buzzer = Buzzer(17)

silence_button = Button(12)


def silence_alarm():
    # Called when "Silence Alarm" button is pressed
    global buzzer_silenced
    buzzer_silenced = True
    buzzer.off()
    # print("[BUZZER] Silenced by user.")

silence_button.when_pressed = silence_alarm


# Becomes True when "Silence Alarm" button is pressed
buzzer_silenced = False
_beep_running = False

def _warning_beep(current_state, root):
    global _beep_running

    # Stops the beep loop
    if current_state != "WARNING" or buzzer_silenced:
        _beep_running = False
        buzzer.off()
        return

    buzzer.on()                         
    root.after(200, buzzer.off)          
    root.after(2000, _warning_beep)     





def reset_silence():
    buzzer.off()