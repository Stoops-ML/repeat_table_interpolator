import unittest
import numpy as np
import interpolate_repeated_table as IRT


class TestInterpolator(unittest.TestCase):

    @classmethod
    def setUp(cls):
        try:
            cls.test_file = np.loadtxt('file.csv')
        except OSError as ex:
            print('Test file not found')
            raise OSError(ex)

    @classmethod
    def teardown(cls):
        pass

    def test_interpolate_exact_values(self):
        """test whether function returns exact values from the file"""
        for line in self.test_file:
            output = IRT.interpolate_table(self.test_file, *line[:3])
            self.assertEqual(list(line[3:]), output)

    def test_move_columns(self):
        """test whether function returns swapped exact values from the file"""
        for line in self.test_file:
            output = IRT.interpolate_table(self.test_file, *line[:3], move_columns=3)
            self.assertEqual(list(line[:2:-1]), output)
