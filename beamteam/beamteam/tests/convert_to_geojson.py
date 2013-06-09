'''
Created on 8 Jun 2013

@author: Maurizio Nagni
'''
import unittest
from beamteam.views.data import convert_to_geojson
import ephem


class Test(unittest.TestCase):

    def test_convert_to_geojson(self):
        expected_geojson = """
{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [12.0, 23.0]}, "type": "Feature", "properties": {"elevation": 1}}]}
        """
        
        date = ephem.now()
        best = (12.0, 23.0, date.datetime().isoformat(), [], 1)
        conv_geojson = convert_to_geojson(best)
        print(conv_geojson)
        self.assertTrue(expected_geojson.trim() == conv_geojson, "Error loading tle")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()