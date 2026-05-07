from gpiozero import Buzzer, Button
 
# Buzzer setup
_buzzer = Buzzer(17)    
silence_button = Button(12)
 
# Becomes True when "Silence Alarm" button or GUI button is pressed
buzzer_silenced = False
_beep_running = False
 
# root is passed in from support file via init() because
# root.after() only works inside the Tkinter event loop
_root = None
 
current_state = "NORMAL"
silenced_state = None
_previous_state = "NORMAL"
 
 
def init(root):
    global _root
    _root = root
 
 
def update_buzzer():
    global _beep_running, _previous_state, silenced_state
 
    if buzzer_silenced and current_state != silenced_state:
        reset_silence()
 
    if buzzer_silenced:
        _buzzer.off()
        _root.after(500, update_buzzer)
        return
 
    if current_state == "NORMAL":
        _buzzer.off()
        _beep_running = False    
 
    elif current_state == "WARNING":
        
        _buzzer.off()              
        if not _beep_running:      
            _beep_running = True
            _warning_beep()
 
    else:
        _beep_running = False    
        _buzzer.on()            
 
    _previous_state = current_state
    _root.after(500, update_buzzer)
 
 
def _warning_beep():
    global _beep_running
 
    if current_state != "WARNING" or buzzer_silenced:
        _beep_running = False
        _buzzer.off()
        return
 
    _buzzer.on()
    _root.after(200, _buzzer.off)    
    _root.after(2000, _warning_beep)  
 
def silence_alarm():
    global buzzer_silenced
    global _beep_running
    global silenced_state
    buzzer_silenced = True
    silenced_state = current_state
    _buzzer.off()
    print("[BUZZER] Silenced by user.")
    _beep_running = False
 
def reset_silence():
    global buzzer_silenced
    global silenced_state
    buzzer_silenced = False
    silenced_state = None
    print("[BUZZER] Silence reset.")
 
 
silence_button.when_pressed = silence_alarm
 