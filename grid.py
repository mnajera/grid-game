import math, pygame


class Grid(object):

	def __init__(self, filename, pixel_w, pixel_h):
		self.load_file(filename)
		self.pixel_w = pixel_w
		self.pixel_h = pixel_h
		self.xscale = pixel_w / self.w
		self.yscale = pixel_h / self.h

	def value(self, x, y):
		index = x + (self.w * y)
		return self.data[index]

	def draw(self, screen, x_offset, y_offset):
		color = (0, 128, 255)
		for x in range(self.w):
			for y in range(self.h):
				bx = x * self.xscale
				by = y * self.yscale
				if self.value(x, y) == 'x':
					pygame.draw.rect(screen, (0, 0, 128), pygame.Rect(bx + x_offset, by + y_offset, self.xscale, self.yscale))

	def load_file(self, filename):
		with open(filename) as f:
			lines = [l.strip() for l in f.readlines()]
			self.h = len(lines)
			self.w = len(lines[0])
			self.data = []
			for l in lines:
				for e in l:
					self.data.append(e)

	def pixel_to_grid(self, pixel_x, pixel_y):
		return math.floor((pixel_x / self.pixel_w) * self.w), math.floor((pixel_y / self.pixel_h) * self.h)

	def grid_to_pixel(self, grid_x, grid_y):
		return grid_x / self.w * self.pixel_w, grid_y / self.h * self.pixel_h
