from person import Person
import numpy as np
import math
import colorama
from colorama import Fore, Style, Back
import time

class Dragon:
	def __init__(self, gridDim):
		self.__disp = np.array([['o', '-', 'o'], ['-', '|', '-'], ['/', ' ', '\\']])
		self.__x = gridDim[0][1] - self.__disp.shape[0]
		self.__y = gridDim[1][0]
		self.__maxLive = 10
		self.__lives = 10
		Person.__init__(self, self.__x, self.__y, self.__disp, self.__maxLive, Fore.CYAN + Back.BLACK)
		self.__score = 0
		self.__jumpCount = 0
		self.__gravity = 0.25
		self.__shieldTime = 10
		self.__curShieldTime = 0
		self.__shieldPowerUpTime = 60
		self.__shieldActivated = 0

	def isShieldActivated(self):
		return self.__shieldActivated == 1

	def activateShield(self):
		if not self.__shieldActivated: 
			self.__shieldActivated = 1
			self.__curShieldTime = int(round(time.time()))

	def checkShield(self):
		if self.__shieldActivated == 1:
			if int(round(time.time())) - self.__curShieldTime > self.__shieldTime:
				self.__curShieldTime = int(round(time.time()))
				self.__shieldActivated = 2
		elif self.__shieldActivated == 2:
			if int(round(time.time())) - self.__curShieldTime > self.__shieldPowerUpTime:
				self.__curShieldTime = 0
				self.__shieldActivated = 0

	def getShieldPower(self):
		if self.__shieldActivated == 1:
			return int((self.__shieldTime - int(round(time.time())) + self.__curShieldTime) / self.__shieldTime * 100)
		elif self.__shieldActivated == 2:
			return 0
		else:
			return 100

	def lossLive(self, obj):
		if self.__shieldActivated != 1:
			self.__lives -= 1
		if not self.__lives:
			obj['grid'].gameOver()

	def getScore(self):
		return self.__score

	def addScore(self, x):
		self.__score += x

	def checkCol(self, x, y, disp, obj):
		dim = disp.shape
		i = (self.__x, self.__y)
		if y + dim[1] <= i[1] or i[1] + self.__disp.shape[1] <= y:
			return False
		if x >= i[0] + self.__disp.shape[0] or i[0] >= x + dim[0]:
			return False
		for j in range(self.__disp.shape[0]):
			for k in range(self.__disp.shape[1]):
				if self.__disp[j][k] ==  ' ':
					continue
				if i[0] + j - x < 0 or i[0] + j - x >= dim[0]:
					continue
				if i[1] + k - y < 0 or i[1] + k - y >= dim[1]:
					continue
				if disp[i[0] + j - x][i[1] + k - y] != ' ':
					if self.__shieldActivated != 1:
						self.__lives -= 1
					if not self.__lives:
						obj['grid'].gameOver()
					return True
		return False

	def objCol(self, obj):
		self.__score += obj['coin'].checkCol(self.__x, self.__y, self.__disp, obj)
		obj['speedBoost'].checkCol(self.__x, self.__y, self.__disp, obj, True)
		obj['dragonBoost'].checkCol(self.__x, self.__y, self.__disp, obj, True)
		isCol = obj['beam'].checkCol(self.__x, self.__y, self.__disp, obj)
		if isCol and self.__shieldActivated != 1:
			self.__lives -= 1
		if not self.__lives:
			obj['grid'].gameOver()

	def move(self, y, obj):
		dim = self.__disp.shape
		if y:	
			left = int(y / abs(y))
			gridDim = obj['grid'].getDim()
			while y:
				if self.__y + left + dim[1] > gridDim[1][1]:
					self.__y = gridDim[1][1] - dim[1]
				elif self.__y + left < gridDim[1][0]:
					self.__y = gridDim[1][0]
				else:
					self.__y += left
				self.objCol(obj)
				y = (abs(y) - 1) * left
		self.objCol(obj)

	def jump(self, x, obj):
		if x < 0:
			self.__jumpCount = 0
		dim = self.__disp.shape
		up = x
		if x: 
			up = int(up / abs(x)) 
		while x:
			gridDim = obj['grid'].getDim()
			if self.__x + up + dim[0] > gridDim[0][1]:
				self.__x = gridDim[0][1] - dim[0]
			elif self.__x + up < gridDim[0][0]:
				self.__x = gridDim[0][0]
			else:
				self.__x += up
			x = (abs(x) - 1) * up
			self.move(0, obj)

	def onGround(self, obj):
		return self.__x + self.__disp.shape[0] == obj['grid'].getDim()[0][1]

	def gravity(self, obj):
		if self.onGround(obj):
			return
		self.__jumpCount += 1
		self.jump(math.floor(self.__gravity * self.__jumpCount), obj)
