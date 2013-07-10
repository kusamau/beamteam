'''
Created on 8 Jun 2013

@author: Maurizio Nagni
'''
import unittest
from beamteam.core.processor import best_beams
from beamteam.core.earth_ellipsoid import xyz_distance, xyz_diff
import numpy

cust = (4012639.25044488, 77046.60963737409, 4940538.213016366)
sat = (-5706057.69586537, -41740588.95292159, -1773720.3653751202)
beam = (-377310.4603242225, -5395790.968263051, 3368565.5092535866)

class Test(unittest.TestCase):



    def test_best_beam(self):
        beamsfile = open('pseudobeams.csv', 'r')
        ret = best_beams("10.0, 12.3, 2013-01-01", beamsfile)
        print(ret)
        self.assertTrue(True, "Error loading tle")
    
    def test_diff(self):
        self.assertListEqual(xyz_diff(cust, sat), 
                             numpy.subtract(cust, sat).tolist(), 
                             "Error")

    def test_dist(self):
        self.assertEqual(xyz_distance(cust, sat), 
                             numpy.linalg.norm(numpy.array(cust)-numpy.array(sat)), 
                             "Error")
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()