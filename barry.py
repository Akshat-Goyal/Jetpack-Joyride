from person import Person
import numpy as np
import math
import colorama
from colorama import Fore, Style, Back
import time

class Barry(Person):
	def __init__(self, gridDim):
		self._disp = np.array([['o', '-', 'o'], ['-', '|', '-'], ['/', ' ', '\\']])
		Person.__init__(self, gridDim[0][1] - self._disp.shape[0], gridDim[1][0], self._disp, Fore.CYAN + Back.BLACK)
		self.__fig = [self._disp, np.array([['o', '^', 'o'], ['-', '|', '-'], ['|', ' ', '|']])]
		for i in range(1, 3):
			f = open('./dragon' + str(i) + '.txt', 'r')
			tmp1 = []
			for line in f:
				line = line.split('\n')[0]
				tmp2 = []
				for i in line:
					tmp2.append(i)
				tmp1.append(tmp2)
			self.__fig.append(np.array(tmp1))
		self._dispNo = 0
		self.__dragonOn = 0
		self.__livesLeft = 10
		self.__score = 0
		self.__jumpCount = 0
		self.__gravity = 0.25
		self.__shieldStayTime = 10
		self.__lastShieldTime = 0
		self.__shieldPowerUpTime = 60
		self.__shieldOn = 0

	def changeDisp(self, obj):
		if self.__dragonOn:
			if self._dispNo < 2:
				self._dispNo = 2
			else:
				self._dispNo += 1
			if self._dispNo == len(self.__fig):
				self._dispNo = 2
		elif not self.__jumpCount and not self.onGround(obj):
			self._dispNo = 1
		else:
			self._dispNo = 0
		self._disp = self.__fig[self._dispNo]
		if self._x + self._disp.shape[0] > obj['grid'].get_dim()[0][1]:
			self._x =  obj['grid'].get_dim()[0][1] - self._disp.shape[0]
		if self._y + self._disp.shape[1] > obj['grid'].get_dim()[1][1]:
			self._y =  obj['grid'].get_dim()[1][1] - self._disp.shape[1]
		if self.__dragonOn:
			obj['bullet'].makeWeapon(self._x + int((self._disp.shape[0] - 1) / 2), self._y + self._disp.shape[1], obj)


	def get_isDragonOn(self):
		return self.__dragonOn

	def get_isShieldOn(self):
		return self.__shieldOn == 1

	def set_shieldOn(self, obj):
		if not self.__shieldOn and not self.__dragonOn: 
			self.__shieldOn = 1
			self._col = Back.BLACK + Fore.CYAN + Fore.MAGENTA
			self.__lastShieldTime = int(round(time.time()))

	def checkShield(self):
		if self.__shieldOn == 1:
			if int(round(time.time())) - self.__lastShieldTime > self.__shieldStayTime:
				self.__prevShieldTime = int(round(time.time()))
				self.__shieldOn = 2
				self._col = Back.BLACK + Fore.CYAN
		elif self.__shieldOn == 2:
			if int(round(time.time())) - self.__lastShieldTime > self.__shieldPowerUpTime:
				self.__lastShieldTime = 0
				self.__shieldOn = 0

	def get_shieldPower(self):
		if self.__shieldOn == 1:
			return int((self.__shieldStayTime - int(round(time.time())) + self.__lastShieldTime) / self.__shieldStayTime * 100)
		elif self.__shieldOn == 2:
			return 0
		else:
			return 100

	def set_live(self, obj):
		if self.__shieldOn == 1:
			return
		if self.__shieldOn != 1:
			self.__livesLeft -= 1
		if not self.__livesLeft:
			obj['grid'].gameOver(obj)

	def get_live(self):
		return self.__livesLeft

	def get_score(self):
		return self.__score

	def set_score(self, x):
		self.__score += x

	def checkCol(self, x, y, disp, obj):
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
					if self.__shieldOn != 1:
						self.__livesLeft -= 1
					if not self.__livesLeft:
						obj['grid'].gameOver(obj)
					return True
		return False

	def objCol(self, obj):
		isCol = 0
		self.__score += obj['coin'].checkCol(self._x, self._y, self._disp, obj)
		obj['speedBoost'].checkCol(self._x, self._y, self._disp, obj)
		self.__dragonOn |= obj['dragonBoost'].checkCol(self._x, self._y, self._disp, obj)
		isCol |= obj['boss'].checkCol(self._x, self._y, self._disp, obj)
		if isCol:
			self._x = obj['grid'].get_dim()[0][1] - self._disp().shape[0]
			self._y = obj['grid'].get_dim()[1][0]
		isCol |= obj['beam'].checkCol(self._x, self._y, self._disp, obj)
		isCol |= obj['iceBall'].checkCol(self._x, self._y, self._disp, obj)
		obj['bullet'].checkCol(self._x, self._y, self._disp, obj)
		if isCol and self.__shieldOn != 1 and not self.__dragonOn:
			self.__livesLeft -= 1
		if not self.__livesLeft:
			obj['grid'].gameOver(obj)
		return isCol

	def move(self, y, obj):
		if self.__dragonOn:
			self.__dragonOn += 1
		dim = self._disp.shape
		if self.objCol(obj) and self.__dragonOn > 20:
			self.__dragonOn = 0
		if y:	
			left = int(y / abs(y))
			gridDim = obj['grid'].get_dim()
			while y:
				if self._y + left + dim[1] > gridDim[1][1]:
					self._y = gridDim[1][1] - dim[1]
				elif self._y + left < gridDim[1][0]:
					self._y = gridDim[1][0]
				else:
					self._y += left
				if self.objCol(obj) and self.__dragonOn > 20:
					self.__dragonOn = 0
				y = (abs(y) - 1) * left

	def jump(self, x, obj):
		if x < 0:
			self.__jumpCount = 0
		dim = self._disp.shape
		up = x
		if x: 
			up = int(up / abs(x)) 
			gridDim = obj['grid'].get_dim()
		while x:
			if self._x + up + dim[0] > gridDim[0][1]:
				self._x = gridDim[0][1] - dim[0]
			elif self._x + up < gridDim[0][0]:
				self._x = gridDim[0][0]
			else:
				self._x += up
			x = (abs(x) - 1) * up
			self.move(0, obj)

	def onGround(self, obj):
		return self._x + self._disp.shape[0] == obj['grid'].get_dim()[0][1]

	def gravity(self, obj):
		if self.onGround(obj):
			return
		self.__jumpCount += 1
		self.jump(math.floor(self.__gravity * self.__jumpCount), obj)
