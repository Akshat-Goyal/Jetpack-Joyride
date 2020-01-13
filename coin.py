import random
import numpy as np

class Coin:
	def __init__(self, grid, gridDim):
		self._disp = np.array(['$', '$', '$', '.'], ['.', '$', '$', '$'], ['$', '$', '$', '.'])
		self.drawCoin(grid, gridDim)

	def getDisp(self):
		return self._disp[0][0]

	def drawCoin(self, grid, gridDim):
		count = int(random.random() * 10 + 5)
		for _ in range(count):
			while(True):
				x = int(random.random() * (gridDim[0][1] - gridDim[0][0]) + gridDim[0][0])
				y = int(random.random() * (gridDim[1][1] - gridDim[1][0]) + gridDim[1][0])
				for i in range(x, min(x + self._disp.shape[0], gridDim[0][1])):
					for j in range(y, min(y + self._disp.shape[1], gridDim[1][1])):
						grid.changeXY(i, j, self._disp[i - x][j - y])
