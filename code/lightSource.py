class TSL510:
    """
    This class provides a simple interface with the TSL-510 Laser. It creates an
    object that consists of setters and getters.
    Most methods require the Laser Diode to be turned on in order to work.
    After turning the power on or the LD output off, it is recommended that you
    wait at least 30 seconds before turning on LD output.
    While the LD light is blinking, communication is not possible.
    """
    inst = None  # VISA resource manager instance for Laser

    def __init__(self):
        import visa

        """Constructor finds and connects to the VISA resource with name in ID string
        Prints confirmation to STDOUT.
        Raises exception if cannot connect
        """

        rm = visa.ResourceManager()
        target = 'TSL-510'

        for dev in rm.list_resources():
            try:
                inst = rm.open_resource(dev)
                name = inst.query('*IDN?')
                if target in name:
                    self.inst = inst
            except:
                continue

        if self.inst is None:
            raise RuntimeError("Target resource {} cannot be found in the VISA resource manager".format(target))
        print("Connected to " + self.inst.query('*IDN?'))

    def status(self) -> None:
        """
        Queries the device and returns some, but not all, human readable status
        values for general information and debugging purposes
        :return:
        """

        str = ""
        str += "Laser Diode Status (0:OFF, 1:ON):            " + self.inst.query(':POW:STAT?')
        str += "Power Attenuation (0:Manual, 1:Auto):        " + self.inst.query(':POW:ATT:AUT?')
        str += "Shutter (0:Open, 1:Closed):                  " + self.inst.query(':POW:SHUT?')
        str += "Power units are (0:dBm, 1:mW):               " + self.inst.query(':POW:UNIT?')
        str += "Wavelength units are (0:nm, 1:THz):          " + self.inst.query(':WAV:UNIT?')
        # And on and on...
        return str

    @staticmethod
    def _bool_to_int(value: bool) -> int:
        """
        Maps a boolean false to an integer 0 and a boolean tru to an integer 1
        :param value:
        :return:
        """
        if value:
            return int(1)
        else:
            return int(0)

    def set_wavelength_unit(self, unit: bool) -> None:
        """
        Wavelength field can either represent the wavelength(in nm) or the
        frequency(in THz). Parameter num can either be 0 or 1.(0:nm, 1:THz)
        Raises exception if num is out of range

        :param unit: If unit is false, the unit is set to nanometers. If true, TeraHertz
        :return:
        """
        self.inst.write(':WAV:UNIT ' + self._bool_to_int(unit))

    def set_color(self, color: float) -> None:
        """
        Sets the color of light coming out of the laser.

        :param color: The color of light coming out of the laser. Units are either nanometers or THz,
            depending on what has been set beforehand.
        :return:
        """
        self.inst.write(':WAV ' + str(color))

    def set_power_unit(self, value: bool) -> None:
        """
        Sets the power unit for the laser. Power field can have units dBm (dBmW) or just mW.

        :param value: If false, the power units are dBm. If true, mW.
        :return:
        """
        self.inst.write(':POW:UNIT ' + str(self._bool_to_int(value)))

    def set_power(self, power: float) -> None:
        """
        Sets laser power in units set beforehand
        :param power: Power in either dBm or mW.
        :return:
        """
        self.inst.write(':POW ' + str(power))

    def get_power_true(self) -> float:
        """
        Uses power meter inside of laser to measure actual power output(at source)

        :return: Measured power in system units (dBm or mW)
        """
        return float(self.inst.query(':POW:ACT?'))

    def get_range_power(self) -> (float, float):
        """
        Gives a range of power. I don't know what this means: maybe attainable power
        range or stable power range? May be constant or vary w/
        temperature, wavelength, etc.

        :return: a 2 element tuple of floats (min, max)
        """
        return float(self.inst.query(':POW:LEV:MIN?')), float(self.inst.query(':POW:LEV:MAX?'))

    def get_range_wavelength(self) -> (float, float):
        """
        Not well documented function (see get_range_power)

        :return: a 2 element tuple of floats (min, max)
        """
        return float(self.inst.query(':WAV:MIN?')), float(self.inst.query(':WAV:MAX?'))

    def ld_off(self) -> None:
        """
        Turns off the Laser Diode (LD)
        :return:
        """
        self.inst.write(':POW:STAT 0')
