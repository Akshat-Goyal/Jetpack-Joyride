import numpy as np
from person import Person
import colorama
from colorama import Fore, Style, Back

class BossEnemy(Person):
	def __init__(self, gridDim):
		self._disp = np.array([['B', 'B'], ['O', 'O'], ['S', 'S'], ['S', 'S']])
		self._x = None
		self._y = gridDim[1][1] - self._disp.shape[1]
		self._maxLive = 10
		self._lives = 10
		Person.__init__(self, self._x, self._y, self._disp, self._maxLive, Fore.MAGENTA + Back.BLACK)
		self._isReady = 0

	def isBossReady(self):
		return self._isReady		

	def checkCol(self, x, y, disp, obj, On):
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
					if On:
						self._lives -= 1
					if not self._lives:
						obj['grid'].gameOver()
					return True

	def checkBoss(self, obj):
		self._isReady = 1
		bXY = obj['barry'].getXY()
		x = self._x
		if bXY[0] + self._disp.shape[0] > obj['grid'].getDim()[0][1]:
			self._x = obj['grid'].getDim()[0][1] - self._disp.shape[0]
		else:
			self._x = bXY[0]
		if x == self._x:
			return

		obj['iceBall'].makeWeapon(self._x + int((self._disp.shape[0] - 1) / 2), self._y + self._disp.shape[1], obj)
		obj['beam'].checkCol(self._x, self._y, self._disp, obj)
		obj['coin'].checkCol(self._x, self._y, self._disp, obj)
		obj['magnet'].checkCol(self._x, self._y, self._disp, obj)
		if self.checkCol(bXY[0], bXY[1], obj['barry'].getDisp(), obj, False):
			obj['barry'].setXY(obj['grid'].getDim()[0][1] - obj['barry'].getDisp().shape[0], obj['grid'].getDim()[1][0])
			obj['barry'].lossLive(obj)
	