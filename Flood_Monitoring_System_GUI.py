import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path

_location = os.path.dirname(__file__)

import Flood_Monitoring_System_GUI_support

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 

_style_code_ran = 0
def _style_code():
    global _style_code_ran
    if _style_code_ran: return        
    try: Flood_Monitoring_System_GUI_support.root.tk.call('source',
                os.path.join(_location, 'themes', 'default.tcl'))
    except: pass
    style = ttk.Style()
    style.theme_use('default')
    style.configure('.', font = "TkDefaultFont")
    if sys.platform == "win32":
       style.theme_use('winnative')    
    _style_code_ran = 1

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("474x247+486+378")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(1,  1)
        top.title("Flood Monitoring System")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")

        self.top = top

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        ########### start #######################
        ########### end #######################

        self.stateTextLabel = tk.Label(self.top)
        self.stateTextLabel.place(relx=0.295, rely=0.121, height=28, width=59)
        self.stateTextLabel.configure(activebackground="#d9d9d9")
        self.stateTextLabel.configure(activeforeground="black")
        self.stateTextLabel.configure(anchor='w')
        self.stateTextLabel.configure(background="#d9d9d9")
        self.stateTextLabel.configure(compound='left')
        self.stateTextLabel.configure(disabledforeground="#a3a3a3")
        self.stateTextLabel.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.stateTextLabel.configure(foreground="black")
        self.stateTextLabel.configure(highlightbackground="#d9d9d9")
        self.stateTextLabel.configure(highlightcolor="#000000")
        self.stateTextLabel.configure(text='''State:''')

        self.stateLabel = tk.Label(self.top)
        self.stateLabel.place(relx=0.443, rely=0.121, height=28, width=167)
        self.stateLabel.configure(activebackground="#d9d9d9")
        self.stateLabel.configure(activeforeground="black")
        self.stateLabel.configure(anchor='w')
        self.stateLabel.configure(background="#00ff00")
        self.stateLabel.configure(compound='center')
        self.stateLabel.configure(cursor="fleur")
        self.stateLabel.configure(disabledforeground="#a3a3a3")
        self.stateLabel.configure(font="-family {Times New Roman} -size 12 -weight bold")
        self.stateLabel.configure(foreground="black")
        self.stateLabel.configure(highlightbackground="#d9d9d9")
        self.stateLabel.configure(highlightcolor="#000000")
        self.stateLabel.configure(padx="40")
        self.stateLabel.configure(text='''NORMAL''')

        self.waterLevelTextLabel = tk.Label(self.top)
        self.waterLevelTextLabel.place(relx=0.084, rely=0.405, height=28
                , width=93)
        self.waterLevelTextLabel.configure(activebackground="#d9d9d9")
        self.waterLevelTextLabel.configure(activeforeground="black")
        self.waterLevelTextLabel.configure(anchor='w')
        self.waterLevelTextLabel.configure(background="#d9d9d9")
        self.waterLevelTextLabel.configure(compound='left')
        self.waterLevelTextLabel.configure(disabledforeground="#a3a3a3")
        self.waterLevelTextLabel.configure(foreground="black")
        self.waterLevelTextLabel.configure(highlightbackground="#d9d9d9")
        self.waterLevelTextLabel.configure(highlightcolor="#000000")
        self.waterLevelTextLabel.configure(text='''Water Level:''')

        self.waterLevelLabel = tk.Label(self.top)
        self.waterLevelLabel.place(relx=0.338, rely=0.405, height=28, width=104)
        self.waterLevelLabel.configure(activebackground="#d9d9d9")
        self.waterLevelLabel.configure(activeforeground="black")
        self.waterLevelLabel.configure(anchor='w')
        self.waterLevelLabel.configure(background="#d9d9d9")
        self.waterLevelLabel.configure(compound='left')
        self.waterLevelLabel.configure(disabledforeground="#a3a3a3")
        self.waterLevelLabel.configure(foreground="black")
        self.waterLevelLabel.configure(highlightbackground="#d9d9d9")
        self.waterLevelLabel.configure(highlightcolor="#000000")
        self.waterLevelLabel.configure(text='''6.3 cm''')

        self.temperatureTextLabel = tk.Label(self.top)
        self.temperatureTextLabel.place(relx=0.084, rely=0.567, height=28
                , width=93)
        self.temperatureTextLabel.configure(activebackground="#d9d9d9")
        self.temperatureTextLabel.configure(activeforeground="black")
        self.temperatureTextLabel.configure(anchor='w')
        self.temperatureTextLabel.configure(background="#d9d9d9")
        self.temperatureTextLabel.configure(compound='left')
        self.temperatureTextLabel.configure(disabledforeground="#a3a3a3")
        self.temperatureTextLabel.configure(foreground="black")
        self.temperatureTextLabel.configure(highlightbackground="#d9d9d9")
        self.temperatureTextLabel.configure(highlightcolor="#000000")
        self.temperatureTextLabel.configure(text='''Temperature:''')

        self.temperatureLabel = tk.Label(self.top)
        self.temperatureLabel.place(relx=0.338, rely=0.567, height=28, width=100)

        self.temperatureLabel.configure(activebackground="#d9d9d9")
        self.temperatureLabel.configure(activeforeground="black")
        self.temperatureLabel.configure(anchor='w')
        self.temperatureLabel.configure(background="#d9d9d9")
        self.temperatureLabel.configure(compound='left')
        self.temperatureLabel.configure(disabledforeground="#a3a3a3")
        self.temperatureLabel.configure(foreground="black")
        self.temperatureLabel.configure(highlightbackground="#d9d9d9")
        self.temperatureLabel.configure(highlightcolor="#000000")
        self.temperatureLabel.configure(text='''3.7 °C''')

        self.thresholdTextLabel = tk.Label(self.top)
        self.thresholdTextLabel.place(relx=0.084, rely=0.729, height=31
                , width=94)
        self.thresholdTextLabel.configure(activebackground="#d9d9d9")
        self.thresholdTextLabel.configure(activeforeground="black")
        self.thresholdTextLabel.configure(anchor='w')
        self.thresholdTextLabel.configure(background="#d9d9d9")
        self.thresholdTextLabel.configure(compound='left')
        self.thresholdTextLabel.configure(disabledforeground="#a3a3a3")
        self.thresholdTextLabel.configure(foreground="black")
        self.thresholdTextLabel.configure(highlightbackground="#d9d9d9")
        self.thresholdTextLabel.configure(highlightcolor="#000000")
        self.thresholdTextLabel.configure(text='''Flood threshold:''')

        self.thresholdLabel = tk.Label(self.top)
        self.thresholdLabel.place(relx=0.338, rely=0.729, height=31, width=104)
        self.thresholdLabel.configure(activebackground="#d9d9d9")
        self.thresholdLabel.configure(activeforeground="black")
        self.thresholdLabel.configure(anchor='w')
        self.thresholdLabel.configure(background="#d9d9d9")
        self.thresholdLabel.configure(compound='left')
        self.thresholdLabel.configure(disabledforeground="#a3a3a3")
        self.thresholdLabel.configure(foreground="black")
        self.thresholdLabel.configure(highlightbackground="#d9d9d9")
        self.thresholdLabel.configure(highlightcolor="#000000")
        self.thresholdLabel.configure(text='''10 cm''')

        _style_code()
        self.alarmButton = ttk.Button(self.top)
        self.alarmButton.place(relx=0.591, rely=0.445, height=36, width=145)
        self.alarmButton.configure(takefocus="")
        self.alarmButton.configure(text='''Silence Alarm''')
        self.alarmButton.configure(compound='left')

        self.gateButton = ttk.Button(self.top)
        self.gateButton.place(relx=0.591, rely=0.688, height=36, width=145)
        self.gateButton.configure(takefocus="")
        self.gateButton.configure(text='''Manually Control Gate''')
        self.gateButton.configure(compound='left')

def start_up():
    Flood_Monitoring_System_GUI_support.main()

if __name__ == '__main__':
    Flood_Monitoring_System_GUI_support.main()

