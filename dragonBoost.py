import numpy as np
import random
import colorama
from colorama import Back, Fore, Style
import time

class DragonBoost:
	def __init__(self):
		self.__disp = np.array([[' ', '-', ' '], ['|', 'D', '|'], [' ', '-', ' ']])
		self.__col = Back.BLACK + Fore.GREEN
		self.__arr = set()
		self.__count  = 1

	def set_XY(self, obj):
		tmp = set()
		for i in self.__arr:
			if i[1] > obj['grid'].get_dim()[1][0]:
				tmp.add((i[0], i[1] - 1))
		self.__arr = tmp

	# checks the collision of boosts with given obj
	def checkCol(self, x, y, disp, obj):
		ar = []
		dim = disp.shape
		for i in self.__arr:
			if y + dim[1] <= i[1] or i[1] + self.__disp.shape[1] <= y:
				continue
			if x >= i[0] + self.__disp.shape[0] or i[0] >= x + dim[0]:
				continue
			for j in range(self.__disp.shape[0]):
				br = 0
				for k in range(self.__disp.shape[1]):
					if self.__disp[j][k] ==  ' ':
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
		self.render(ar, obj)
		return len(ar) > 0

	# removes the boost from the grid in the ar
	def render(self, ar, obj):
		for i in ar:
			self.__arr.remove(i)
			for j in range(self.__disp.shape[0]):
				for k in range(self.__disp.shape[1]):
					if self.__disp[j][k] != ' ':
						obj['grid'].set_XY(j + i[0], k + i[1], obj['grid'].get_col() +  ' ')

	# draws all the boost on the grid
	def drawBoost(self, obj):
		for i in self.__arr:
			if i[1] >= obj['grid'].get_dim()[1][1]:
				continue
			x = i[0]
			y = i[1]
			for j in range(self.__disp.shape[0]):
				for k in range(self.__disp.shape[1]):
					if self.__disp[j][k] != ' ':
						obj['grid'].set_XY(j + x, k + y, self.__col + self.__disp[j][k])

	# makes a new boost on the grid
	def makeBoost(self, obj, frameNo):
		if not self.__count:
			return
		self.__count -= 1
		count = int(random.random() + 0.95)
		gridDim = obj['grid'].get_dim()
		for _ in range(count):
			while True:
				x = int(random.random() * (gridDim[0][1] - gridDim[0][0] - self.__disp.shape[0]) + gridDim[0][0])
				y = int(random.random() * (gridDim[1][1] - gridDim[1][0] - self.__disp.shape[1]) + gridDim[1][0])
				flag = 0
				for j in range(self.__disp.shape[0]):
					for k in range(self.__disp.shape[1]):
						if self.__disp[j][k] ==  ' ':
							continue
						if obj['grid'].get_XY(x + j, y + k) != obj['grid'].get_col() + ' ' and obj['grid'].get_XY(x + j, y + k) != obj['coin'].get_disp():
							flag = 1
							break
					if flag:
						break
				if not flag:
					self.__arr.add((x, y + frameNo * gridDim[1][1]))
					obj['coin'].checkCol(x, y, self.__disp, obj)
					for i in range(self.__disp.shape[0]):
						for j in range(self.__disp.shape[1]):
							if self.__disp[i][j] != ' ':
								obj['grid'].set_XY(i + x, j + y + frameNo * gridDim[1][1], self.__col + self.__disp[i][j])
					break
