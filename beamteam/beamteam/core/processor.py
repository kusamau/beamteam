import sys
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
        print sat.alt, sat.az, sat.range, sat.sublat, sat.sublong, obs.date.datetime() 
        print sat_xyz, map(lambda x,y: x-y, sat_xyz, obs_xyz)
    return sat


constellation = {
    'AMER': 'INMARSAT-4-F3.tle',
    'EMEA': 'INMARSAT-4-F2.tle',
#    'ASIP': 'INMARSAT-4-F1.tle',
}


def best_beams(coordinates):

    values = [line.split(',') for line in coordinates.split('\n')]
    values.pop(0)

    return do_best_beams(values)

def do_best_beams(values):
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

        print obs_xyz

        bbs = []
        best = -100000000

        for label, tlepath in constellation.items():
            f = open('pseudobeams.csv')
            sat_beams = parse_beam_data(f.readlines(), label)

            tle = open(tlepath).readlines()
            sat = ephem.readtle(*tle)

            sat.compute(obs)
            sat_xyz = pyproj.transform(source, target, x=sat.sublong * 180. / ephem.pi, y=sat.sublat * 180. / ephem.pi, z=sat.elevation)
            
            print sat.alt, sat.az, sat.range, sat.sublat, sat.sublong, obs.date.datetime()
            print sat_xyz, map(lambda x,y: x-y, sat_xyz, obs_xyz)

            sat_best_beams = closest_beams(float(lat), float(lon), sat_beams, max_beams)
            #1.66e9 is the satellite frequency in Hertz
            db_beam_losses(obs_xyz, sat_xyz, sat_best_beams, 1.66e9, 3.0)
                
            sat_best_beams = sorted(sat_best_beams, key=lambda b: -b[6])

            bb = sat_best_beams[0]

            if 0 < sat.alt < 180 and bb[6] > best:
                best = bb[6]
                bbs.append((float(lat), float(lon), date.datetime().isoformat(), bb, sat.alt))

            print "Best match is " + bb[5] + " - Beam: " + str(bb[1]) + " - Point: " + str(bb[2])
            print "Arc distance from beam point is " + str(round(bb[0]/1000, 3)) + " km"
            print "Elevation is " + str(round(sat.alt, 2)) + " degrees"
            print "Attenuation is " + str(round(bb[6], 2)) + " dB"
            print "Signal power efficiency is " + str(round(bb[7]*100, 2)) + "% of power at beam center"

        bests.append(bbs[-1])

    return bests



if __name__ == '__main__':
    best_beams('lat,lon,dat\n51,1,2013/06/08 04:00:00')
