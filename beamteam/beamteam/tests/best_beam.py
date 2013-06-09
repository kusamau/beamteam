'''
Created on 8 Jun 2013

@author: Maurizio Nagni
'''
import unittest
from beamteam.core.processor import best_beams


class Test(unittest.TestCase):

    def test_best_beam(self):
        beamsfile = open('pseudobeams.csv', 'r')
        ret = best_beams("10.0, 12.3, 2013-01-01", beamsfile)
        print(ret)
        self.assertTrue(True, "Error loading tle")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()