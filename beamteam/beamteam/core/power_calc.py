import sys
import math
from beamteam.core.beamparser import parse_beam_data
import numpy
sys.path.append(".")
from beamteam.core.geoparser import *
from beamteam.core.earth_ellipsoid import *

max_beams = 20	# Number of closest beams we want to find as a first approximation

cust_ll = [31, 25]
sat_xyz = [30000000, 0, 0]

# Find an array of n beams which are closest (in arc distances) from a given point
# Returns their distances, beam number, and point number

def closest_beams(lat, lng, beam_data, n):
	
	arc_dist = []
	
	for i, beam in enumerate(beam_data):
		for j, p in enumerate(beam):
			d = haversine_dist(lat, lng, p[0], p[1])
			arc_dist.append([d, i, j, p[0], p[1], p[2]])

	# Sort distances
			
	arc_dist = sorted(arc_dist, key=lambda d: d[0])
	
	if n > 0 and n < len(arc_dist):
		return arc_dist[:n]
	else:
		return arc_dist

# Beam power geometric loss. Computes a factor (in dB) of loss from geometric factors:
# - distance in meters
# - angle misalignment in degrees
# Takes frequency in Hertz and half-power beamwidth as an argument, returns the factor in decibels

def db_beam_power_loss(S, e, f, hp_bw):
	return 20.0*math.log10(LIGHT_C/(f*4.0*math.pi*S)) - (12.0*(e/hp_bw)**2.0)

# Calculates losses for all beams in array

def db_beam_losses(cust_coords, sat_coords, beams, f, hp_bw):
	"""
		Appends to each beams the absolute_loss and the relative_loss 
	"""
	for b in beams:
		beam_coords = coords_to_xyz(b[3], b[4])
		S = numpy.linalg.norm(numpy.array(cust_coords)-numpy.array(sat_coords))
		cust_r = numpy.subtract(cust_coords, sat_coords).tolist()
		beam_r = numpy.subtract(beam_coords, sat_coords).tolist()
		e = math.acos(scalar_prod(cust_r, beam_r)/(vec_mod(cust_r)*vec_mod(beam_r)))*180.0/math.pi
		abs_loss = db_beam_power_loss(S, e, f, hp_bw)
		S_b = numpy.linalg.norm(numpy.array(beam_coords)-numpy.array(sat_coords))
		rel_loss = 10.0**((abs_loss-db_beam_power_loss(S_b, 0, f, hp_bw))/10.0)
		b.append(abs_loss)
		b.append(rel_loss)

# Calculate elevation on horizon

def sat_elevation(cust_coords, sat_coords):
	
	r = xyz_diff(sat_coords, cust_coords)
	zen = [cust_coords[0]/EARTH_A, cust_coords[1]/EARTH_A, cust_coords[2]/EARTH_B]
	el_angle = 90.0-math.acos(scalar_prod(zen, r)/(vec_mod(zen)*vec_mod(r)))/math.pi*180.0
	
	return el_angle

if __name__ == "__main__":

	sat_beams = parse_beam_data(f.readlines(), sys.argv[2])
	sat_best_beams = closest_beams(cust_ll[0], cust_ll[1], sat_beams, max_beams)
	db_beam_losses(coords_to_xyz(cust_ll[0], cust_ll[1]), sat_xyz, sat_best_beams, 1.66e9, 3.0)
	
	sat_best_beams = sorted(sat_best_beams, key=lambda b: -b[6])
	
	bb = sat_best_beams[0]
	el = sat_elevation(coords_to_xyz(cust_ll[0], cust_ll[1]), sat_xyz)
	
	print "Best match is " + bb[5] + " - Beam: " + str(bb[1]) + " - Point: " + str(bb[2])
	print "Arc distance from beam point is " + str(round(bb[0]/1000, 3)) + " km"
	print "Elevation is " + str(round(el, 2)) + " degrees"
	if el < 0 or el > 180:
		print "WARNING: satellite is beyond the horizon and is not observable"
	print "Attenuation is " + str(round(bb[6], 2)) + " dB"
	print "Signal power efficiency is " + str(round(bb[7]*100, 2)) + "% of power at beam center" 
	
