import sys
import math

# Data from the WGS 84 ellipsoid model

EARTH_A = 6378137		#meters
EARTH_B = 6356752.3142	#meters
EARTH_AVG_R = (EARTH_A**2*EARTH_B)**(1.0/3.0)

# Lightspeed

LIGHT_C = 3e8 # meters/s

# Simple Cartesian distance calculator

def xyz_distance(r1, r2):
	'''
		Deprecated. Use:
			numpy.subtract(coords_1, coords_2)
	'''
	return math.sqrt((r1[0]-r2[0])**2+(r1[1]-r2[1])**2+(r1[2]-r2[2])**2)

# Vector diff

def xyz_diff(r1, r2):
	'''
		Deprecated. Use:
			numpy.linalg.norm(coords_1 - coords_2)
	'''
	return [r1[0]-r2[0], r1[1]-r2[1], r1[2]-r2[2]]

# Vector module

def vec_mod(r):
	return math.sqrt(r[0]**2.0+r[1]**2.0+r[2]**2.0)

# Simple scalar product

def scalar_prod(r1, r2):
	return r1[0]*r2[0]+r1[1]*r2[1]+r1[2]*r2[2]

# Takes latitude and longitude in degrees, turns them into xyz coordinates in meters - z is rotation axis, x-z plane contains Greenwich
# Altitude is an optional argument

def coords_to_xyz(lat, lng, alt = 0.0):
	
	rad_lat = lat/180.0*math.pi
	rad_lng = lng/180.0*math.pi
	
	# Level-of-sea position
	
	z = EARTH_B*math.sin(rad_lat)
	x = EARTH_A*math.cos(rad_lat)*math.cos(rad_lng)
	y = EARTH_A*math.cos(rad_lat)*math.sin(rad_lng)
	
	# Zenithal versor
	z_x = 2.0*x/EARTH_A
	z_y = 2.0*y/EARTH_A
	z_z = 2.0*z/EARTH_B
	z_mod = xyz_distance([z_x, z_y, z_z], [0, 0, 0])
	z_x *= alt/z_mod
	z_y *= alt/z_mod
	z_z *= alt/z_mod
	x += z_x
	y += z_y
	z += z_z
	
	return x, y, z

# Gives off arc distance in meters between two points on Earth

def haversine_dist(lat1, lng1, lat2, lng2):
	
	rad_lat1 = lat1/180.0*math.pi
	rad_lat2 = lat2/180.0*math.pi
	rad_lng1 = lng1/180.0*math.pi
	rad_lng2 = lng2/180.0*math.pi
	dlat = abs(rad_lat1-rad_lat2)
	dlng = abs(rad_lng1-rad_lng2)
	hs = 2.0*math.asin(math.sqrt(math.sin(dlat/2.0)**2+math.cos(rad_lat1)*math.cos(rad_lat2)*math.sin(dlng/2.0)**2))
	return EARTH_AVG_R*hs


if __name__ == "__main__":

	lat = float(sys.argv[1])
	lng = float(sys.argv[2])
	
	print coords_to_xyz(lat, lng)
	
