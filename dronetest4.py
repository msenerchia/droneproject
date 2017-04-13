#Current version of target-seeking code. Currently set to run in SITL.
# To do: set to look for an actual vehicle, use connection code from dronetest3; script should enter LAND mode after returning to launch; script should search a rectangular area; integrate camera and dropper functionality.

# begin (mostly) borrowed code
print "Start simulator (SITL)"
# import dronekit
# import socket
import exceptions
import dronekit_sitl
import math
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))

try:
    vehicle = connect(connection_string, wait_ready=True, heartbeat_timeout=15)

# Bad TCP connection
except socket.error:
    print 'No server exists!'

# Bad TTY connection
except exceptions.OSError as e:
    print 'No serial exists!'

# API Error
except dronekit.APIException:
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

# Flight Code

# Takeoff

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
while True:
    print " Altitude: ", vehicle.location.global_relative_frame.alt 
    #Break and return from function just below target altitude.        
    if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
        print "Reached target altitude"
        break
    time.sleep(1)

# begin original code

currentlocation = vehicle.location.global_relative_frame
# store location at launch to output locations relative to it later
launchloc=currentlocation
print "Location: ", currentlocation.lon, " ", currentlocation.lat, " ", currentlocation.alt
# set speed
print "Set default/target airspeed to 10"
vehicle.airspeed = 10

# loop to look for targets
while True:
    print "Searching for Targets"
    # check camera for targets
    # If a target is found, break
    if True:
        print "Target found!"
        # format of target location from camera TBD, using dummy
        xdegrees = 15
        ydegrees = 10
        currentlocation = vehicle.location.global_relative_frame
        currentfacing = vehicle.attitude.yaw
        break
    time.sleep(1)
# acquire target position from camera
print "Acquiring Coordinates..."
z = currentlocation.alt
# determine location relative to drone position and facing
hcoord = z*math.tan(math.radians(xdegrees))
vcoord = z*math.tan(math.radians(ydegrees))
# find vehicle yaw
yaw=currentfacing
# determine angle to target relative to drone and world
phi1=math.atan2(vcoord,hcoord)
phi2=yaw-phi1
# determine distance to target
hyp=math.hypot(hcoord,vcoord)
# determine location relative to drone, with global orientation
y=hyp*math.sin(phi2)
x=hyp*math.cos(phi2)
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
print "Deploying Ordnance"
# Drop Raisins
time.sleep(2)

print "Returning to Launch"
vehicle.mode = VehicleMode("RTL")

# End Flight Code



# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
sitl.stop()
print("Completed")
