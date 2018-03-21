import numpy as np

class PPC:
	def __init__(self, width, height, hfov):
		self.width_ = width
		self.height_ = height
		self.center_ = np.zeros(3, dtype=np.float32)
		self.a_ = np.array([1.0, 0.0, 0.0], dtype=np.float32)
		self.b_ = np.array([0.0, -1.0, 0.0], dtype=np.float32)
		half = 0.5 * (hfov * (np.pi / 180.0))
		self.c_ = np.array([-0.5 * width, 0.5 * height, float(-0.5 * width) / (np.tan(half))])
		
	def GetRd(self, u, v):
		point_to =  self.c_ + \
					self.a_ * (u + 0.5) + \
					self.b_ * (v + 0.5)
		return point_to / np.linalg.norm(point_to)