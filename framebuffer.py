import numpy as np
from PIL import Image
from io import BytesIO
import win32clipboard

class Framebuffer:
	def __init__(self, width, height):
		self.width_ = width
		self.height_ = height
		self.resolution_ = np.array([width, height])
		self.pixels_ = np.zeros((height, width, 3), dtype = np.uint8)
	
	def Show(self):
		img = Image.fromarray(self.pixels_, 'RGB')
		img.show()
		img.close()
	
	def Save(self, name):
		img = Image.fromarray(self.pixels_, 'RGB')
		img.save(name)