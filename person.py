
class Person:
	def __init__(self, x, y, disp):
		self._x = x
		self._y = y
		self._disp = disp

	def drawPerson(self, grid):
		dim = self._disp.shape
		for i in range(dim[0]):
			for j in range(dim[1]):
				if self._disp[i][j] != ' ':
					grid.setBoardXY(self._x + i, self._y + j, self._disp[i][j])

	def render(self, grid):
		dim = self._disp.shape
		for i in range(dim[0]):
			for j in range(dim[1]):
				if self._disp[i][j] != ' ':
					grid.setBoardXY(self._x + i, self._y + j, ' ')
