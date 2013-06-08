import sys

# Parses NORAD data on satellite positions
# Takes file lines as string array and the name of the satellite of interest as a string
# Returns a block of two lines of orbital data

def parse_sat_data(f_lines, sat_name):
	
	l_iter = iter(f_lines)
	dblock = [[],[]]
	
	for l in l_iter:
		if sat_name in l:
			for i in range(0, 2):
				dblock[i] = l_iter.next().split()

	return dblock

if __name__ == "__main__":

	f = open(sys.argv[1])
	
	print parse_sat_data(f.readlines(), sys.argv[2])
	
