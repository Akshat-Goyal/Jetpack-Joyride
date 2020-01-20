import numpy as np
from obstacle import Obstacle
import random

class FireBeam(Obstacle):
	def __init__(self):
		self._disp = np.array([np.array([['_', '_']]), np.array([['|'], ['|']]), np.array([[' ', '/'], ['/', ' ']]), np.array([['\\', ' '], [' ', '\\']])])
		Obstacle.__init__(self, self._disp)

	def changeY(self, obj):
		tmp = set()
		for i in self._arr:
			tmp.add(((i[0][0], i[0][1] - 1), i[1]))
			if i[0][1] > obj['grid'].getDim()[1][0]:
				tmp.add(((i[0][0], i[0][1] - 1), i[1]))
		self._arr = tmp

	def checkCol(self, x, y, disp, obj):
		ar = []
		dim = disp.shape
		for i in self._arr:
			if y + dim[1] <= i[0][1] or i[0][1] + self._disp[i[1]].shape[1] <= y:
				continue
			if x >= i[0][0] + self._disp[i[1]].shape[0] or i[0][0] >= x + dim[0]:
				continue
			for j in range(self._disp[i[1]].shape[0]):
				br = 0
				for k in range(self._disp[i[1]].shape[1]):
					if self._disp[i[1]][j][k] ==  ' ':
						continue
					if i[0][0] + j - x < 0 or i[0][0] + j - x >= dim[0]:
						continue
					if i[0][1] + k - y < 0 or i[0][1] + k - y >= dim[1]:
						continue
					if disp[i[0][0] + j - x][i[0][1] + k - y] != ' ':
						ar.append(i)
						br = 1
						break
				if br:
					break
		self.removeObstacle(ar, obj)
		return len(ar) > 0

	def removeObstacle(self, ar, obj):
		for i in ar:
			self._arr.remove(i)
			for j in range(self._disp[i[1]].shape[0]):
				for k in range(self._disp[i[1]].shape[1]):
					if self._disp[i[1]][j][k] != ' ':
						obj['grid'].setBoardXY(j + i[0][0], k + i[0][1], ' ')

	def drawObstacle(self, obj, frameNo):
		count = int(random.random() * 5 + 2)
		gridDim = obj['grid'].getDim()
		for _ in range(count):
			while True:
				z = int(random.random() * 3)
				x = int(random.random() * (gridDim[0][1] - gridDim[0][0] - self._disp[z].shape[0]) + gridDim[0][0])
				y = int(random.random() * (gridDim[1][1] - gridDim[1][0] - self._disp[z].shape[1]) + gridDim[1][0])
				flag = 0
				for j in range(self._disp[z].shape[0]):
					for k in range(self._disp[z].shape[1]):
						if self._disp[z][j][k] ==  ' ':
							continue
						if obj['grid'].getBoardXY(x + j, y + k) != ' ' and obj['grid'].getBoardXY(x + j, y + k) != obj['coin'].getDisp():
							flag = 1
							break
					if flag:
						break
				if not flag:
					self._arr.add(((x, y + frameNo * gridDim[1][1]), z))
					for i in range(self._disp[z].shape[0]):
						for j in range(self._disp[z].shape[1]):
							if self._disp[z][i][j] != ' ':
								obj['grid'].setBoardXY(i + x, j + y + frameNo * gridDim[1][1], self._disp[z][i][j])
					break
