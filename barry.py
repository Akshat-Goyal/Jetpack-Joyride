from person import Person
import numpy as np
import math

class Barry(Person):
	def __init__(self, gridDim):
		self._disp = np.array([['o', '-', 'o'], ['-', '|', '-'], ['/', ' ', '\\']])
		self._x = gridDim[0][1] - self._disp.shape[0]
		self._y = gridDim[1][0]
		self._maxLive = 10
		self._lives = 10
		Person.__init__(self, self._x, self._y, self._disp, self._maxLive)
		self._score = 0
		self._jumpCount = 0
		self._gravity = 0.25
		self._maxShield = 10
		self._curShield = 10
		self._powerUpTime = 60
		self._shieldActivated = 0


	def activateShield(self):
		if not self._shieldActivated and self._curShield == self._maxShield:
			self._shieldActivated = 1

	def checkShield(self):
		if self._shieldActivated:
			self._curShield -= 1
			if not self._curShield:
				self._shieldActivated = 0
				self._curShield -= self._powerUpTime
		elif self._curShield < 0:
			self._curShield += 1
			if not self._curShield:
				self._curShield = self._maxShield 

	def getShieldPower(self):
		if self._curShield > 0:
			return int(self._curShield * 100 / self._maxShield)
		else:
			return 0

	def getScore(self):
		return self._score

	def addScore(self, x):
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
					self._lives -= 1
					if not self._lives:
						obj['grid'].gameOver()
					return True
		return False

	def objCol(self, obj):
		self._score += obj['coin'].checkCol(self._x, self._y, self._disp, obj)
		obj['speedBoost'].checkCol(self._x, self._y, self._disp, obj, True)
		isCol = obj['beam'].checkCol(self._x, self._y, self._disp, obj)
		if isCol and not self._shieldActivated:
			self._lives -= 1
		if not self._lives:
			obj['grid'].gameOver()

	def move(self, y, obj):
		dim = self._disp.shape
		if y:	
			left = int(y / abs(y))
			gridDim = obj['grid'].getDim()
			while y:
				if self._y + left + dim[1] > gridDim[1][1]:
					self._y = gridDim[1][1] - dim[1]
				elif self._y + left < gridDim[1][0]:
					self._y = gridDim[1][0]
				else:
					self._y += left
				self.objCol(obj)
				y = (abs(y) - 1) * left
		self.objCol(obj)

	def jump(self, x, obj):
		if x < 0:
			self._jumpCount = 0
		dim = self._disp.shape
		up = x
		if x: 
			up = int(up / abs(x)) 
		while x:
			gridDim = obj['grid'].getDim()
			if self._x + up + dim[0] > gridDim[0][1]:
				self._x = gridDim[0][1] - dim[0]
			elif self._x + up < gridDim[0][0]:
				self._x = gridDim[0][0]
			else:
				self._x += up
			x = (abs(x) - 1) * up
			self.move(0, obj)

	def onGround(self, obj):
		return self._x + self._disp.shape[0] == obj['grid'].getDim()[0][1]

	def gravity(self, obj):
		if self.onGround(obj):
			return
		self._jumpCount += 1
		self.jump(math.floor(self._gravity * self._jumpCount), obj)
