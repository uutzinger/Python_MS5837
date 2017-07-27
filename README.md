# Python_MS5837

A python module to interface with MS5837-30BA and MS5837-02BA waterproof pressure and temperature sensors.
This module is based on RTIMU MS5837 as well as bluerobotics MS5837.
The main difference to bluerobotics implementation is that the read command will release as soon as it is called and return True when new valid data is available.

This code is untested yet.

The Adafruit_Python_GPIO must be installed.

# Usage

	import MS5837

MS5837 provides a generic MS5837 class for use with different models

	MS5837(model=MS5837.MODEL_30BA, bus=1)

An MS5837 object can be constructed by specifiying the model and the bus

	sensor = MS5837.MS5837() # Use defaults (MS5837-30BA device on I2C bus 1)
	sensor = MS5837.MS5837(ms5837.MODEL_02BA, 0) # Specify MS5837-02BA device on I2C bus 0

### init()

Initialize the sensor. This needs to be called before using any other methods.

    sensor.init()

Returns true if the sensor was successfully initialized, false otherwise.

### setOSR()

After initilization, set the sensor accuracty

	sensor.setOSR(MS5837.OSR_8192)

	Valid arguments are:

    MS5837.OSR_256
    MS5837.OSR_512
    MS5837.OSR_1024
    MS5837.OSR_2048
    MS5837.OSR_4096
    MS5837.OSR_8192

### getPollInterval()

After setting oversampling rate the recommended poll interval can be obtained:
	
	poll_interval = sensor.getPollInterval()

It is recommended that the read() command is issued on a regular basis with the pollInterval.
	
### read()

Read the sensor and update the pressure and temperature. The sensor will be read with the supplied oversampling setting. Greater oversampling increases resolution, but takes longer and increases current consumption.

    sensor.read()
       
Returns True if a new data set is available, False otherwise. A data set consists of a pressure and tempreature reading.

### setFluidDensity(density)

Sets the density in (kg/m^3) of the fluid for depth measurements. The default fluid density is ms5837.DENISTY_FRESHWATER.

	sensor.setFluidDensity(1000) # Set fluid density to 1000 kg/m^3
	sensor.setFluidDensity(MS5837.DENSITY_SALTWATER) # Use predefined saltwater density

Some convenient constants are:

	MS5837.DENSITY_FRESHWATER = 997
	MS5837.DENSITY_SALTWATER = 1029

### pressure(conversion=UNITS_mbar)

Get the most recent pressure measurement.

	sensor.pressure() # Get pressure in default units (millibar)
	sensor.pressure(MS5837.UNITS_atm) # Get pressure in atmospheres
	sensor.pressure(MS5837.UNITS_kPa) # Get pressure in kilopascal

Some convenient constants are:

	MS5837.UNITS_Pa     = 100.0
	MS5837.UNITS_hPa    = 1.0
	MS5837.UNITS_kPa    = 0.1
	MS5837.UNITS_mbar   = 1.0
	MS5837.UNITS_bar    = 0.001
	MS5837.UNITS_atm    = 0.000986923
	MS5837.UNITS_Torr   = 0.750062
	MS5837.UNITS_psi    = 0.014503773773022

Returns the most recent pressure in millibar * conversion. Call read() to update.

### temperature(conversion=UNITS_Centigrade)

Get the most recent temperature measurement.

	sensor.temperature() # Get temperature in default units (Centigrade)
	sensor.temperature(MS5837.UNITS_Farenheit) # Get temperature in Farenheit

Valid arguments are:

	MS5837.UNITS_Centigrade
	MS5837.UNITS_Farenheit
	MS5837.UNITS_Kelvin

Returns the most recent temperature in the requested units, or temperature in degrees Centigrade if invalid units specified. Call read() to update.

### depth()

Get the most recent depth measurement in meters.

	sensor.depth(staticPressure=1013.25)
	
Returns the most recent depth in meters using the fluid density (kg/m^3) configured by setFluidDensity(). Call read() to update.

### altitude()

Get the most recent altitude measurement relative to Mean Sea Level pressure in meters.

	sensor.altitude(staticPressure=1013.25)

Returns the most recent altitude in meters relative to MSL pressure using the density of air at MSL. Call read() to update.
