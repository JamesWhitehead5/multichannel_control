import sys
sys.path.insert(1, '../code/')
from lightSource import TSL510

if __name__=='__main__':
    light = TSL510();
    print(light.status())
