# Code to run in a square. Connection string looks for a vehicle connected by serial port.
# To do: done.

import exceptions
import math
connection_string = "/dev/ttyAMA0"

from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
import socket

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))

try:
    vehicle = connect(connection_string, baud=115200, wait_ready=True, heartbeat_timeout=15)

# Bad TCP connection
except socket.error:
    print 'No server exists!'

# Bad TTY connection
except exceptions.OSError as e:
    print 'No serial exists!'

# API Error
except APIException:
    print 'Timeout!'

# Other error
except:
    print 'Some other error!'

# Get some vehicle attributes (state)
print "Get some vehicle attribute values:"
print " GPS: %s" % vehicle.gps_0
print " Battery: %s" % vehicle.battery
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Mode: %s" % vehicle.mode.name    # settable

print "Basic pre-arm checks"
# Don't try to arm until autopilot is ready
while not vehicle.is_armable:
    print " Waiting for vehicle to initialise..."
    time.sleep(1)
     
print "Arming motors"
# Copter should arm in GUIDED mode
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True    
# Confirm vehicle armed before attempting to take off
while not vehicle.armed:      
    print " Waiting for arming..."
    time.sleep(1)
print "Taking off!"
aTargetAltitude = 30
vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
# Wait until the vehicle reaches a safe height
i = 0
while i < 20:
    i += 1
    print " Altitude: ", vehicle.location.global_relative_frame.alt 
    #Break and return from function just below target altitude.        
    if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
        print "Reached target altitude"
        break
    time.sleep(1)

currentlocation = vehicle.location.global_relative_frame
# store location at launch to output locations relative to it later
launchloc=currentlocation
print "Location: ", currentlocation.lon, " ", currentlocation.lat, " ", currentlocation.alt
# set speed
print "Set default/target airspeed to 10"
vehicle.airspeed = 10

# First leg

print "Acquiring Coordinates..."
z = currentlocation.alt
x = 20
y = 0
print "Coordinates acquired: ", x, ", ", y, ", ", z
# convert coordinates from feet relative to drone to global latitude and longitude
xfactor=1/298171.5253016029
yfactor=1/363999.33433628065
x2=(x*xfactor)+currentlocation.lon
y2=(y*yfactor)+currentlocation.lat
print "Coordinates refactored: ", x2, ", ", y2, ", ", z, "; deploying"
coords=LocationGlobalRelative(y2, x2, z)
print "Going to: ", (coords.lon-launchloc.lon)/xfactor, ", ", (coords.lat-launchloc.lat)/yfactor, ", ", coords.alt-launchloc.alt
currentlocation = vehicle.location.global_relative_frame
# print location, first in global lat and lon, then in feet from drone
print "Location: ", currentlocation.lon, " ", currentlocation.lat, " ", currentlocation.alt, " Rloc: ", (currentlocation.lon-launchloc.lon)/xfactor, ", ", (currentlocation.lat-launchloc.lat)/yfactor, ", ", currentlocation.alt-launchloc.alt
# begin travelling to target
vehicle.simple_goto(coords)
# loop to output location to track progress
i=0
while i<18:
    time.sleep(0.5)
    currentlocation = vehicle.location.global_relative_frame
    print "Location: ", currentlocation.lon, " ", currentlocation.lat, " ", currentlocation.alt, " Rloc: ", (currentlocation.lon-launchloc.lon)/xfactor, ", ", (currentlocation.lat-launchloc.lat)/yfactor, ", ", currentlocation.alt-launchloc.alt
    i=i+1

# Second leg

print "Acquiring Coordinates..."
z = currentlocation.alt
x = 0
y = 20
print "Coordinates acquired: ", x, ", ", y, ", ", z
# convert coordinates from feet relative to drone to global latitude and longitude
x2=(x*xfactor)+currentlocation.lon
y2=(y*yfactor)+currentlocation.lat
print "Coordinates refactored: ", x2, ", ", y2, ", ", z, "; deploying"
coords=LocationGlobalRelative(y2, x2, z)
print "Going to: ", (coords.lon-launchloc.lon)/xfactor, ", ", (coords.lat-launchloc.lat)/yfactor, ", ", coords.alt-launchloc.alt
currentlocation = vehicle.location.global_relative_frame
# print location, first in global lat and lon, then in feet from drone
print "Location: ", currentlocation.lon, " ", currentlocation.lat, " ", currentlocation.alt, " Rloc: ", (currentlocation.lon-launchloc.lon)/xfactor, ", ", (currentlocation.lat-launchloc.lat)/yfactor, ", ", currentlocation.alt-launchloc.alt
# begin travelling to target
vehicle.simple_goto(coords)
# loop to output location to track progress
i=0
while i<18:
    time.sleep(0.5)
    currentlocation = vehicle.location.global_relative_frame
    print "Location: ", currentlocation.lon, " ", currentlocation.lat, " ", currentlocation.alt, " Rloc: ", (currentlocation.lon-launchloc.lon)/xfactor, ", ", (currentlocation.lat-launchloc.lat)/yfactor, ", ", currentlocation.alt-launchloc.alt
    i=i+1

# Third leg

print "Acquiring Coordinates..."
z = currentlocation.alt
x = -20
y = 0
print "Coordinates acquired: ", x, ", ", y, ", ", z
# convert coordinates from feet relative to drone to global latitude and longitude
x2=(x*xfactor)+currentlocation.lon
y2=(y*yfactor)+currentlocation.lat
print "Coordinates refactored: ", x2, ", ", y2, ", ", z, "; deploying"
coords=LocationGlobalRelative(y2, x2, z)
print "Going to: ", (coords.lon-launchloc.lon)/xfactor, ", ", (coords.lat-launchloc.lat)/yfactor, ", ", coords.alt-launchloc.alt
currentlocation = vehicle.location.global_relative_frame
# print location, first in global lat and lon, then in feet from drone
print "Location: ", currentlocation.lon, " ", currentlocation.lat, " ", currentlocation.alt, " Rloc: ", (currentlocation.lon-launchloc.lon)/xfactor, ", ", (currentlocation.lat-launchloc.lat)/yfactor, ", ", currentlocation.alt-launchloc.alt
# begin travelling to target
vehicle.simple_goto(coords)
# loop to output location to track progress
i=0
while i<18:
    time.sleep(0.5)
    currentlocation = vehicle.location.global_relative_frame
    print "Location: ", currentlocation.lon, " ", currentlocation.lat, " ", currentlocation.alt, " Rloc: ", (currentlocation.lon-launchloc.lon)/xfactor, ", ", (currentlocation.lat-launchloc.lat)/yfactor, ", ", currentlocation.alt-launchloc.alt
    i=i+1

# Last leg

print "Returning to Launch"
vehicle.mode = VehicleMode("RTL")
i=0
while i<18:
    time.sleep(0.5)
    currentlocation = vehicle.location.global_relative_frame
    print "Location: ", currentlocation.lon, " ", currentlocation.lat, " ", currentlocation.alt, " Rloc: ", (currentlocation.lon-launchloc.lon)/xfactor, ", ", (currentlocation.lat-launchloc.lat)/yfactor, ", ", currentlocation.alt-launchloc.alt
    i=i+1

# Land

print "Landing"
vehicle.mode = VehicleMode("LAND")
while i<18:
    time.sleep(0.5)
    currentlocation = vehicle.location.global_relative_frame
    print "Location: ", currentlocation.lon, " ", currentlocation.lat, " ", currentlocation.alt, " Rloc: ", (currentlocation.lon-launchloc.lon)/xfactor, ", ", (currentlocation.lat-launchloc.lat)/yfactor, ", ", currentlocation.alt-launchloc.alt
    i=i+1

# End Flight Code



# Close vehicle object before exiting script
vehicle.close()
