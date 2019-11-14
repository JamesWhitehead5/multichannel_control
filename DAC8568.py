import board
import busio


class DAC8568:
    _spi = None

    _COMMAND = {"WRITE": 0b0000,
                "UPDATE": 0b0001,
                "WRITE_AND_UPDATE_ALL": 0b0010,
                "WRITE_AND_UPDATE": 0b0011
                }

    _CHANNEL = {"A": 0b0000,
                "B": 0b0001,
                "C": 0b0010,
                "D": 0b0011,
                "E": 0b0100,
                "F": 0b0101,
                "G": 0b0110,
                "H": 0b0111,
                "ALL": 0b1111,
                }

    def __init__(self, baud_rate):
        """Takes control of pins D0, D1, D3"""
        self._spi = busio.SPI(board.SCLK, board.MOSI, None)
        while not self._spi.try_lock():
            pass

        # Config for DAC baud rate (max is 50MHz):
        self._spi.configure(baudrate=baud_rate, polarity=1, phase=1, bits=32)
        self._spi.unlock()

        # Ensures we start in the same state each time
        self.software_reset()

        # Make sure that there is no external reference connected. Reference voltage is 2.5V
        self.internal_reference_on()

    def _write(self, buffer):
        self._spi.write(buffer)

    def internal_reference_on(self):
        self._write(DAC8568.to_bytes(0x090A0000))

    def software_reset(self):
        self._write(DAC8568.to_bytes(0x07000000))

    def clear_all_to_zero(self):
        """Sets all outputs to 0"""
        self._write(DAC8568.to_bytes(0x05000000))

    def clear_all_to_mid(self):
        """Sets all outputs to half way between 0 and maximum"""
        self._write(DAC8568.to_bytes(0x05000001))

    def clear_all_to_full(self):
        """Sets all outputs to their maximum value"""
        self._write(DAC8568.to_bytes(0x05000002))

    def write_to_register(self, channel: str, value: float):
        """"""
        self._write(DAC8568._make_word(command="WRITE", channel=channel, value=value))

    def write_and_update(self, channel: str, value: float):
        """"""
        self._write(DAC8568._make_word(command="WRITE_AND_UPDATE", channel=channel, value=value))

    def write_and_update_all(self, channel: str, value: float):
        """"""
        self._write(DAC8568._make_word(command="WRITE_AND_UPDATE_ALL", channel=channel, value=value))

    def update_channel(self, channel: str):
        """"""
        self._write(DAC8568._make_word(command="UPDATE", channel=channel))

    def write_to_ldac_register(self, channels: list):
        """"""
        channels_byte = DAC8568._channels_to_byte(channels)
        word = DAC8568.to_bytes(0x03000000 & channels_byte)
        self._write(word)

    def power_up_dac(self, channels: list):
        """"""
        channels_byte = DAC8568._channels_to_byte(channels)
        word = DAC8568.to_bytes(0x04000000 & channels_byte)
        self._write(word)

    @staticmethod
    def to_bytes(word: int):
        """Converts an integer to an array of 8-bit bytes with length 4 that can be processed by busio.SPI write
        for the Ti DA8568"""
        assert (word & ~0xFFFFFFFF == 0), "word is too long for 32 bits"
        return word.to_bytes(4, byteorder="big", signed=False)

    @staticmethod
    def _make_word_from_bits(prefix_bits: int, control_bits: int, address_bits: int, data_bits: int,
                             feature_bits: int) -> int:
        """Make a word for setting DAC register values"""
        assert (prefix_bits & ~0b1111 == 0)
        assert (control_bits & ~0b1111 == 0)
        assert (address_bits & ~0b1111 == 0)
        assert (data_bits & ~(2 ** 16 - 1) == 0)
        assert (feature_bits & ~0b1111 == 0)
        word = prefix_bits << 28 | control_bits << 24 | address_bits << 20 | data_bits << 4 | feature_bits
        return DAC8568.to_bytes(word)

    @staticmethod
    def _make_word(command: str, channel: str, value: float):
        """"""
        assert channel in DAC8568._CHANNEL.keys(), "Invalid channel: {}".format(channel)
        return DAC8568._make_word_from_bits(prefix_bits=0,
                                            control_bits=DAC8568._COMMAND[command],
                                            address_bits=DAC8568._CHANNEL[channel],
                                            data_bits=DAC8568._float_to_int(value),
                                            feature_bits=0)

    @staticmethod
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

    @staticmethod
    def _float_to_int(value: float):
        """Takes a floating point value between [0, 1] and converts it to a 16bit integer"""
        assert 0. <= value <= 1., "Value: {} is out of range".format(value)
        return int(value * (2 ** 16 - 1))


if __name__ == '__main__':
    assert (os.environ["BLINKA_FT232H"] == '1')

    dac_instance = DAC8568.DAC8568();
