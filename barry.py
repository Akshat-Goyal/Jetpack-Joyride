from person import Person
import numpy as np


class Barry(Person):
	def __init__(self, grid):
		self._disp = np.array([[' ', '_', ' '], ['{', 'o', '}'], ['/', '_', '\\']])
		self._dim = self._disp.shape
		Person.__init__(self, grid.getDim()[0] - self._dim[0] - 2, 0, self._disp)
		self._score = 0

	def checkCoin(self, grid, coin):
		for i in range(self._dim[0]):
			for j in range(self._dim[1]):
				if grid.getBoardXY(i + self._x, j + self._y) == coin.getDisp():
					grid.change(i + self._x, j + self._y, '.')
					self._score += 1

	def move(self, y, grid, coin):
		if self._y + y + self._dim[1] >= grid.getGridRange()[1] + 1:
			self._y = grid.getGridRange()[1] - self._dim[1]
		elif self._y + y < grid.getGridRange()[0]:
			self._y = grid.getGridRange()[0]
		else:
			self._y += y
		self.checkCoin(grid, coin)

	def getScore(self):
		return self._score

	def jump(self):
		pass

	def gravity(self, grid):
		pass
