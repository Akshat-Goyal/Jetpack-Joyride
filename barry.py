from person import Person
import numpy as np
import math
import colorama
from colorama import Fore, Style, Back
import time

class Barry(Person):
	def __init__(self, gridDim):
		self._disp = np.array([['o', '-', 'o'], ['-', '|', '-'], ['/', ' ', '\\']])
		self._fig = [self._disp, np.array([['6']])]
		self._dispNo = 0
		self._dragonOn = 0
		self._x = gridDim[0][1] - self._disp.shape[0]
		self._y = gridDim[1][0]
		self._lives = 10
		Person.__init__(self, self._x, self._y, self._disp, Fore.CYAN + Back.BLACK)
		self._score = 0
		self._jumpCount = 0
		self._gravity = 0.25
		self._shieldStayTime = 10
		self._lastShieldTime = 0
		self._shieldPowerUpTime = 60
		self._shieldOn = 0

	def changeDisp(self, obj):
		if self._dragonOn:
			self._dispNo += 1
			if self._dispNo == len(self._fig):
				self._dispNo = 1
		else:
			self._dispNo = 0
		self._disp = self._fig[self._dispNo]
		if self._x + self._disp.shape[0] > obj['grid'].get_dim()[0][1]:
			self._x =  obj['grid'].get_dim()[0][1] - self._disp.shape[0]
		if self._y + self._disp.shape[1] > obj['grid'].get_dim()[1][1]:
			self._y =  obj['grid'].get_dim()[1][1] - self._disp.shape[1]


	def get_isDragonOn(self):
		return self._dragonOn

	def get_isShieldOn(self):
		return self._shieldOn == 1

	def set_shieldOn(self, obj):
		if not self._shieldOn and not self._dragonOn: 
			self._shieldOn = 1
			self._lastShieldTime = int(round(time.time()))

	def checkShield(self):
		if self._shieldOn == 1:
			if int(round(time.time())) - self._lastShieldTime > self._shieldStayTime:
				self._prevShieldTime = int(round(time.time()))
				self._shieldOn = 2
		elif self._shieldOn == 2:
			if int(round(time.time())) - self._lastShieldTime > self._shieldPowerUpTime:
				self._lastShieldTime = 0
				self._shieldOn = 0

	def get_shieldPower(self):
		if self._shieldOn == 1:
			return int((self._shieldStayTime - int(round(time.time())) + self._lastShieldTime) / self._shieldStayTime * 100)
		elif self._shieldOn == 2:
			return 0
		else:
			return 100

	def set_live(self, obj):
		if self._shieldOn == 1:
			return
		if self._shieldOn != 1:
			self._lives -= 1
		if not self._lives:
			obj['grid'].gameOver()

	def get_live(self):
		return self._lives

	def get_score(self):
		return self._score

	def set_score(self, x):
		self._score += x

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
					if self._shieldOn != 1:
						self._lives -= 1
					if not self._lives:
						obj['grid'].gameOver()
					return True
		return False

	def objCol(self, obj):
		isCol = 0
		self._score += obj['coin'].checkCol(self._x, self._y, self._disp, obj)
		obj['speedBoost'].checkCol(self._x, self._y, self._disp, obj)
		self._dragonOn |= obj['dragonBoost'].checkCol(self._x, self._y, self._disp, obj)
		isCol |= obj['boss'].checkCol(self._x, self._y, self._disp, obj)
		if isCol:
			self._x = obj['grid'].get_dim()[0][1] - self._disp().shape[0]
			self._y = obj['grid'].get_dim()[1][0]
		isCol |= obj['beam'].checkCol(self._x, self._y, self._disp, obj)
		isCol |= obj['iceBall'].checkCol(self._x, self._y, self._disp, obj)
		obj['bullet'].checkCol(self._x, self._y, self._disp, obj)
		if isCol and self._shieldOn != 1 and not self._dragonOn:
			self._lives -= 1
		if not self._lives:
			obj['grid'].gameOver()
		return isCol

	def move(self, y, obj):
		dim = self._disp.shape
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
				if self.objCol(obj):
					self._dragonOn = 0
				y = (abs(y) - 1) * left
		if self.objCol(obj):
			self._dragonOn = 0

	def jump(self, x, obj):
		if x < 0:
			self._jumpCount = 0
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
		self._jumpCount += 1
		self.jump(math.floor(self._gravity * self._jumpCount), obj)
