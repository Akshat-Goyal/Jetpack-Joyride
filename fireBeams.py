import numpy as np
from obstacle import Obstacle
import random

class FireBeam(Obstacle):
	def __init__(self):
		self._disp = np.array([np.array([['_', '_']]), np.array([['|'], ['|']]), np.array([[' ', '/'], ['/', ' ']]), np.array([['\\', ' '], [' ', '\\']])])
		self._arr = set()

	def changeY(self):
		ar = []
		tmp = set()
		for i in self._arr:
			tmp.add(((i[0][0], i[0][1] - 1), i[1]))
			if i[0][1] < 1:
				ar.append(((i[0][0], i[0][1] - 1), i[1]))
		self._arr = tmp
		for i in ar:
			self._arr.remove(i)

	def isFireBeam(self, x, y, obj, i):
		if not len(self._arr):
			return False
		if y + obj.shape[1] <= i[0][1] or i[0][1] + self._disp[i[1]].shape[1] <= y:
			return False
		if x >= i[0][0] + self._disp[i[1]].shape[0] or i[0][0] >= x + obj.shape[0]:
			return False
		for j in range(self._disp[i[1]].shape[0]):
			for k in range(self._disp[i[1]].shape[1]):
				if self._disp[i[1]][j][k] ==  ' ':
					continue
				if i[0][0] + j - x < 0 or i[0][0] + j - x >= obj.shape[0]:
					continue
				if i[0][1] + k - y < 0 or i[0][1] + k - y >= obj.shape[1]:
					continue
				if obj[i[0][0] + j - x][i[0][1] + k - y] != ' ':
					return True
		return False

	def removeFireBeam(self, i, grid):
		for j in range(self._disp[i[1]].shape[0]):
			for k in range(self._disp[i[1]].shape[1]):
				if self._disp[i[1]][j][k] != ' ':
					grid.setBoardXY(j + i[0][0], k + i[0][1], ' ')

	def checkCol(self, barry, grid):
		ar = []
		for i in self._arr:
			if self.isFireBeam(barry.getXY()[0], barry.getXY()[1], barry.getDisp(), i):
				ar.append(i)
		for i in ar:
			self.removeFireBeam(i, grid)
			self._arr.remove(i)
		return len(ar) > 0

	def drawFireBeams(self, grid, frameNo):
		count = int(random.random() * 5 + 2)
		gridDim = grid.getDim()
		for _ in range(count):
			while True:
				z = int(random.random() * 3)
				x = int(random.random() * (gridDim[0][1] - gridDim[0][0] - self._disp[z].shape[0]) + gridDim[0][0])
				y = int(random.random() * (gridDim[1][1] - gridDim[1][0] - self._disp[z].shape[1]) + gridDim[1][0])
				flag = 0
				for i in self._arr:
					flag |= self.isFireBeam(x, y, self._disp[z], i)
				if not flag:
					self._arr.add(((x, y + frameNo * gridDim[1][1]), z))
					for i in range(self._disp[z].shape[0]):
						for j in range(self._disp[z].shape[1]):
							if self._disp[z][i][j] != ' ':
								grid.setBoardXY(i + x, j + y + frameNo * gridDim[1][1], self._disp[z][i][j])
					break
