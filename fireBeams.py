import numpy as np
import random
import colorama
from colorama import Fore, Back, Style

class FireBeam:
	def __init__(self):
		self._disp = [np.array([['_', '_', '_', '_']]), np.array([['|'], ['|'], ['|'], ['|']]), np.array([[' ', ' ', ' ', '/'], [' ', ' ', '/', ' '], [' ', '/', ' ', ' '], ['/', ' ', ' ', ' ']]), np.array([['\\', ' ', ' ', ' '], [' ', '\\', ' ', ' '], [' ', ' ', '\\', ' '], [' ', ' ', ' ', '\\']])]
		self._col = Fore.YELLOW + Back.YELLOW
		self._arr = set()

	def set_XY(self, obj):
		tmp = set()
		for i in self._arr:
			if i[0][1] > obj['grid'].get_dim()[1][0]:
				tmp.add(((i[0][0], i[0][1] - 1), i[1]))
		self._arr = tmp

	def checkCol(self, x, y, disp, obj, On):
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
		if On:
			self.render(ar, obj)
		return len(ar) > 0

	def render(self, ar, obj):
		for i in ar:
			self._arr.remove(i)
			for j in range(self._disp[i[1]].shape[0]):
				for k in range(self._disp[i[1]].shape[1]):
					if self._disp[i[1]][j][k] != ' ':
						obj['grid'].set_XY(j + i[0][0], k + i[0][1], obj['grid'].get_col() + ' ')

	def drawObstacle(self, obj, frameNo):
		count = int(random.random() * 5 + 2)
		gridDim = obj['grid'].get_dim()
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
						if obj['grid'].get_XY(x + j, y + k) != obj['grid'].get_col() + ' ' and obj['grid'].get_XY(x + j, y + k) != obj['coin'].get_disp():
							flag = 1
							break
					if flag:
						break
				if not flag:
					self._arr.add(((x, y + frameNo * gridDim[1][1]), z))
					obj['coin'].checkCol(x, y, self._disp[z], obj)
					for i in range(self._disp[z].shape[0]):
						for j in range(self._disp[z].shape[1]):
							if self._disp[z][i][j] != ' ':
								obj['grid'].set_XY(i + x, j + y + frameNo * gridDim[1][1], self._col + self._disp[z][i][j])
					break
