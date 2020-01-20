import numpy as np
import random
import colorama
from colorama import Back, Fore, Style

class Magnet:
	def __init__(self):
		self._disp = np.array([[':', ':', ':'], [':', ':', ':']])
		self._col = Back.RED + Fore.RED
		self._arr = set()

	def changeY(self, obj):
		tmp = set()
		for i in self._arr:
			if i[1] > obj['grid'].getDim()[1][0]:
				tmp.add((i[0], i[1] - 1))
		self._arr = tmp

	def checkCol(self, x, y, disp, obj):
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
		self.removeObstacle(ar, obj)
		return len(ar) > 0

	def removeObstacle(self, ar, obj):
		for i in ar:
			self._arr.remove(i)
			for j in range(self._disp.shape[0]):
				for k in range(self._disp.shape[1]):
					if self._disp[j][k] != ' ':
						obj['grid'].setBoardXY(j + i[0], k + i[1], obj['grid'].getCol() + ' ')

	def checkMagnet(self, obj):
		l = 0
		u = 0
		x = obj['barry'].getXY()[0]
		y = obj['barry'].getXY()[1]
		bDim = obj['barry'].getDisp().shape
		for i in self._arr:
			if i[1] >= obj['grid'].getDim()[1][1]:
				continue
			if i[0] < x:
				u -= 1
			if i[0] + self._disp.shape[0] > x + bDim[0]:
				u += 1
			if i[1] < y:
				l -= 1
			if i[1] + self._disp.shape[1] > y + bDim[1]:
				l += 1
		l *= 2
		while l | u:
			if l:
				obj['barry'].move(l / abs(l), obj)
				l = int((abs(l) - 1) * l / abs(l))
			if u:
				obj['barry'].jump(u / abs(u), obj)
				u = int((abs(u) - 1) * u / abs(u))


	def drawObstacle(self, obj):
		for i in self._arr:
			if i[1] >= obj['grid'].getDim()[1][1]:
				continue
			x = i[0]
			y = i[1]
			for j in range(self._disp.shape[0]):
				for k in range(self._disp.shape[1]):
					if self._disp[j][k] != ' ':
						obj['grid'].setBoardXY(j + x, k + y, self._col + self._disp[j][k])

	def makeMagnet(self, obj, frameNo):
		count = int(random.random() + 0.25)
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
						if obj['grid'].getBoardXY(x + j, y + k) != obj['grid'].getCol() + ' ' and obj['grid'].getBoardXY(x + j, y + k) != obj['coin'].getDisp():
							flag = 1
							break
					if flag:
						break
				if not flag:
					self._arr.add((x, y + frameNo * gridDim[1][1]))
					for i in range(self._disp.shape[0]):
						for j in range(self._disp.shape[1]):
							if self._disp[i][j] != ' ':
								obj['grid'].setBoardXY(i + x, j + y + frameNo * gridDim[1][1], self._col + self._disp[i][j])
					break
