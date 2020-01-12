
class Person:
	def __init__(self, x, y, disp):
		self._x = x
		self._y = y
		self._disp = disp
		self._dim = self._disp.shape

	def drawPerson(self, grid):
		for i in range(self._dim[0]):
			for j in range(self._dim[1]):
				grid.change(self._x + i, self._y + j, self._disp[i][j])

	def render(self, grid):
		for i in range(self._dim[0]):
			for j in range(self._dim[1]):
				grid.change(self._x + i, self._y + j, '.')
