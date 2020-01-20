
class Person:
	def __init__(self, x, y, disp, lives):
		self._x = x
		self._y = y
		self._disp = disp
		self._maxLive = lives
		self._lives = lives

	def drawPerson(self, obj):
		dim = self._disp.shape
		for i in range(dim[0]):
			for j in range(dim[1]):
				if self._disp[i][j] != ' ':
					obj['grid'].setBoardXY(self._x + i, self._y + j, self._disp[i][j])

	def render(self, obj):
		dim = self._disp.shape
		for i in range(dim[0]):
			for j in range(dim[1]):
				if self._disp[i][j] != ' ':
					obj['grid'].setBoardXY(self._x + i, self._y + j, ' ')

	def getLive(self):
		return self._lives / self._maxLive * 100

	def getXY(self):
		return [self._x, self._y]

	def setXY(self, x, y):
		self._x = x
		self._y = y

	def getDisp(self):
		return self._disp

	def lossLive(self, obj):
		self._lives -= 1
		if not self._lives:
			obj['grid'].gameOver()