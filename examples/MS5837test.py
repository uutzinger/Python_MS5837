#!/usr/bin/python3
import MS5837.MS5837 as MS5837
import time

# Can enable debug output by uncommenting:
import logging
logging.basicConfig(level=logging.ERROR)
# Options DEBUG, INFO, WARNING, ERROR, CRITICAL

def low_pass(curr, prev, alpha):
  return curr * alpha + prev * (1 - alpha)

# Free up some CPU time
loop_interval = 0.001 # seconds

# Create sensor object
sensor = MS5837.MS5837(model=MS5837.MODEL_30BA) 

# We must initialize the sensor before reading it
if sensor.init():
  print("Pressure sensor init succeeded")
else:
  print("Sensor could not be initialized")
  exit(1)

# Configure sensor resolution
sensor.setOSR(MS5837.OSR_8192)           # highest sensor resolution
poll_interval = sensor.getPollInterval() # seconds
print("Recommended Poll Interval for MS5837: %4.3fS" % poll_interval)
  
# Get Static Pressure and read sensor for 2 seconds to stabilize it
i=int(2.0/poll_interval)
firsttime = True
while (i>0):
  i -= 1
  if sensor.read():
    if firsttime :
      staticPressure = sensor.pressure()
      firsttime = False
    else :
      staticPressure = low_pass(sensor.pressure(), staticPressure, 0.1)
  time.sleep(poll_interval)

print("Pressure: %f, Static: %f" % (sensor.pressure(), staticPressure))

lastPoll=time.monotonic()
previousRateTime=time.monotonic()
pressureCounter=0
  
while True:
  currentTimeS = time.monotonic()
  if currentTimeS - lastPoll >= poll_interval :
    if sensor.read():
      pressureCounter = pressureCounter + 1
	  
      print("Pressure: %.2f atm  %.2f Torr  %.2f psi") % (
      sensor.pressure(MS5837.UNITS_atm),
      sensor.pressure(MS5837.UNITS_Torr),
      sensor.pressure(MS5837.UNITS_psi))

      print("Temperature: %.2f C  %.2f F  %.2f K") % (
      sensor.temperature(MS5837.UNITS_Centigrade),
      sensor.temperature(MS5837.UNITS_Farenheit),
      sensor.temperature(MS5837.UNITS_Kelvin))

      sensor.setFluidDensity(MS5837.DENSITY_FRESHWATER)
      freshwaterDepth = sensor.depth(staticPressure) # default is freshwater
      sensor.setFluidDensity(MS5837.DENSITY_SALTWATER)
      saltwaterDepth = sensor.depth(staticPressure) # No nead to read() again
      sensor.setFluidDensity(1000) # kg/m^3
      print("Depth: %.3f m (freshwater)  %.3f m (saltwater)") % (freshwaterDepth, saltwaterDepth)

      # fluidDensity doesn't matter for altitude() (always MSL air density)
      print("MSL Relative Altitude: %.2f m") % sensor.altitude(staticPressure) # relative to Mean Sea Level pressure in air

  # Compute Sampling Rate
  if ((currentTimeS - previousRateTime) >= 1.0):
    pressureRate = pressureCounter
    pressureCounter = 0
    previousRateTime = currentTimeS
    
  print("Pressure rate: %d" % (pressureRate) ) 
  
  # Release task
  timeRemaining = loop_interval - (time.monotonic() - currentTimeS)
  if (timeRemaining > 0):
    time.sleep(timeRemaining)
