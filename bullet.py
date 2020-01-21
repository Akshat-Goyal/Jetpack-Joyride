import numpy as np
import colorama
from colorama import Back, Fore, Style
import time

class Bullet:
	def __init__(self):
		self._disp = np.array([[':', ':', ':']])
		self._col = Fore.MAGENTA + Back.BLACK
		self._shootTime = 0.5
		self._curTime = 0
		self._arr = set()

	def objCol(self, x, y, obj):
		isCol = 0
		isCol |= y + self._disp.shape[1] > obj['grid'].getDim()[1][1]
		if not isCol:
			isCol |= obj['beam'].checkCol(x, y, self._disp, obj)
			isCol |= obj['magnet'].checkCol(x, y, self._disp, obj)
			isCol |= obj['iceBall'].checkCol(x, y, self._disp, obj)
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


	def render(self, obj):
		dim = self._disp.shape
		for i in self._arr:
			for j in range(dim[0]):
				for k in range(dim[1]):
					if self._disp[j][k] != ' ':
						obj['grid'].setBoardXY(i[0] + j, i[1] + k, Back.BLACK + Fore.BLACK + ' ')
		

	def checkCol(self, x, y, disp, obj):
		dim = disp.shape
		ar = []
		for i in self._arr:
			br = 0
			if y + dim[1] <= i[1] or i[1] + self._disp.shape[1] <= y:
				return False
			if x >= i[0] + self._disp.shape[0] or i[0] >= x + dim[0]:
				return False
			for j in range(self._disp.shape[0]):
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
		for i in ar:
			self._arr.remove(i)
		return len(ar) > 0

	def drawWeapon(self, obj):
		dim = self._disp.shape
		for i in self._arr:
			for j in range(dim[0]):
				for k in range(dim[1]):
					if self._disp[j][k] != ' ':
						obj['grid'].setBoardXY(i[0] + j, i[1] + k, self._col + self._disp[j][k])

	def makeWeapon(self, x, y, obj):
		if self._curTime:
			if int(round(time.time())) - self._curTime > self._shootTime:
				self._curTime = 0
			return
		else:
			self._curTime = int(round(time.time()))
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
