import numpy as np
from gridsdf import GridSDF

def ReadTo(filename):
	f = open(filename, "r")
	dimensions = (f.readline().rstrip('\n')).split(' ')
	ni = int(dimensions[0])
	nj = int(dimensions[1])
	nk = int(dimensions[2])
	origin = (f.readline().rstrip('\n')).split(' ')
	origin = np.array([float(origin[0]), float(origin[1]), float(origin[2])])
	dx = float(f.readline().rstrip('\n'))
	
	grid_sdf = GridSDF(ni, nj, nk, origin, dx)
	
	for k in range(nk):
		for j in range(nj):
			for i in range(ni):
				dist = float(f.readline().rstrip('\n'))
				grid_sdf.data_[k][j][i] = dist
				
	return grid_sdf