from person import Person
import numpy as np


class Barry(Person):
	
	def __init__(self, x, y):
		self._disp = np.array([['/', '\\'], ['\\', '/']])
		self._dim = (2, 2)
		Person.__init__(self, x, y, self._dim, self._disp)

	def move(self, x, y, grid):
		if self._y + y + self._dim[0] >= grid.getBreadth() - 1:
			self._y = grid.getBreadth() - self._dim[0] - 2
		elif self._y + y < 2:
			self._y = 2
		else:
			self._y += y

		if self._x + x + self._dim[1] >= grid.getLength() - 1:
			self._x = grid.getLength() - self._dim[1] - 2
		elif self._x + x < 2:
			self._x = 2
		else:
			self._x += x