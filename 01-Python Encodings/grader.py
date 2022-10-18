import unittest
import random
from code import *


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_int_bits(self):
        for _ in range(10):
            x = random.randint(-1000, 1000)
            self.assertEqual(int_bits(x), bin(x))

    def test_str_bits(self):
        strs = [
            "MAyDCEnfmz",
            "ipjPhHBdzO",
            "RoOeFyrlnB",
            "vwZirOThda",
            "RnvSUIcCxX",
            "ykIykPHjGS",
            "orIwLBnnvP",
            "utymLcrtTz",
            "BeRkLIxqCK",
            "JvobHwRJIu",
        ]
        bins = [
            "01001101 01000001 01111001 01000100 01000011 01000101 01101110 01100110 01101101 01111010",
            "01101001 01110000 01101010 01010000 01101000 01001000 01000010 01100100 01111010 01001111",
            "01010010 01101111 01001111 01100101 01000110 01111001 01110010 01101100 01101110 01000010",
            "01110110 01110111 01011010 01101001 01110010 01001111 01010100 01101000 01100100 01100001",
            "01010010 01101110 01110110 01010011 01010101 01001001 01100011 01000011 01111000 01011000",
            "01111001 01101011 01001001 01111001 01101011 01010000 01001000 01101010 01000111 01010011",
            "01101111 01110010 01001001 01110111 01001100 01000010 01101110 01101110 01110110 01010000",
            "01110101 01110100 01111001 01101101 01001100 01100011 01110010 01110100 01010100 01111010",
            "01000010 01100101 01010010 01101011 01001100 01001001 01111000 01110001 01000011 01001011",
            "01001010 01110110 01101111 01100010 01001000 01110111 01010010 01001010 01001001 01110101",
        ]
        for (s, b) in zip(strs, bins):
            self.assertEqual(str_bits(s), b)

    def test_bytes_bits(self):
        bstrs = [
            b"yOlNlfOhPI",
            b"caSDYjCMVo",
            b"zeTsqTmkXn",
            b"BnnWYisOKr",
            b"yqXthKCshU",
            b"hMHvDyDnvQ",
            b"WmuUTDDgYY",
            b"eQgxeuzDkR",
            b"IyjgRNWsfz",
            b"pTWuTHlcic",
        ]
        bins = [
            "01111001 01001111 01101100 01001110 01101100 01100110 01001111 01101000 01010000 01001001",
            "01100011 01100001 01010011 01000100 01011001 01101010 01000011 01001101 01010110 01101111",
            "01111010 01100101 01010100 01110011 01110001 01010100 01101101 01101011 01011000 01101110",
            "01000010 01101110 01101110 01010111 01011001 01101001 01110011 01001111 01001011 01110010",
            "01111001 01110001 01011000 01110100 01101000 01001011 01000011 01110011 01101000 01010101",
            "01101000 01001101 01001000 01110110 01000100 01111001 01000100 01101110 01110110 01010001",
            "01010111 01101101 01110101 01010101 01010100 01000100 01000100 01100111 01011001 01011001",
            "01100101 01010001 01100111 01111000 01100101 01110101 01111010 01000100 01101011 01010010",
            "01001001 01111001 01101010 01100111 01010010 01001110 01010111 01110011 01100110 01111010",
            "01110000 01010100 01010111 01110101 01010100 01001000 01101100 01100011 01101001 01100011",
        ]
        for (s, b) in zip(bstrs, bins):
            self.assertEqual(bytes_bits(s), b)

    def test_int_hex(self):
        for _ in range(10):
            x = random.randint(-1000, 1000)
            self.assertEqual(int_hex(x), hex(x))

    def test_str_hex(self):
        strs = [
            "jzDoltpxag",
            "tRlnXEUuco",
            "oisSuNWLLL",
            "zYzLsYjnOx",
            "ofJzDsFFtj",
            "jXGnKvnZeu",
            "bjaKyWmknT",
            "NWxfZKXzrQ",
            "DnmasAUVtc",
            "DCvVxhuUhO",
        ]
        hexs = [
            "0x6a7a446f6c7470786167",
            "0x74526c6e58455575636f",
            "0x6f697353754e574c4c4c",
            "0x7a597a4c73596a6e4f78",
            "0x6f664a7a44734646746a",
            "0x6a58476e4b766e5a6575",
            "0x626a614b79576d6b6e54",
            "0x4e5778665a4b587a7251",
            "0x446e6d61734155567463",
            "0x4443765678687555684f",
        ]
        for (s, b) in zip(strs, hexs):
            self.assertEqual(str_hex(s), b)

    def test_bytes_hex(self):
        bstrs = [
            b"GbraQXqViB",
            b"shABSzqTZZ",
            b"SEDMhYGZIR",
            b"ZjNqPkhkwW",
            b"ptYOJdxeui",
            b"crdJTSGSRY",
            b"pJWGoMeZkD",
            b"PhxTxdUmAu",
            b"DlyfOgOpgO",
            b"ImDQUWkoRd",
        ]
        hexs = [
            "0x47627261515871566942",
            "0x73684142537a71545a5a",
            "0x5345444d6859475a4952",
            "0x5a6a4e71506b686b7757",
            "0x7074594f4a6478657569",
            "0x6372644a545347535259",
            "0x704a57476f4d655a6b44",
            "0x506878547864556d4175",
            "0x446c79664f674f70674f",
            "0x496d445155576b6f5264",
        ]
        for (s, b) in zip(bstrs, hexs):
            self.assertEqual(bytes_hex(s), b)

    def test_bin_int(self):
        bins = [
            "-0b1101100000",
            "-0b100110011",
            "-0b111110001",
            "-0b110011011",
            "-0b1111111",
            "0b1001011110",
            "0b1001001100",
            "0b110",
            "0b1000011000",
            "0b1101110010",
        ]
        ints = [-864, -307, -497, -411, -127, 606, 588, 6, 536, 882]
        for (b, i) in zip(bins, ints):
            self.assertEqual(bin_int(b), i)

    def test_bytes_int(self):
        bts = [
            b"\xff-",
            b"\xfd\x05",
            b"\xfc\xe3",
            b"\x02\x98",
            b"\xfe\xd0",
            b"b",
            b"\xfe}",
            b"\xfei",
            b"\xfc=",
            b"\x03J",
        ]
        ints = [-211, -763, -797, 664, -304, 98, -387, -407, -963, 842]
        for (b, i) in zip(bts, ints):
            self.assertEqual(bytes_int(b), i)

    def test_int_bytes(self):
        ints = [942, -820, 509, -557, -576, 910, -306, -582, 65, -599]
        bts = [
            b"\x03\xae",
            b"\xfc\xcc",
            b"\x01\xfd",
            b"\xfd\xd3",
            b"\xfd\xc0",
            b"\x03\x8e",
            b"\xfe\xce",
            b"\xfd\xba",
            b"A",
            b"\xfd\xa9",
        ]
        for (i, b) in zip(ints, bts):
            self.assertEqual(int_bytes(i), b)

    def test_str_bytes(self):
        strs = [
            "OLWrUSFTFR",
            "YmxPLMFAsQ",
            "oyEbzThHxp",
            "dbwFjBrXrk",
            "VhUMRttDKV",
            "YWoQCYtAlE",
            "iiclJTWpHw",
            "SbfYiEQiih",
            "BoVxChxFov",
            "LSDslXMPcW",
        ]
        bts = [
            b"OLWrUSFTFR",
            b"YmxPLMFAsQ",
            b"oyEbzThHxp",
            b"dbwFjBrXrk",
            b"VhUMRttDKV",
            b"YWoQCYtAlE",
            b"iiclJTWpHw",
            b"SbfYiEQiih",
            b"BoVxChxFov",
            b"LSDslXMPcW",
        ]
        for (s, b) in zip(strs, bts):
            self.assertEqual(str_bytes(s), b)

    def test_bytes_str(self):
        bts = [
            b"DgmaiOQUXQ",
            b"FLEYyxCBfS",
            b"MiPzKwCVzv",
            b"KjmilpJrAh",
            b"aCSzXgaORB",
            b"ROqRVQtJyd",
            b"skAKSgMgmF",
            b"SHMDanMFtY",
            b"gAoIowXHIO",
            b"PrKglHruuS",
        ]
        strs = [
            "DgmaiOQUXQ",
            "FLEYyxCBfS",
            "MiPzKwCVzv",
            "KjmilpJrAh",
            "aCSzXgaORB",
            "ROqRVQtJyd",
            "skAKSgMgmF",
            "SHMDanMFtY",
            "gAoIowXHIO",
            "PrKglHruuS",
        ]
        for (b, s) in zip(bts, strs):
            self.assertEqual(bytes_str(b), s)


if __name__ == "__main__":
    results = unittest.main()
