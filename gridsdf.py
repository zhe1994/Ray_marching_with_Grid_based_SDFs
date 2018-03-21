import numpy as np

class GridSDF:
	def __init__(self, ni, nj, nk, origin, dx):
		#The Mesh must be placed at the center of the coordinate
		self.data_ = np.zeros((nk, nj, ni))
		self.dx_ = dx
		self.b_ = 0.5 * (self.dx_) * np.array([ni - 2, nj - 2, nk - 2])
		self.min_ = origin + np.array([dx, dx, dx])
		self.max_ = self.min_ + 2.0 * self.b_
		
	def InsideOfBB(self, ro):
		if  ro[0] < self.min_[0] or\
			ro[1] < self.min_[1] or\
			ro[2] < self.min_[2]:
			return False
		elif ro[0] > self.max_[0] or\
			 ro[1] > self.max_[1] or\
			 ro[2] > self.max_[2]:
			 return False
		
		return True
		
	def UdBox(self, ro):
		d = np.abs(ro) - self.b_
		return np.linalg.norm(np.maximum(d, 0.0))
		#d = np.abs(ro) - self.b_;
		#return np.minimum(np.maximum(d[0], np.maximum(d[1], d[2])),0.0) + np.linalg.norm(np.maximum(d, 0.0))