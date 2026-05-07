# Smart-Flood-Early-Warning-System

### Context
Every year during the spring season, the rising temperature causes the accumulated snow to melt rapidly, leading to a significant increase in water levels in rivers and surrounding areas. This often results in flooding, which can cause extensive damage to the environment and disrupt daily life by forcing school closures, interrupting transportation, and displacing communities.
The development of Internet of Things (IoT) offers a proactive approach to this problem. By using automated systems, it is possible to continuously monitor the increasing levels of water and temperature in real time. These systems can detect early warning signs of flooding and trigger protective measures before the damage occurs. For example, automated barriers or flood gates can be deployed as soon as risk level rise, reducing the impact on affected areas. 

### Objective
The objective of this project is to design and implement an IoT system that can monitor water levels and temperature to evaluate potential flood risks. The system will provide real-time alerts to users when a potentially dangerous condition is detected. In addition, it will automatically activate a motorized flood gate to prevent of limit water intrusion. By combining early detection with automated response, the system aims to minimize damage, improve safety, and enhance preparedness in flood-prone areas.
 
### HW Components
<img width="1567" height="930" alt="Hardware components list" src="https://github.com/user-attachments/assets/624a177d-8cb6-4798-a987-44fc095668bf" />
  
### System Architecture
<img width="1687" height="840" alt="image" src="https://github.com/user-attachments/assets/ce828edc-e72d-4438-8ddd-f8cba3260700" />

### GUI (image)
<img width="591" height="342" alt="System GUI" src="https://github.com/user-attachments/assets/09c88f16-129e-43bc-b8e4-8ca5511abc84" />

### Installation instructions
1. Clone this repository onto your Raspberry Pi and navigate into the project folder.
2. Connect all the hardware components as per the circuit diagram (Ultrasonic sensor, DS18B20 temperature sensor, LEDs, Buzzer, Buttons, and Fan).
3. Install the required Python dependencies if not already installed.
4. Launch the GUI by running the Flood_Monitoring_System_GUI_support.py file.
5. Check GUI and verify that it shows: State, Water level, Temperature, Flood threshold, and Buttons.
6. Test the functionality of the buttons (Silence the buzzer, Manually control fan). Optional, adjust the flood threshold using the rotary encoder.
7. Simulate rising water levels to confirm that LEDs, the buzzer, and fan respond correctly according to the set states.
8. When finished, close the GUI window to stop the program.

# User Manual
### What Does the System Do? 

The project is an IoT system that monitors the temperature and water level, evaluating flood risk, warning users locally, and automatically activates a flood gate when there’s risk.  

### Monitoring System Display (GUI): 

It displays the current state, the sensor data for water level, temperature, and the threshold. It also has buttons to manually control the buzzer and the fan. 

### Project Hardware and Their Functionality  

LEDs – used for states 

- Blue LED: Normal 

- Yellow LED:  Warning 

- Red LED: Flood Risk (Critical) 

Buttons – used to control the buzzer (alarm) and fan (gate) 

- Red Button: Used to silence the buzzer 

- Blue Button: Used to manually control the fan (gate) 

Active Buzzer – audible flood alert 

- Normal state: Buzzer is off 

- Warning state: Buzzer beeps every 2 seconds 

- Flood risk state (Critical state): Buzzer continuously beeps 

Ultrasonic Distance Sensor Module – detects rising water, measures distance 

DC Motor Module – represents automated gate closure. 

Can be manually controlled using the Blue button at any time (turns off/on the fan). 

- Normal state: Fan is off 

- Warning state: Fan is off 

- Flood risk state: Fan automatically turns on 

Temperature - checks the current temperature 

Rotary Encoder Module – allows user to modify the flood threshold (default is set to 10 for Flood risk and 5 for Warning) 

- Increase threshold: rotate the rotary encoder clockwise 

- Decrease threshold: rotate the rotary encoder counterclockwise 

### How Does the System Work? 
The Distance Sensor detects the water level or distance and evaluates flood risk to warn users and activates flood gate. The default state of the program is NORMAL and has a WARNING level at 5 cm, and CRITICAL level of at 10cm. 

#### When on NORMAL: 

Distance is less than 5cm 

Blue LED is turned on 

Buzzer is off 

#### When on WARNING: 

Distance is between 5cm to 10cm 

Yellow LED is turn on 

Buzzer beeps every 2 seconds 

#### When on CRITICAL: 

Distance is greater than 10cm 

Red LED is turned on 

Buzzer beeps continuously 

Fan turns on 

##
The buzzer can be silenced at any time using the Red Button or the “Silence Alarm” button on the GUI for both WARNING and CRITICAL states. 

The fan can be turned on/off at any time using the Blue Button or the “Manually Control Gate” on the GUI regardless of the state. 

Rotary Encoder can be used to change the default distance levels. For example, if the flood threshold is set to 20cm:  

- NORMAL state will be triggered from 0cm to 10cm 

- WARNING state will be triggered from 10cm to 20cm 

- CRITICAL state will be triggered when it exceeds 20cm 
