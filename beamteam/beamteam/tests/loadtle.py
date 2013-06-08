'''
Created on 8 Jun 2013

@author: kusanagi
'''
import unittest
from beamteam.teambeam_helper import load_tle


class Test(unittest.TestCase):

    def test_load_tle(self):
        tle = load_tle('GSTAR 3', url='http://www.celestrak.com/NORAD/elements/geo.txt')
        print tle
        self.assertTrue(tle.startswith('GSTAR 3'), "Error loading tle")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()