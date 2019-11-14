#Demo to show smooth output from the DAC



import numpy as np
from DAC8568 import DAC8568

def generate_points():
    n = 1000
    t = np.arange(n)
    y = np.sin(t/n*2*np.pi)/2. + 0.5

    return t, y

def smooth_point():
    _, Y = generate_points()

    dac = DAC8568(baud_rate=100000)
    while True:
        for y in Y:
            dac._write(dac._make_word(command="WRITE_AND_UPDATE", channel="A", value=float(y)))

if __name__=='__main__':
    smooth_point()