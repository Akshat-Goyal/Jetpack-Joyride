from person import Person
import numpy as np


class Barry(Person):
	def __init__(self, grid, lives, shieldPower, powerUpTime):
		self._disp = np.array([[' ', '_', ' '], ['{', 'o', '}'], ['/', '_', '\\']])
		gridDim = grid.getDim()
		Person.__init__(self, gridDim[0][1] - self._disp.shape[0], gridDim[1][0], self._disp)
		self._score = 0
		self._maxLive = lives
		self._lives = lives
		self._jumpCount = 0
		self._gravity = 0.25
		self._maxShield = shieldPower
		self._curShield = shieldPower
		self._powerUpTime = powerUpTime
		self._shieldActivated = 0

	def checkCoin(self, grid, coin):
		dim = self._disp.shape
		for i in range(dim[0]):
			for j in range(dim[1]):
				if self._disp[i][j] == ' ':
					continue
				if grid.getBoardXY(i + self._x, j + self._y) == coin.getDisp():
					grid.setBoardXY(i + self._x, j + self._y, ' ')
					self._score += 1

	def move(self, y, grid, coin, beam):
		dim = self._disp.shape
		if not y:
			self.checkCoin(grid, coin)
			if beam.checkCol(self, grid) and not self._shieldActivated:
				self._lives -= 1
			if not self._lives:
				grid.gameOver()
		else:		
			left = int(y / abs(y))
			while y:
				if self._y + left + dim[1] > grid.getDim()[1][1]:
					self._y = grid.getDim()[1][1] - dim[1]
				elif self._y + left < grid.getDim()[1][0]:
					self._y = grid.getDim()[1][0]
				else:
					self._y += left
				self.checkCoin(grid, coin)
				if beam.checkCol(self, grid) and not self._shieldActivated:
					self._lives -= 1
				if not self._lives:
					grid.gameOver()
				y = (abs(y) - 1) * left

	def activateShield(self):
		if not self._shieldActivated and self._curShield == self._maxShield:
			self._shieldActivated = 1

	def isShieldActivated(self):
		return self._shieldActivated

	def getShieldPower(self):
		if self._curShield > 0:
			return int(self._curShield * 100 / self._maxShield)
		else:
			return int((self._powerUpTime + self._curShield) * 100 / self._powerUpTime)

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

	def getXY(self):
		return [self._x, self._y]

	def getDisp(self):
		return self._disp

	def getScore(self):
		return self._score

	def getLive(self):
		return self._lives / self._maxLive * 100

	def jump(self, x, grid, coin, beam):
		if x < 0:
			self._jumpCount = 0
		dim = self._disp.shape
		up = x
		if x: 
			up = int(up / abs(x)) 
		while x:
			if self._x + up + dim[0] > grid.getDim()[0][1]:
				self._x = grid.getDim()[0][1] - dim[0]
			elif self._x + up < grid.getDim()[0][0]:
				self._x = grid.getDim()[0][0]
			else:
				self._x += up
			x = (abs(x) - 1) * up
			self.move(0, grid, coin, beam)

	def onGround(self, grid):
		return self._x + self._disp.shape[0] == grid.getDim()[0][1]

	def gravity(self, grid, coin, beam):
		if self.onGround(grid):
			return
		self._jumpCount += 1
		self.jump(int(self._gravity * self._jumpCount), grid, coin, beam)
