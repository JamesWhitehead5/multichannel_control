from typing import Tuple
from tools import PowerUnit;


class KEYSIGHT81634B:
    """
    This class provides a simple interface with the Keysight 81634B lightwave power meter. The device is connected
    to the computer using a GPIB to USB adapter connected to a multi-device bus.
    """
    _inst = None  # VISA resource manager instance for power meter

    def __init__(self):
        """
        Finds and connects to the VISA resource with name in ID string.
        Prints confirmation to STDOUT.
        :raises: RuntimeError if cannot connect to the meter
        """
        import visa

        rm = visa.ResourceManager()
        target = 'Agilent Technologies,8163B,MY48208514,V5.25(72637)'

        for dev in rm.list_resources():
            try:
                inst = rm.open_resource(dev)
                name = inst.query('*IDN?')  # Agilent Technologies,8163B,MY48208514,V5.25(72637)
                if target in name:
                    # TODO: check that the slot contains the correct module
                    self._inst = inst
            except:
                continue

        if self._inst is None:
            raise RuntimeError("Target resource {} cannot be found in the VISA resource manager".format(target))
        print("Connected to " + self.id())

    def id(self) -> str:
        """
        Queries the module for the identification number

        :return: Identification string
        """

        return self._inst.query('*IDN?')

    def get_power(self):
        """
        :READ[n][:CHANnel[m]][:SCALar]: POWer[:DC]?
        Reads the current power meter value. It provides its own software triggering and does not need a triggering command.

        :return: The current power meter reading as a float value in dBm, W or dB.
        """

        return float(self._inst.query(":READ:POW?"))

    def set_power_unit(self, power_unit: PowerUnit) -> None:
        """
        Sets or returns the units used for absolute readings on a sensor.

        :param power_unit: Power unit that should be used. Either dBm or W.
        """

        # 0: Current power units are dBm. 1: Current power units are Watts.
        if power_unit == PowerUnit.dBm:
            unit_argument = int(0)
        elif power_unit == PowerUnit.W:
            unit_argument = int(1)
        else:
            raise ValueError("power unit {} is not supported on this device".format(power_unit))

        #:SENSe[n][:CHANnel[m]]:POWer:UNIT/?
        self._inst.write("SENS:POW:UNIT {}".format(unit_argument))

    def set_wavelength(self, wavelength: float) -> None:
        """
        Sets the power wavelength
        :param wavelength: Wavelength in micrometers.
        """

        assert isinstance(wavelength, float), "Incompatible type"

        #:SENSe[n][:CHANnel[m]]:POWer:WAVelength /?
        self._inst.write("SENS:POW:WAV {}".format(wavelength))

    def get_errors(self) -> str:
        """

        :return: Returns the contents of the instrument’s error queue.
        """
        #:SYSTem:ERRor?
        return self._inst.query(":SYST:ERR?")