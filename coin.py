import random

class Coin:
	def __init__(self, grid):
		self._disp = '$'
		self._count = int(random.random() * 20 * grid.getFrame() + 20 * grid.getFrame())
		self.drawCoin(grid)

	def getDisp(self):
		return self._disp

	def drawCoin(self, grid):
		for _ in range(self._count):
			while(True):
				x = int(random.random() * (grid.getDim()[0] - 1))
				y = int(random.random() * (grid.getDim()[1] - 1))
				if grid.getBoardXY(x, y) == '.':
					grid.change(x, y, self._disp)
					break
