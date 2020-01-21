import numpy as np
import random
import colorama
from colorama import Back, Fore, Style
import time

class IceBall:
	def __init__(self):
		self._disp = np.array([[':', ':', ':'], [':', ':', ':'], [':', ':', ':']])
		self._col = Back.BLACK + Fore.WHITE
		self._shootTime = 0.25
		self._lastTime = 0
		self._vy = 4
		self._arr = set()

	def objCol(self, x, y, obj):
		isCol = 0
		isCol |= y < obj['grid'].get_dim()[1][0]
		isCol |= x + self._disp.shape[0] > obj['grid'].get_dim()[0][1]
		if not isCol:
			obj['beam'].checkCol(x, y, self._disp, obj)
			obj['magnet'].checkCol(x, y, self._disp, obj)
			obj['coin'].checkCol(x, y, self._disp, obj) > 0
			isCol |= obj['bullet'].checkCol(x, y, self._disp, obj)
			isCol |= obj['barry'].checkCol(x, y, self._disp, obj)
		return isCol

	def set_XY(self, obj):
		tmp = set()
		for i in self._arr:
			br = 0
			for j in range(self._vy + 1):
				if self.objCol(i[0], i[1] - j, obj):
					br = 1
					break
			if not br:
				tmp.add((i[0], i[1] - self._vy))
		self._arr = tmp

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

	def render(self, obj):
		dim = self._disp.shape
		for i in self._arr:
			for j in range(dim[0]):
				for k in range(dim[1]):
					if self._disp[j][k] != ' ':
						obj['grid'].set_XY(i[0] + j, i[1] + k, obj['grid'].get_col() + ' ')
	
	def drawWeapon(self, obj):
		dim = self._disp.shape
		for i in self._arr:
			for j in range(dim[0]):
				for k in range(dim[1]):
					if self._disp[j][k] != ' ':
						obj['grid'].set_XY(i[0] + j, i[1] + k, self._col + self._disp[j][k])

	def makeWeapon(self, x, y, obj):
		if self._lastTime:
			if int(round(time.time())) - self._lastTime > self._shootTime:
				self._lastTime = 0
			return
		else:
			self._lastTime = int(round(time.time()))
		x = obj['barry'].get_XY()[0]
		if x + self._disp.shape[0] > obj['grid'].get_dim()[0][1]:
			x = obj['grid'].get_dim()[0][1] - self._disp.shape[0]
		elif x < obj['grid'].get_dim()[0][0]:
			x = obj['grid'].get_dim()[0][0]
		if not self.objCol(x, y, obj):
			if (x, y) in self._arr:
				return
			self._arr.add((x, y))
			for i in range(self._disp.shape[0]):
				for j in range(self._disp.shape[1]):
					if self._disp[i][j] != ' ':
						obj['grid'].set_XY(i + x, j + y, self._col + self._disp[i][j])
