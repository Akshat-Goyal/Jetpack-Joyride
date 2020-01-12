import numpy as np

class Board:
	''' contains the design of board '''

	def __init__(self, length, breadth):
		self._length = length
		self._breadth = breadth
		self._frame = 5
		self._board = np.zeros((self._length, self._frame * self._breadth), str)
		self._board[:] = "."
		self._sky = "#"
		self._ground = "x"
		self._wall = "#"
		self._L = 0
		self._R = self._breadth

		for i in range(self._frame * self._breadth):
			self._board[0][i] = self._sky
			self._board[1][i] = self._sky
			self._board[self._length - 2][i] = self._ground
			self._board[self._length - 1][i] = self._ground

	def shift(self, barry, coin):
		if self._R == self._breadth * self._frame:
			return
		barry.render(self)
		self._L += 1
		self._R += 1
		barry.move(1, self, coin)
		barry.drawPerson(self)

	def change(self, x, y, ch):
		self._board[x][y] = ch
	
	def getBoardXY(self, x, y):
		return self._board[x][y]

	def getFrame(self):
		return self._frame

	def getDim(self):
		return (self._length, self._breadth * self._frame)

	def getGridRange(self):
		return (self._L, self._R)

	def printBoard(self):
		print("\033[0;0f", end="")
		st = ''
		for i in range(self._length):
			st += self._wall + " " + self._wall + " "
			for j in range(self._L, self._R):
				st += self._board[i][j] + " "
			st += self._wall + " " + self._wall + '\n'
		print(st)
			
