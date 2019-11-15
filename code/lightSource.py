import visa, time, math, sys
import numpy as np


# This class provides a simple interface with the TSL-510 Laser. It creates an
# object that consists of setters and getters for the source.
# Most methods in  Laser require the Laser Diode to be turned on in order to work.
# After turning the power on or the LD output off, it is recommended that you
# wait at least 30 seconds before turning on LD output.
# While the LD light is blinking, communication is not possible.
# Additonal methods should be added in the future to allow for greater
# functionality
# Methods with a preceding '_' are considered private and should not be used
# outside of the class since they may be depreciated or modified in the future
class Laser:

    # Constructor finds and connects to the VISA resource with name in ID string
    # Prints conformation to STDOUT.
    # Raises exception if cannot connect
    def __init__(self):
        self.inst = None  # VISA resource manager instance for Laser
        rm = visa.ResourceManager()
        for dev in rm.list_resources():
            try:
                inst = rm.open_resource(dev)
                name = inst.query('*IDN?')
                if 'TSL-510' in name:
                    self.inst = inst
            except:  # gotta find out the specific exception that is thrown
                continue
        if self.inst is None:
            raise Exception('Can\'t connect to TSL-510 LASER')
        print("Connected to " + self.inst.query('*IDN?'))

    # Queries the device and returns some, but not all, human readable status
    # values for general information and debuging purposes
    def status(self):
        str = ""
        str += "Laser Diode Status (0:OFF, 1:ON):            " + self.inst.query(':POW:STAT?')
        str += "Power Attenuation (0:Manual, 1:Auto):        " + self.inst.query(':POW:ATT:AUT?')
        str += "Shutter (0:Open, 1:Closed):                  " + self.inst.query(':POW:SHUT?')
        str += "Power units are (0:dBm, 1:mW):               " + self.inst.query(':POW:UNIT?')
        str += "Wavelength units are (0:nm, 1:THz):          " + self.inst.query(':WAV:UNIT?')
        # And on and on...
        return str

    # a "private" helper class. Raises exception if num in neither 0 nor 1
    def _zero_or_one(self, num):
        if not (num == 0 or num == 1):
            raise Exception('Invalid input: ' + str(num))  # throw a better exception

    # Wavelength field can either represent the wavelength(in nm) or the
    # frequency(in THz). Parameter num can either be 0 or 1.(0:nm, 1:THz)
    # Raises exception if num is out of range
    def set_wavelength_unit(self, num):
        self._zero_or_one(num)
        self.inst.write(':WAV:UNIT ' + str(num))

    # Sets wavelength of the laser. Units of wl depend on what has been set
    def set_wavelength(self, wl):
        self.inst.write(':WAV ' + str(wl))

    # Power field can have units dBm (dBmW) or just mW. The parameter num can be
    # either 0 or 1.(0:dBm, 1:mW)
    # Raises exception if num is out of range
    def set_power_unit(self, num):
        self._zero_or_one(num)
        self.inst.write(':POW:UNIT ' + str(num))

    # Sets laser power in units previously set
    def set_power(self, power):
        self.inst.write(':POW ' + str(power))

    # Uses internal power meter to measure acctual power outpt(at source). Returns
    # a float of output power
    def get_power_true(self):
        return float(self.inst.query(':POW:ACT?'))

    # gives a range of power. I don't know what this means: maybe attainable power
    # range or stable power range? May be constant or vary w/
    # temperature, wavelength, etc.
    # returns a 2 element list of floats [min, max]
    def get_range_power(self):
        return [float(self.inst.query(':POW:LEV:MIN?')), float(self.inst.query(':POW:LEV:MAX?'))]

    # Not well documented function(see get_range_power)
    # returns a 2 element list of floats [min, max]
    def get_range_wavelength(self):
        return [float(self.inst.query(':WAV:MIN?')), float(self.inst.query(':WAV:MAX?'))]

    # turns on the Laser Diode (LD)
    # After turning the power on or the LD off, it is recommended that you
    # wait at least 30 seconds before turning on the LD.
    # def LD_on(self):
    #   self.inst.write(':POW:STAT 1')
    # Depreciated. Is easy to change manually and may cause damage to laser

    # turns off the Laser Diode (LD)
    def LD_off(self):
        self.inst.write(':POW:STAT 0')