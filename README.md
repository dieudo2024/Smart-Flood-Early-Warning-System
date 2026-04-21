# Smart-Flood-Early-Warning-System

### Context
Every year during the spring season, the rising temperature causes the accumulated snow to melt rapidly, leading to a significant increase in water levels in rivers and surrounding areas. This often results in flooding, which can cause extensive damage to the environment and disrupt daily life by forcing school closures, interrupting transportation, and displacing communities.
The development of Internet of Things (IoT) offers a proactive approach to this problem. By using automated systems, it is possible to continuously monitor the increasing levels of water and temperature in real time. These systems can detect early warning signs of flooding and trigger protective measures before the damage occurs. For example, automated barriers or flood gates can be deployed as soon as risk level rise, reducing the impact on affected areas. 

### Objective
The objective of this project is to design and implement an IoT system that can monitor water levels and temperature to evaluate potential flood risks. The system will provide real-time alerts to users when a potentially dangerous condition is detected. In addition, it will automatically activate a motorized flood gate to prevent of limit water intrusion. By combining early detection with automated response, the system aims to minimize damage, improve safety, and enhance preparedness in flood-prone areas.
 
### Features
 
### HW Components
<img width="1177" height="698" alt="Hardware components list" src="https://github.com/user-attachments/assets/d0baa5b3-da18-47f3-823d-5269020475e2" />

  
### System Architecture
  
### GUI (image)
<img width="591" height="342" alt="System GUI" src="https://github.com/user-attachments/assets/09c88f16-129e-43bc-b8e4-8ca5511abc84" />

### Installation instructions
1. Clone this repository onto your Raspberry Pi and navigate into the project folder.
2. Connect all the hardware components as per the circuit diagram (Ultrasonic sensor, DS18B20 temperature sensor, LEDs, Buzzer, Buttons, and Fan).
3. Install the required Python dependencies if not already installed.
4. Launch the GUI by running the thermostat_support.py file.
5. Check GUI and verify that it shows: State, Water level, Temperature, Flood threshold, and Buttons.
6. Test the functionality of the buttons (Silence the buzzer, Manually control fan). Optional, adjust the flood threshold using the rotary encoder.
7. Simulate rising water levels to confirm that LEDs, the buzzer, and fan respond correctly according to the set states.
8. When finished, close the GUI window to stop the program.
  
### User Manual
