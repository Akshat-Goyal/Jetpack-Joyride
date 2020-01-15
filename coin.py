import random
import numpy as np

class Coin:
	def __init__(self):
		self._chCoin = '$'
		self._disp = np.array([['$', '$', '$', ' '], [' ', '$', '$', '$']])

	def getDisp(self):
		return self._chCoin

	def drawCoin(self, grid, frameNo):
		count = int(random.random() * 10 + 5)
		gridDim = grid.getDim()
		for _ in range(count):
			x = int(random.random() * (gridDim[0][1] - gridDim[0][0] - 1) + gridDim[0][0])
			y = int(random.random() * (gridDim[1][1] - gridDim[1][0] - 1) + gridDim[1][0])
			for i in range(x, min(x + self._disp.shape[0], gridDim[0][1])):
				for j in range(y, min(y + self._disp.shape[1], gridDim[1][1])):
					grid.setBoardXY(i, j + frameNo * gridDim[1][1], self._disp[i - x][j - y])
