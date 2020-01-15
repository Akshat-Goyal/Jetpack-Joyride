import numpy as np
from obstacle import Obstacle
import random

class Magnet(Obstacle):
	def __init__(self):
		self._disp = np.array([['M']])
		self._arr = set()

	def changeY(self):
		ar = []
		tmp = set()
		for i in self._arr:
			tmp.add((i[0], i[1] - 1))
			if i[1] < 1:
				ar.append((i[0], i[1] - 1))
		self._arr = tmp
		for i in ar:
			self._arr.remove(i)

	def isMagnet(self, x, y, obj, i):
		if not len(self._arr):
			return False
		if y + obj.shape[1] <= i[1] or i[1] + self._disp.shape[1] <= y:
			return False
		if x >= i[0] + self._disp.shape[0] or i[0] >= x + obj.shape[0]:
			return False
		for j in range(self._disp.shape[0]):
			for k in range(self._disp.shape[1]):
				if self._disp[j][k] ==  ' ':
					continue
				if i[0] + j - x < 0 or i[0] + j - x >= obj.shape[0]:
					continue
				if i[1] + k - y < 0 or i[1] + k - y >= obj.shape[1]:
					continue
				if obj[i[0] + j - x][i[1] + k - y] != ' ':
					return True
		return False

	def checkMagnet(self, barry, grid, coin, beam):
		l = 0
		u = 0
		x = barry.getXY()[0]
		y = barry.getXY()[1]
		bDim = barry.getDisp().shape
		for i in self._arr:
			if i[1] >= grid.getDim()[1][1]:
				continue
			if i[0] < x:
				u -= 1
			if i[0] + self._disp.shape[0] > x + bDim[0]:
				u += 1
			if i[1] < y:
				l -= 1
			if i[1] + self._disp.shape[1] > y + bDim[1]:
				l += 1
		while l | u:
			if l:
				barry.move(l / abs(l), grid, coin, beam)
				l = int((abs(l) - 1) * l / abs(l))
			if u:
				barry.jump(u / abs(u), grid, coin, beam)
				u = int((abs(u) - 1) * u / abs(u))


	def drawMagnet(self, grid):
		for i in self._arr:
			if i[1] >= grid.getDim()[1][1]:
				continue
			x = i[0]
			y = i[1]
			for j in range(self._disp.shape[0]):
				for k in range(self._disp.shape[1]):
					if self._disp[j][k] != ' ':
						grid.setBoardXY(j + x, k + y, self._disp[j][k])

	def makeMagnet(self, grid, frameNo):
		count = int(random.random() + 1)
		gridDim = grid.getDim()
		for _ in range(count):
			while True:
				x = int(random.random() * (gridDim[0][1] - gridDim[0][0] - self._disp.shape[0]) + gridDim[0][0])
				y = int(random.random() * (gridDim[1][1] - gridDim[1][0] - self._disp.shape[1]) + gridDim[1][0])
				flag = 0
				for i in self._arr:
					flag |= self.isMagnet(x, y, self._disp, i)
				if not flag:
					self._arr.add((x, y + frameNo * gridDim[1][1]))
					for i in range(self._disp.shape[0]):
						for j in range(self._disp.shape[1]):
							if self._disp[i][j] != ' ':
								grid.setBoardXY(i + x, j + y + frameNo * gridDim[1][1], self._disp[i][j])
					break
