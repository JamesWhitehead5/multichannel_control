import os
from enum import Enum


def to_bytes(word: int):
    """Converts an integer to an array of 8-bit bytes with length 4 that can be processed by busio.SPI write
    for the Ti DA8568"""
    assert (word & ~0xFFFFFFFF == 0), "word is too long for 32 bits"
    return word.to_bytes(4, byteorder="big", signed=False)


def make_word(prefix_bits: int, control_bits: int, address_bits: int, data_bits: int, feature_bits: int) -> int:
    """Make a word for setting DAC register values"""
    assert (prefix_bits & ~0b1111 == 0)
    assert (control_bits & ~0b1111 == 0)
    assert (address_bits & ~0b1111 == 0)
    assert (data_bits & ~(2 ** 16 - 1) == 0)
    assert (feature_bits & ~0b1111 == 0)
    word = prefix_bits << 28 | control_bits << 24 | address_bits << 20 | data_bits << 4 | feature_bits
    return to_bytes(word)


def make_word_nice(command: str, channel: str, value: float):
    """Syntax wrapper for make_word."""
    return make_word(prefix_bits=0,
                     control_bits=COMMAND[command],
                     address_bits=CHANNEL[channel],
                     data_bits=float_to_int(value),
                     feature_bits=0)

COMMAND = {"WRITE": 0b0000,
           "UPDATE": 0b0001,
           "CLEAR": 0b0101,
           "RESET": 0b0111,
           "WRITE_AND_UPDATE_ALL": 0b0010,
           "WRITE_AND_UPDATE": 0b0011,
           "POWER_DOWN": 0b0100,
           }

CHANNEL = {"A": 0b0000,
           "B": 0b0001,
           "C": 0b0010,
           "D": 0b0011,
           "E": 0b0100,
           "F": 0b0101,
           "G": 0b0110,
           "H": 0b0111,
           "ALL": 0b1111,
           }


INTERNAL_REFERENCE_ON = to_bytes(0x090A0000)
SOFTWARE_RESET = to_bytes(0x07000000)
CLEAR_ALL_ON = to_bytes(0x05000002)


def _channels_to_byte(channels: list):
    channel_byte = 0
    if "H" in channels:
        channel_byte |= 0b10000000
    if "G" in channels:
        channel_byte |= 0b01000000
    if "F" in channels:
        channel_byte |= 0b00100000
    if "E" in channels:
        channel_byte |= 0b00010000
    if "D" in channels:
        channel_byte |= 0b00001000
    if "C" in channels:
        channel_byte |= 0b00000100
    if "B" in channels:
        channel_byte |= 0b00000010
    if "A" in channels:
        channel_byte |= 0b00000001
    if "ALL" in channels:
        channel_byte |= 0b11111111
    return channel_byte


def write_to_ldac_register(channels: list):
    channels_byte = _channels_to_byte(channels)
    word = 0x03000000 & channels_byte
    return to_bytes(word)

def power_up_dac(channels: list):
    channels_byte = _channels_to_byte(channels)
    word = 0x04000000 & channels_byte
    return to_bytes(word)


def float_to_int(value: float):
    """Takes a floating point value between [0, 1] and converts it to a 16bit integer"""
    assert 0. <= value <= 1., "Value: {} is out of range".format(value)
    return int(value*(2**16-1))

class DAC8568:
    _spi = None
    _sync = None

    def __init__(self):
        self._spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=None)
        while not self._spi.try_lock():
            pass
        pass

        self._sync = digitalio.DigitalInOut(board.C0) #Sync line
        self._ldac = digitalio.DigitalInOut(board.C1) #Load dac from shift register


        # Config for DAC baudrate (max is 50MHz for DAC):
        self._spi.configure(baudrate=12000000, polarity=0, phase=1, bits=32)



    def send_command(self, buffer):

        self._spi.write(buffer)



if __name__=='__main__':
    import time
    import board
    import digitalio
    import busio
    assert (os.environ["BLINKA_FT232H"] == '1')
    dac_instance = DAC8568.DAC8568();


