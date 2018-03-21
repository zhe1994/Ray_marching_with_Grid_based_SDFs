'''
Zhe Zeng
March 20, 2018
@Purdue
'''
import numpy as np
import os
import multiprocessing as mp
from itertools import repeat
import time
import argparse

from framebuffer import Framebuffer
from gridsdf import GridSDF
from readsdf import ReadTo
from camera import*

parser = argparse.ArgumentParser(description="Grid-based SDF Renderer Options")
parser.add_argument("--path", required=True, help="filename")
opt = parser.parse_args()

fb = Framebuffer(400, 400)
camera = PPC(fb.width_, fb.height_, 90.0)
#path = "bunny_watertight.sdf"
#path = "cube_static.sdf"
path = opt.path
grid_sdf = ReadTo(path)
num_workers = 6
parallel_mode = True
	
def Transform(ro):
	q = np.pi / 180.0 * 30.0
	ro[0] = ro[0] * np.cos(q) + ro[2] * np.sin(q)
	ro[2] = ro[2] * np.cos(q) - ro[0] * np.sin(q)
	ro[1] = ro[1]
	#ro = ro + [4.0, 0.0, 10.0]
	#ro = ro + np.array([0.0, 0.0, 1.5])
	ro = ro + np.array([1.0, 0.1, 1.5])
	#ro = ro + np.array([0.0, 0.5, 3.5])
	return ro
	
def LookUp(ro):
	ro = Transform(ro)
	if grid_sdf.InsideOfBB(ro):
		x = int((ro[0] - grid_sdf.min_[0]) / grid_sdf.dx_ + 0.5)
		y = int((ro[1] - grid_sdf.min_[1]) / grid_sdf.dx_ + 0.5)
		z = int((ro[2] - grid_sdf.min_[2]) / grid_sdf.dx_ + 0.5)
		return True, grid_sdf.data_[z][y][x]
	else:
		res = grid_sdf.UdBox(ro) + 0.5 * grid_sdf.dx_
		return False, res

def Ray(ro, rd):
	t = 1.0
	for i in range(60):
		flag, res = LookUp(ro + t * rd)
		if flag == False and res > 30.0:
			return 0.0
		elif flag == True:
			if res < 0.1:
				return t
			elif res > 20.0: 
				return 0.0
		t += res
		
	return 0.0

def ForEachLine(v, ro):
	depths_row = np.zeros(fb.width_, dtype=np.float)
	for u in range(fb.width_):
		ro = camera.center_
		rd = camera.GetRd(u, v)
		t = Ray(ro, rd)
		if t > 0.0:
			depth = Transform(ro + rd * t)[2]
		else:
			depth = np.finfo(np.float).min
		depths_row[u] = depth
	return depths_row

def UpdateDepthsP():
	ro = np.array([0.0, 0.0, 0.0])
	p = mp.Pool(num_workers)
	depths = np.array(p.starmap(ForEachLine, zip(range(fb.height_), repeat(ro))))
	p.close()
	return depths
	
def UpdateDepths():
	depths = np.zeros((fb.height_, fb.width_), dtype=np.float)
	min = np.finfo(np.float).max
	max = np.finfo(np.float).min
	for v in range(fb.height_):
		for u in range(fb.width_):
			ro = camera.center_
			rd = camera.GetRd(u, v)
			t = Ray(ro, rd)
			if t > 0.0:
				depth = Transform(ro + rd * t)[2]
				if depth < min: min = depth
				if depth > max: max = depth
			else:
				depth = 0.0
			depths[v][u] = depth
	return depths, min, max

def UpdateFramebuffer(depths, min, max):
	reciprocal_max_minus_min = 1.0 / (max - min)
	for v in range(fb.height_):
		for u in range(fb.width_):
			depth = depths[v][u]
			if depth != np.finfo(np.float).min:
				linear_param = (depths[v][u] - min) * reciprocal_max_minus_min
				color = int(255 * linear_param)
				fb.pixels_[v][u] = np.array([color, 0, 0])
			else:
				fb.pixels_[v][u] = [255, 255, 255]
	return fb
	
def RenderGraph(is_parallel=True):
	if is_parallel:
		def GetMinAndMax(depths):
			min = np.finfo(np.float).max
			max = np.finfo(np.float).min
			flag = False
			for depth_row in depths:
				for depth in depth_row:
					if depth != np.finfo(np.float).min:
						if depth < min: min = depth
						if depth > max: max = depth
			
			if max <= min: 	return 0.0, 1.0
			else:			return min, max
			
		elapsed = time.time()
		depths = UpdateDepthsP()		
		min, max = GetMinAndMax(depths)
	else:
		elapsed = time.time()
		depths, min, max = UpdateDepths()
	
	print("Computing Time\t", time.time() - elapsed)
	print("Depth Range\t", min, " to ", max)
	print("grid_sdf, min\t", grid_sdf.min_)
	print("grid_sdf, max\t", grid_sdf.max_)
	print("grid_sdf, b\t", grid_sdf.b_)
	fb = UpdateFramebuffer(depths, min, max)
	fb.Show()
	
if __name__ == "__main__":
	RenderGraph(parallel_mode)