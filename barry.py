from person import Person
import numpy as np


class Barry(Person):
	def __init__(self, grid, lives):
		self._disp = np.array([[' ', '_', ' '], ['{', 'o', '}'], ['/', '_', '\\']])
		gridDim = grid.getDim()
		Person.__init__(self, gridDim[0][1] - self._disp.shape[0], gridDim[1][0], self._disp)
		self._score = 0
		self._maxLive = lives
		self._lives = lives

	def checkCoin(self, grid, coin):
		dim = self._disp.shape
		for i in range(dim[0]):
			for j in range(dim[1]):
				if self._disp[i][j] == ' ':
					continue
				if grid.getBoardXY(i + self._x, j + self._y) == coin.getDisp():
					grid.setBoardXY(i + self._x, j + self._y, ' ')
					self._score += 1

	def move(self, y, grid, coin, beam):
		dim = self._disp.shape
		if self._y + y + dim[1] >= grid.getDim()[1][1] + 1:
			self._y = grid.getDim()[1][1] - dim[1]
		elif self._y + y < grid.getDim()[1][0]:
			self._y = grid.getDim()[1][0]
		else:
			self._y += y
		self.checkCoin(grid, coin)
		if beam.checkCol(self, grid):
			self._lives -= 1
		if not self._lives:
			grid.gameOver()

	def getXY(self):
		return [self._x, self._y]

	def getDisp(self):
		return self._disp

	def getScore(self):
		return self._score

	def getLive(self):
		return self._lives / self._maxLive * 100

	def jump(self):
		pass

	def gravity(self, grid):
		pass
