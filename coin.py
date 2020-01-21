import random
import numpy as np
import colorama
from colorama import Fore, Back, Style

class Coin:
	def __init__(self):
		self._col =  Back.BLACK + Fore.YELLOW
		self._chCoin = self._col + '$'
		self._disp = np.array([['$', '$', '$', '$', '$']])
		self._arr = set()

	def get_disp(self):
		return self._chCoin

	def set_XY(self, obj):
		tmp = set()
		for i in self._arr:
			if i[1] > obj['grid'].get_dim()[1][0]:
				tmp.add((i[0], i[1] - 1))
		self._arr = tmp

	def checkCol(self, x, y, disp, obj):
		dim = disp.shape
		score = 0
		for i in range(dim[0]):
			for j in range(dim[1]):
				if disp[i][j] == ' ':
					continue
				if obj['grid'].get_XY(i + x, j + y) == self._chCoin:
					self._arr.remove((i + x, j + y))
					obj['grid'].set_XY(i + x, j + y, obj['grid'].get_col() + ' ')
					score += 1
		return score

	def drawCoin(self, obj):
		for i in self._arr:
			if i[1] < obj['grid'].get_dim()[1][1]:
				obj['grid'].set_XY(i[0], i[1], self._chCoin)

	def makeCoin(self, obj, frameNo):
		count = int(random.random() * 5 + 5)
		gridDim = obj['grid'].get_dim()
		for _ in range(count):
			x = int(random.random() * (gridDim[0][1] - gridDim[0][0] - 1) + gridDim[0][0])
			y = int(random.random() * (gridDim[1][1] - gridDim[1][0] - 1) + gridDim[1][0])
			for i in range(x, min(x + self._disp.shape[0], gridDim[0][1])):
				for j in range(y, min(y + self._disp.shape[1], gridDim[1][1])):
					if self._disp[i - x][j - y] != ' ':
						self._arr.add((i, j + frameNo * gridDim[1][1]))
						obj['grid'].set_XY(i, j + frameNo * gridDim[1][1], self._col + self._disp[i - x][j - y])
