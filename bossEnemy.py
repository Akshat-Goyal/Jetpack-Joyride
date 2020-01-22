import numpy as np
from person import Person
import colorama
from colorama import Fore, Style, Back

class BossEnemy(Person):
	def __init__(self, gridDim):
		f = open('./bossEnemy.txt', 'r')
		self._disp = []
		for line in f:
			line = line.split('\n')[0]
			tmp = []
			for i in line:
				tmp.append(i)
			self._disp.append(tmp)
		self._disp = np.array(self._disp)
		Person.__init__(self, None, gridDim[1][1] - self._disp.shape[1], self._disp, Fore.MAGENTA + Back.BLACK)
		self.__lives = 20
		self.__livesLeft = self.__lives
		self.__isReady = 0

	def get_isReady(self):
		return self.__isReady		

	def set_ready(self, x):
		self.__isReady = x

	def get_live(self):
		return int(self.__livesLeft / self.__lives * 100)

	def checkCol(self, x, y, disp, obj):
		if not self._x:
			return False
		dim = disp.shape
		i = (self._x, self._y)
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
					self.__livesLeft -= 1
					if not self.__livesLeft:
						obj['grid'].gameWon(obj)
					return True
		return False

	def checkBoss(self, obj):
		bXY = obj['barry'].get_XY()
		if bXY[0] + self._disp.shape[0] > obj['grid'].get_dim()[0][1]:
			self._x = obj['grid'].get_dim()[0][1] - self._disp.shape[0]
		else:
			self._x = bXY[0]

		obj['iceBall'].makeWeapon(self._x + int((self._disp.shape[0] - 1) / 2), self._y - 1, obj)
		obj['beam'].checkCol(self._x, self._y, self._disp, obj)
		obj['coin'].checkCol(self._x, self._y, self._disp, obj)
		obj['magnet'].checkCol(self._x, self._y, self._disp, obj)
		if obj['bullet'].checkCol(self._x, self._y, self._disp, obj):
			self.__livesLeft -= 1
		if obj['barry'].checkCol(self._x, self._y, self._disp, obj):
			self.__livesLeft -= 1	
			obj['barry'].set_XY(obj['grid'].get_dim()[0][1] - obj['barry'].get_disp().shape[0], obj['grid'].get_dim()[1][0])
	