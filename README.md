# SmartBar
The Smart Bar is a prototype IoT barbell that has the potential to enhance your workout through the magic of data analytics. Using a gyroscope and an accelerometer the smart bar can automatically count your reps, display rep speed, and make sure your strength is symmetrical. The Smart Bar has an accompanying Android app and access to a website for in-depth analysis.

# How it Works
The Arduino 101 sends 6 space seperated values to the Raspberry Pi over USB Serial, 3 gyroscope values and 3 accelerometer values. The Raspberry Pi interprets the incoming data. The following graph is an example of some of our accelerometer sample dating showing acceleration on the three axes', the yellow line being the Z axis that was the primary axis used. 
![Acceleration Data](https://raw.githubusercontent.com/KevinAiken/Smart-Bar/master/image1.PNG)
![Velocity](https://raw.githubusercontent.com/KevinAiken/Smart-Bar/master/image2.png)
![Position](https://raw.githubusercontent.com/KevinAiken/Smart-Bar/master/image3.png)
Our code determines if a repetition has been completed by following the acceleration pattern of the rep through a series of while loops. A typical overhead press rep starts with 1g of acceleration on the Z axis. The acceleration is then over 1g for approximately half of the time the barbell is rising. As the barbell nears the top of the range of motion there is negative acceleration. Finally, at the top there may or may not be a brief pause where there is 1g of acceleration. There is then a negative acceleration. Finally, at the bottom of the rep there is a positive acceleration. The force on the Z axis then returns to 1g at the end as the bar is stopped on the lifters chest.



# Hardware
  * Broom
  * Raspberry Pi 3
  * Arduino 101 
  * Android Phone
  
# Software
  * AWS server running Python backend using the flask framework and a PostgreSQL database
  * C script running on the Arduino 101
  * Python script running on the Raspberry Pi
  * Android App programmed in Java
  

