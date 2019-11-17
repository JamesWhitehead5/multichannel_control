from typing import Tuple

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
                name = inst.query('*IDN?') #Agilent Technologies,8163B,MY48208514,V5.25(72637)
                if target in name:
                    self._inst = inst
            except:
                continue

        if self._inst is None:
            raise RuntimeError("Target resource {} cannot be found in the VISA resource manager".format(target))
        print("Connected to " + self._inst.query('*IDN?'))
