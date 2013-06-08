
import ephem
import pyproj

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

if __name__ == '__main__':
    day_trajectory('INMARSAT-4-F2.tle')
