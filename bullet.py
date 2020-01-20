import numpy as np

class Bullet:
	def __init__(self):
		self._disp = np.array([['B']])
		self._arr = set()

	def objCol(self, x, y, obj):
		isCol = 0
		isCol |= y + self._disp.shape[1] > obj['grid'].getDim()[1][1]
		if not isCol:
			isCol |= obj['beam'].checkCol(x, y, self._disp, obj)
			isCol |= obj['magnet'].checkCol(x, y, self._disp, obj)
			isCol |= obj['speedBoost'].checkCol(x, y, self._disp, obj, False)
			isCol |= obj['coin'].checkCol(x, y, self._disp, obj) > 0
			if obj['boss'].isBossReady():
				isCol |= obj['boss'].checkCol(x, y, self._disp, obj, True)
		return isCol

	def changeY(self, y, obj):
		tmp = set()
		for i in self._arr:
			br = 0
			for j in range(y + 1):
				if self.objCol(i[0], i[1] + j, obj):
					br = 1
					break
			if not br:
				tmp.add((i[0], i[1] + y))
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
