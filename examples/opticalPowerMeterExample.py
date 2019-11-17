import sys
sys.path.insert(1, '../code/')
from opticalPowerMeter import KEYSIGHT81634B

if __name__=='__main__':
    light = KEYSIGHT81634B();
    #print(light.status())