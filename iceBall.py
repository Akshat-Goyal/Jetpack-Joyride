import numpy as np
import random
import colorama
from colorama import Back, Fore, Style

class IceBall:
	def __init__(self):
		self._disp = np.array([[':', ':', ':'], [':', ':', ':'], [':', ':', ':']])
		self._col = Back.BLACK + Fore.WHITE
		self._vy = 4
		self._arr = set()

	def objCol(self, x, y, obj):
		isCol = 0
		isCol |= y < obj['grid'].getDim()[1][0]
		if not isCol:
			isCol |= obj['beam'].checkCol(x, y, self._disp, obj)
			isCol |= obj['magnet'].checkCol(x, y, self._disp, obj)
			isCol |= obj['coin'].checkCol(x, y, self._disp, obj) > 0
			isCol |= obj['bullet'].checkCol(x, y, self._disp, obj)
			isCol |= obj['barry'].checkCol(x, y, self._disp, obj)
		return isCol

	def changeY(self, obj):
		tmp = set()
		for i in self._arr:
			br = 0
			j = 1
			while j <= self._vy:
				if self.objCol(i[0], i[1] - j, obj):
					br = 1
					break
				j += 1
			if not br:
				tmp.add((i[0], i[1] - self._vy))
		self._arr = tmp

	def drawWeapon(self, obj):
		dim = self._disp.shape
		for i in self._arr:
			for j in range(dim[0]):
				for k in range(dim[1]):
					if self._disp[j][k] != ' ':
						obj['grid'].setBoardXY(i[0] + j, i[1] + k, self._col + self._disp[j][k])

	def render(self, obj):
		dim = self._disp.shape
		for i in self._arr:
			for j in range(dim[0]):
				for k in range(dim[1]):
					if self._disp[j][k] != ' ':
						obj['grid'].setBoardXY(i[0] + j, i[1] + k, Back.BLACK + Fore.BLACK + ' ')
		

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
						obj['grid'].setBoardXY(i + x, j + y, self._col + self._disp[i][j])
