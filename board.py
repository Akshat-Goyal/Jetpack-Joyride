import numpy as np
from coin import Coin

class Board:
	''' contains the design of board '''

	def __init__(self, length, breadth, frame):
		self._length = length
		self._breadth = breadth
		self._frame = frame
		self._board = np.zeros((self._length, 2 * self._breadth), str)
		self._board[:] = "."
		self._sky = np.array(['#'], ['#'])
		self._ground = np.array(['x'], ['x'])
		self._wall = '#'
		self._curCol = 0
		self._coin = None

	def createBoundry(self):
		for i in range(0, self._breadth, self._sky.shape[1]):
			self._board[:min(self._sky.shape[0], self._length), i:min(i+self._sky.shape[1], self._breadth)] = self._sky[:min(self._sky.shape[0], self._length), :min(self._sky.shape[1], self._breadth-i)]

		for i in range(0, self._breadth, self._ground.shape[1]):
			self._board[max(0, self._length-self._ground.shape[0]):, i:min(i+self._ground.shape[1], self._breadth)] = self._ground[max(self._ground.shape[0], self._ground.shape[0]-self._length):, :min(self._ground.shape[1], self._breadth-i)]

	def shift(self, barry):
		if not self._frame:
			return
		barry.render(self)
		barry.move(1, self, self._coin)
		if not self._curCol:
			self._frame -= 1
			if not self._frame:				
				return
			else:
				self.fillGrid()
		self._curCol = (self._curCol + 1) % self._breadth
		self._board[:, :self._breadth] = self._board[:, 1:self._breadth+1]
		barry.drawPerson(self)

	def fillGrid(self):
		pass
		
	def setBoardXY(self, x, y, ch):
		self._board[x][y] = ch
	
	def getBoardXY(self, x, y):
		return self._board[x][y]

	def getDim(self):
		return (self._length, self._breadth)

	def printBoard(self):
		print("\033[0;0f", end="")
		st = ''
		for i in range(self._length):
			st += self._wall + " " + self._wall + " "
			for j in range(self._breadth):
				st += self._board[i][j] + " "
			st += self._wall + " " + self._wall + '\n'
		print(st)
			
