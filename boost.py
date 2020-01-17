import numpy as np
import random

class speed_boost:

	def __init__(self, boostTime):
		self._disp = np.array([['2']])
		self._arr = set()
		self._boostTime = boostTime
		self._curTime = 0
		self._boostOn = 0

	def isBoostOn(self):
		return self._boostOn

	def checkBoostT(self):
		if self._boostOn:
			self._curTime += 1
			if self._curTime == self._boostTime:
				self._curTime = 0
				self._boostOn = 0 

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

	def checkBoost(self, x, y, disp, obj):
		ar = []
		dim = disp.shape
		for i in self._arr:
			if y + dim[1] <= i[1] or i[1] + self._disp.shape[1] <= y:
				continue
			if x >= i[0] + self._disp.shape[0] or i[0] >= x + dim[0]:
				continue
			for j in range(self._disp.shape[0]):
				br = 0
				for k in range(self._disp.shape[1]):
					if self._disp[j][k] ==  ' ':
						continue
					if i[0] + j - x < 0 or i[0] + j - x >= dim[0]:
						continue
					if i[1] + k - y < 0 or i[1] + k - y >= dim[1]:
						continue
					if disp[i[0] + j - x][i[1] + k - y] != ' ':
						ar.append(i)
						br = 1
						break
				if br:
					break
		if len(ar) > 0:
			self._boostOn = 1
			self._boostTime = 0
			self.removeBoost(ar, obj)
		return len(ar) > 0

	def removeBoost(self, ar, obj):
		for i in ar:
			self._arr.remove(i)
			for j in range(self._disp.shape[0]):
				for k in range(self._disp.shape[1]):
					if self._disp[j][k] != ' ':
						obj['grid'].setBoardXY(j + i[0], k + i[1], ' ')

	def drawBoost(self, obj, frameNo):
		count = int(random.random() + 0.5)
		gridDim = obj['grid'].getDim()
		for _ in range(count):
			while True:
				x = int(random.random() * (gridDim[0][1] - gridDim[0][0] - self._disp.shape[0]) + gridDim[0][0])
				y = int(random.random() * (gridDim[1][1] - gridDim[1][0] - self._disp.shape[1]) + gridDim[1][0])
				flag = 0
				for j in range(self._disp.shape[0]):
					for k in range(self._disp.shape[1]):
						if self._disp[j][k] ==  ' ':
							continue
						if obj['grid'].getBoardXY(x + j, y + k) != ' ' and obj['grid'].getBoardXY(x + j, y + k) != obj['coin'].getDisp():
							flag = 1
							break
				if not flag:
					self._arr.add((x, y + frameNo * gridDim[1][1]))
					for i in range(self._disp.shape[0]):
						for j in range(self._disp.shape[1]):
							if self._disp[i][j] != ' ':
								obj['grid'].setBoardXY(i + x, j + y + frameNo * gridDim[1][1], self._disp[i][j])
					break
