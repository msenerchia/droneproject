# droneproject

"Pooper Trooper" Navigation Module

Project goal: modify a drone to fly autonomously, find humans in an open field, and drop raisins on them.

Module goal: issue instructions to drone to search field, interpret target location from infrared camera module, direct drone to target.

Current progress: drone takes off and flies, calculations for converting image position data to usable GPS coordinates are complete.

To be done: call image-collection code, call raisin-collection code, modify flight script to search an entire rectangular area.

Code is in Python, using Dronekit, and runs on the Raspberry Pi Zero on board the drone. After turning on the drone, SSH into the Pi (its IP address is 10.160.168.5) to run scripts.

Most instructions are here: http://ardupilot.org/dev/docs/raspberry-pi-via-mavlink.html

Important notes:

The Pi has several necessary packages installed on it. If they are ever deleted, the commands to install them are:

sudo apt-get update

sudo apt-get install screen python-wxgtk2.8 python-matplotlib python-opencv python-pip python-numpy python-dev libxml2-dev libxslt-dev

sudo pip install pymavlink

sudo pip install mavproxy

To install Dronekit itself:

sudo apt-get install python-serial python-pyparsing

sudo pip install droneapi

The OS control of the serial port on the Pi must also be disabled.

To ensure the Pi is connected to the drone, start Mavproxy using the following commands:

sudo -s

mavproxy.py --master=/dev/ttyAMA0 --baudrate 57600 --aircraft MyCopter

Do not attempt to run scripts when Mavproxy or a mission planner is running, and make sure that the vehicle is in "Guided" mode and that it is ready to arm. Mission planner software, of which several versions are available for download for different operating systems, is useful for debugging, but interferes with Dronekit scripts.


Files in this repository:

dronetest3.py: Basic test script, drone lifts off and lands.

dronetest4.py: Current version of full flight script, includes target-interpretation calculations.

dronetest5.py: Test script to fly in a square.

dronetest33.py: Alternate test script to fly in a square.
