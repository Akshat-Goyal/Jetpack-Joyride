from person import Person
import numpy as np
import math

class Barry(Person):
	def __init__(self, gridDim, lives, shieldPower, powerUpTime):
		self._disp = np.array([[' ', '_', ' '], ['{', 'o', '}'], ['/', '_', '\\']])
		Person.__init__(self, gridDim[0][1] - self._disp.shape[0], gridDim[1][0], self._disp)
		self._score = 0
		self._maxLive = lives
		self._lives = lives
		self._jumpCount = 0
		self._gravity = 0.50
		self._maxShield = shieldPower
		self._curShield = shieldPower
		self._powerUpTime = powerUpTime
		self._shieldActivated = 0

	def checkCoin(self, obj):
		dim = self._disp.shape
		for i in range(dim[0]):
			for j in range(dim[1]):
				if self._disp[i][j] == ' ':
					continue
				if obj['grid'].getBoardXY(i + self._x, j + self._y) == obj['coin'].getDisp():
					obj['grid'].setBoardXY(i + self._x, j + self._y, ' ')
					self._score += 1

	def move(self, y, obj):
		dim = self._disp.shape
		if not y:
			self.checkCoin(obj)
			ar = obj['beam'].checkCol(obj['barry'].getXY()[0], obj['barry'].getXY()[1], obj['barry'].getDisp())
			obj['beam'].removeFireBeam(ar, obj)
			if len(ar) and not self._shieldActivated:
				self._lives -= 1
			if not self._lives:
				obj['grid'].gameOver()
		else:		
			left = int(y / abs(y))
			gridDim = obj['grid'].getDim()
			while y:
				if self._y + left + dim[1] > gridDim[1][1]:
					self._y = gridDim[1][1] - dim[1]
				elif self._y + left < gridDim[1][0]:
					self._y = gridDim[1][0]
				else:
					self._y += left
				self.checkCoin(obj)
				ar = obj['beam'].checkCol(obj['barry'].getXY()[0], obj['barry'].getXY()[1], obj['barry'].getDisp())
				obj['beam'].removeFireBeam(ar, obj)
				if len(ar) and not self._shieldActivated:
					self._lives -= 1
				if not self._lives:
					obj['grid'].gameOver()
				y = (abs(y) - 1) * left

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

	def getXY(self):
		return [self._x, self._y]

	def getDisp(self):
		return self._disp

	def getScore(self):
		return self._score

	def getLive(self):
		return self._lives / self._maxLive * 100

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
		self._jumpCount += 0.5
		self.jump(math.floor(self._gravity * self._jumpCount), obj)
