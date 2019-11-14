import unittest

#from DAC8568 import make_word, float_to_uint16


class TestDAC8568(unittest.TestCase):
    if __name__ == '__main__':
        unittest.main()

    # def testInstantialte(self):
    #     val = make_word(prefix_bits=0b00, control_bits=0b0011, address_bits=0b0000, data_bits=0b1111111111111111,
    #                       feature_bits=0b0000)
    #     #val = DAC8568.makeFrame(0b00, 0b0011, 0b0000, 0b1111111111111111, 0b0000)
    #
    #     self.assertEqual(bytes(0b000011000011111111111111110000), val)

    # def test_float_to_uint(self):
    #     self.assertEqual(float_to_uint16(0.), b'\x00\x00');
    #     self.assertEqual(float_to_uint16(1.), b'\xFF\xFF');
    #     self.assertEqual(float_to_uint16(0.5), b'\x7F\xFF');

