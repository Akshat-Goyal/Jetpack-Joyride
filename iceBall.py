import numpy as np
import random

class IceBall:
	def __init__(self):
		self._disp = np.array([['S']])
		self._arr = set()

	def objCol(self, x, y, obj):
		isCol = 0
		isCol |= x + self._disp.shape[0] > obj['grid'].getDim()[0][1]
		isCol |= y < obj['grid'].getDim()[1][0]
		if not isCol:
			isCol |= obj['beam'].checkCol(x, y, self._disp, obj)
			isCol |= obj['magnet'].checkCol(x, y, self._disp, obj)
			isCol |= obj['coin'].checkCol(x, y, self._disp, obj) > 0
			isCol |= obj['barry'].checkCol(x, y, self._disp, obj)
		return isCol

	def changeY(self, obj):
		tmp = set()
		vy = int(random.random() * 1) + 1
		vx = int(random.random() + 0.25)
		for i in self._arr:
			br = 0
			j = 1
			k = 1
			while j <= vy or k <= vx:
				if j <= vy:
					if self.objCol(i[0], i[1] - j, obj):
						br = 1
						break
					j += 1
				if k <= vx:
					if self.objCol(i[0] + k, i[1], obj):
						br = 1
						break
					k += 1
			if not br:
				tmp.add((i[0] + vx, i[1] - vy))
		self._arr = tmp

	def drawWeapon(self, obj):
		dim = self._disp.shape
		for i in self._arr:
			for j in range(dim[0]):
				for k in range(dim[1]):
					if self._disp[j][k] != ' ':
						obj['grid'].setBoardXY(i[0] + j, i[1] + k, self._disp[j][k])

	def render(self, obj):
		dim = self._disp.shape
		for i in self._arr:
			for j in range(dim[0]):
				for k in range(dim[1]):
					if self._disp[j][k] != ' ':
						obj['grid'].setBoardXY(i[0] + j, i[1] + k, ' ')
		

	def makeWeapon(self, x, y, obj):
		if x + self._disp.shape[0] > obj['grid'].getDim()[0][1]:
			x = obj['grid'].getDim()[0][1] - self._disp.shape[0]
		elif x < obj['grid'].getDim()[0][0]:
			x = obj['grid'].getDim()[0][0]
		if not self.objCol(x, y, obj):
			if (x, y) in self._arr:
				return
			self._arr.add((x, y))
			for i in range(self._disp.shape[0]):
				for j in range(self._disp.shape[1]):
					if self._disp[i][j] != ' ':
						obj['grid'].setBoardXY(i + x, j + y, self._disp[i][j])
