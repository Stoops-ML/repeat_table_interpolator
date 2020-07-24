import unittest
import numpy as np
import interpolate_repeated_table as IRT


class TestInterpolator(unittest.TestCase):

    @classmethod
    def setUp(cls):
        try:
            cls.num_decimals = 6
            cls.test_file = np.loadtxt('file.csv').round(decimals=cls.num_decimals)
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
            nums_compare = np.array(line[3:]) == output.round(decimals=self.num_decimals)
            self.assertTrue(np.all(nums_compare))

    def test_move_columns(self):
        """test whether function returns swapped exact values from the file"""
        for line in self.test_file:
            output = IRT.interpolate_table(self.test_file, *line[:3], move_columns=3)
            nums_compare = np.array(line[:2:-1]) == output.round(decimals=self.num_decimals)
            self.assertTrue(np.all(nums_compare))
