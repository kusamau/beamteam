'''
Created on 9 Jun 2013

@author: Simone Sturnioli
'''
import sys
import urllib2
sys.path.append(".")
import ephem
import pyproj
 
from beamteam.core.power_calc import *
 
def day_trajectory(path, date='2013/06/08 00:00:00', points=24, lat=51.5, lon=1.1, elevation=200):
    tle = open(path).readlines()
    sat = ephem.readtle(*tle)
    date = ephem.Date(date)
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = elevation
 
    source = pyproj.Proj(init='epsg:4326')
    target = pyproj.Proj(proj='geocent')
 
    obs_xyz = pyproj.transform(source, target, x=obs.lon * 180. / ephem.pi, y=obs.lat * 180. / ephem.pi, z=obs.elevation)
 
    for i in range(points):
        t = i / float(points)
        obs.date = ephem.Date(date + t)
        sat.compute(obs)
        sat_xyz = pyproj.transform(source, target, x=sat.sublong * 180. / ephem.pi, y=sat.sublat * 180. / ephem.pi, z=sat.elevation)
 
    return sat
 
 
constellation = {
    'AMER': 'INMARSAT-4-F3.tle',
    'EMEA': 'INMARSAT-4-F2.tle',
#    'ASIP': 'INMARSAT-4-F1.tle',
}
 
max_beams = 10    # Number of closest beams we want to find as a first approximation
 
def best_beams(coordinates, beamsfile):
 
    values = [line.split(',') for line in coordinates.split('\n')]
    return do_best_beams(values, beamsfile)
 
def do_best_beams(values, beamsfile, return_all = False):
    bests = []
     
    source = pyproj.Proj(init='epsg:4326')
    target = pyproj.Proj(proj='geocent')
 
    for vs in values:
        lat, lon = vs[:2]
        try:
            date = ephem.Date(vs[2])
        except IndexError:
            date = ephem.now()
 
        obs = ephem.Observer()
        obs.lat = str(lat)
        obs.lon = str(lon)
        obs.date = date
 
        obs_xyz = pyproj.transform(source, target, x=obs.lon * 180. / ephem.pi, y=obs.lat * 180. / ephem.pi, z=obs.elevation)
 
        bbs = []
        best = None
 
        for label, tlepath in constellation.items():
            f = beamsfile
            sat_beams = parse_beam_data(f.readlines(), label)
 
            tle = load_tle(tlepath, url='http://www.celestrak.com/NORAD/elements/geo.txt')
            #tle = open(tlepath).readlines()
            #sat = ephem.readtle(*tle)
            sat = ephem.readtle(tle[0], tle[1], tle[2])
 
            sat.compute(obs)
            sat_xyz = pyproj.transform(source, target, x=sat.sublong * 180. / ephem.pi, y=sat.sublat * 180. / ephem.pi, z=sat.elevation)
 
            sat_best_beams = closest_beams(float(lat), float(lon), sat_beams, max_beams)
            #1.66e9 is the satellite frequency in Hertz
            db_beam_losses(obs_xyz, sat_xyz, sat_best_beams, 1.66e9, 3.0)
                 
            if return_all == False:
                sat_best_beams = sorted(sat_best_beams, key=lambda b: -b[6])
 
            bb = sat_best_beams[0]
             
            if return_all == True:
                for sbb in sat_best_beams:
                    bbs.append((float(lat), float(lon), date.datetime().isoformat(), sbb, sat.alt))
            else:
                if 0 < sat.alt < 180 and (bb[6] > best or best == None):
                    best = bb[6]
                    bbs.append((float(lat), float(lon), date.datetime().isoformat(), bb, sat.alt))
 
            #print "Best match is " + bb[5] + " - Beam: " + str(bb[1]) + " - Point: " + str(bb[2])
            #print "Arc distance from beam point is " + str(round(bb[0]/1000, 3)) + " km"
            #print "Elevation is " + str(round(sat.alt, 2)) + " degrees"
            #print "Attenuation is " + str(round(bb[6], 2)) + " dB"
            #print "Signal power efficiency is " + str(round(bb[7]*100, 2)) + "% of power at beam center"
         
        if len(bbs) == 0:
            print "No available satellite found"
        else:
            if return_all:
                bests.append(bbs)
            else:
                bests.append(bbs[-1])
                 
    return bests
 
def load_tle(satname, url='http://www.celestrak.com/NORAD/elements/geo.txt'):
    """
        Download a satellite TLE.
        The function loads a standard a TLE file, like in the one pointed
        as default from the 'url' parameter and, if exists extract the three lines.
        A NotExistingTLE is raised is not TLE is found
        
        **satname** the name of the satellite a defined in the first TLE line
        **url** the URL of the file containing the TLE
    """
    tles = urllib2.urlopen(url).read()    
    splits = [x.strip() for x in tles.split("\n")]    
    index = splits.index(satname)
    ret = None
    if index:
        ret = (splits[index], splits[index + 1], splits[index + 2])
    return ret
 
if __name__ == '__main__':
    print best_beams('lat,lon,dat\n51,1,2013/06/08 04:00:00')