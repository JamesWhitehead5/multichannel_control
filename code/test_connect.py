import os
import time
import board
import digitalio

def main():
    ft232H_test()


def ft232H_test():
    assert (os.environ["BLINKA_FT232H"] == '1')
    led = digitalio.DigitalInOut(board.C0)
    led.direction = digitalio.Direction.OUTPUT

    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)


if __name__== "__main__":

    main()