import numpy as np
from coin import Coin
import sys

class Board:
	''' contains the design of board '''

	def __init__(self, length, breadth, frame):
		self._length = length
		self._breadth = breadth
		self._frame = frame
		self._board = np.zeros((self._length, 2 * self._breadth), str)
		self._board[:] = " "
		self._sky = np.array([['#'], ['#']])
		self._ground = np.array([['x'], ['x']])
		self._wall = '#'
		self._curCol = 0
		self.createBoundry()

	def createBoundry(self):
		for i in range(0, 2 * self._breadth, self._sky.shape[1]):
			self._board[:min(self._sky.shape[0], self._length), i:min(i+self._sky.shape[1], 2*self._breadth)] = self._sky[:min(self._sky.shape[0], self._length), :min(self._sky.shape[1], 2*self._breadth-i)]

		for i in range(0, 2 * self._breadth, self._ground.shape[1]):
			self._board[max(0, self._length-self._ground.shape[0]):, i:min(i+self._ground.shape[1], 2*self._breadth)] = self._ground[max(0, self._ground.shape[0]-self._length):, :min(self._ground.shape[1], 2*self._breadth-i)]

	def shift(self, barry, coin, beam, magnet):
		if not self._frame:
			return
		barry.render(self)
		if not self._curCol:
			self._frame -= 1
			if not self._frame:				
				self.fillGrid(beam, magnet, coin, 1)
			else:
				self.fillGrid(beam, magnet, coin, 1)
		beam.changeY()
		magnet.changeY()
		self._curCol += 1
		self._board[:, :2 * self._breadth - self._curCol] = self._board[:, 1:2 * self._breadth - self._curCol + 1]
		self._curCol %= self._breadth
		barry.move(0, self, coin, beam)
		barry.drawPerson(self)

	def fillGrid(self, beam, magnet, coin, frameNo):
		self._board[self._sky.shape[0]:self._length - self._ground.shape[0], frameNo * self._breadth:] = ' '
		coin.drawCoin(self, frameNo)
		beam.drawFireBeams(self, frameNo)
		magnet.makeMagnet(self, frameNo)
		
	def setBoardXY(self, x, y, ch):
		self._board[x][y] = ch
	
	def getBoardXY(self, x, y):
		return self._board[x][y]

	def getDim(self):
		return [[self._sky.shape[0], self._length - self._ground.shape[0]], [0, self._breadth]]

	def gameOver(self):
		print("Game Over")
		sys.exit(0)

	def printBoard(self):
		print("\033[0;0f", end="")
		st = ''
		for i in range(self._length):
			st += self._wall + " " + self._wall + " "
			for j in range(self._breadth):
				st += self._board[i][j] + " "
			st += self._wall + " " + self._wall + '\n'
		print(st)
