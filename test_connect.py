from pyftdi.ftdi import Ftdi
import os
import time
import board
import digitalio
import busio

from DAC8568 import make_word, COMMAND, make_word_nice, INTERNAL_REFERENCE_ON, write_to_ldac_register, SOFTWARE_RESET, \
    power_up_dac, CLEAR_ALL_ON

BAUD_RATE = 10000

def main():
    #ft232H_test()
    interface_test()


def interface_test():
    spi = busio.SPI(board.SCLK, board.MOSI, None)
    while not spi.try_lock():
        pass
    # Config for DAC baudrate (max is 50MHz):
    spi.configure(baudrate=BAUD_RATE, polarity=1, phase=1, bits=32)
    spi.unlock()  # What does this do?

    #Define a pin to clear the device
    CLR_INV = digitalio.DigitalInOut(board.D7)
    CLR_INV.direction = digitalio.Direction.OUTPUT


    #Clear device
    CLR_INV.value = True
    time.sleep(0.001)
    CLR_INV.value = False
    time.sleep(0.001)
    CLR_INV.value = True
    time.sleep(0.001)

    #spi.write(SOFTWARE_RESET)
    #spi.write(CLEAR_ALL_ON)
    #spi.write(power_up_dac(["ALL"]))
    #spi.write(write_to_ldac_register(["ALL"]))

    #Turn internal reference on
    #spi.write(INTERNAL_REFERENCE_ON) #It doesn't turn on

    #Write to DAC input register Ch A and update that DAC registers (SW LDAC)
    spi.write(make_word_nice(command="WRITE_AND_UPDATE_ALL", channel="A", value=1))
    # spi.write(make_word_nice(command="WRITE_AND_UPDATE_ALL", channel="B", value=1))
    # spi.write(make_word_nice(command="WRITE_AND_UPDATE_ALL", channel="C", value=1))
    # spi.write(make_word_nice(command="WRITE_AND_UPDATE_ALL", channel="D", value=1))
    # spi.write(make_word_nice(command="WRITE_AND_UPDATE_ALL", channel="E", value=1))
    #spi.write(make_word_nice(command="WRITE_AND_UPDATE_ALL", channel="G", value=1))
    #spi.write(make_word_nice(command="UPDATE", channel="G", value=1))
    #spi.write(make_word_nice(command="RESET", channel="G", value=1))
    #spi.write(make_word_nice(command="WRITE_AND_UPDATE_ALL", channel="H", value=1))


    while True:
        channels = ["A", "B", "C", "D", "E", "F", "G", "H"]
        for channel in channels:
            spi.write(make_word_nice(command="WRITE_AND_UPDATE", channel=channel, value=0.5))
            time.sleep(0.1)
        for channel in channels:
            spi.write(make_word_nice(command="WRITE_AND_UPDATE", channel=channel, value=0))
            time.sleep(0.1)


def ft232H_test():
    assert (os.environ["BLINKA_FT232H"] == '1')

    ##Ftdi().open_from_url('ftdi://ftdi:232h:1/1')

    # print(dir(board))

    led = digitalio.DigitalInOut(board.C0)
    led.direction = digitalio.Direction.OUTPUT

    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)


if __name__== "__main__":

    main()