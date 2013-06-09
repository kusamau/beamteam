'''
Created on 9 Jun 2013

@author: Simone Storniolo
'''
import sys
 
#Parser for beam data: takes as input file lines and satellite of interest name, returns a nested array containing a
# [latitude, longitude, name]
# array for each beam and point
 
def parse_beam_data(f_lines, sat_name):
 
    n_beams = 0
    n_points = []
    dblock = []
     
    for l in f_lines:
        if "beam,pointorder,latitude,longitude,satellite" in l:
            continue
        spl_data = l.split(',')
        sat = spl_data[4].rstrip()
        if sat_name != sat:
            continue
        beam = int(spl_data[0])
        point = int(spl_data[1])
        if beam > n_beams:
            dblock.append([])
            n_points.append(0)
            n_beams += 1
        if point > n_points[beam-1]:
            dblock[beam-1].append([])
            n_points[beam-1] += 1
        dblock[beam-1][point-1] = [float(spl_data[2]), float(spl_data[3]), sat]
     
    return dblock
     
if __name__ == "__main__":
 
    f = open(sys.argv[1])
     
    print parse_beam_data(f.readlines(), sys.argv[2])