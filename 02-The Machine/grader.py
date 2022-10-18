import unittest
import random
from interpreter import *


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_program1(self):
        expected = [3]
        result = execute("programs/program1")
        self.assertEqual(result, expected)

    def test_program2(self):
        expected = ["1 + 2 =\n", 3]
        result = execute("programs/program2")
        self.assertEqual(result, expected)

    def test_program3(self):
        expected = ["Hello World!\n"]
        result = execute("programs/program3")
        self.assertEqual(result, expected)

    def test_program4(self):
        expected = ["10 + 100 =\n", 110]
        result = execute("programs/program4")
        self.assertEqual(result, expected)

    def test_program5(self):
        expected = [85, 8, 3.0, 720, "ALL DONE!\n"]
        result = execute("programs/program5")
        self.assertEqual(result, expected)

    def test_program6(self):
        expected = [5, 3, 24, 3.0, "ABCDEFG\n"]
        result = execute("programs/program6")
        self.assertEqual(result, expected)

    def test_program7(self):
        expected = [
            "4 + 1 =\n",
            5,
            "\n",
            "10 * 100 =\n",
            1000,
            "\n",
            "100 / 10 =\n",
            10.0,
            "\n",
            "5 / 3 =\n",
            1.6666666666666667,
        ]
        result = execute("programs/program7")
        self.assertEqual(result, expected)

    def test_program8(self):
        expected = [
            "H   H EEEEE L     L      OOO       W   W  OOO  RRRR  L     DDDD  !!\n",
            "H   H E     L     L     O   O      W W W O   O R   R L     D   D !!\n",
            "HHHHH EEEEE L     L     O   O      W W W O   O RRRR  L     D   D !!\n",
            "H   H E     L     L     O   O       W W  O   O R   R L     D   D !!\n",
            "H   H EEEEE LLLLL LLLLL  OOO        W W   OOO  R   R LLLLL DDDD  !!\n",
        ]
        result = execute("programs/program8")
        self.assertEqual(result, expected)


if __name__ == "__main__":
    results = unittest.main()
