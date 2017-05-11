# Basic test code; set up to make drone take off and land. Connection string looks for a vehicle connected by serial port.
# To do: script should wait between RTL mode and LAND mode. 

import exceptions
import math
connection_string = "/dev/ttyAMA0"

from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
import socket

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
vehicle.simple_takeoff(aTargetAltitude) # Take off to
i = 0
while i < 10:
    i += 1
    print " Waiting..."
    time.sleep(1)

print "Returning to Launch"
vehicle.mode = VehicleMode("RTL")

print "Landing"
vehicle.mode = VehicleMode("LAND")

# End Flight Code



# Close vehicle object before exiting script
vehicle.close()
