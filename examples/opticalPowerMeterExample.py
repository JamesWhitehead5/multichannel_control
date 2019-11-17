import sys
sys.path.insert(1, '../code/')
from tools import PowerUnit
from opticalPowerMeter import KEYSIGHT81634B

if __name__=='__main__':
    meter = KEYSIGHT81634B();

    meter.set_power_unit(PowerUnit.W)

    meter.set_wavelength(1.45)

    for _ in range(10):
        print(meter.get_power())