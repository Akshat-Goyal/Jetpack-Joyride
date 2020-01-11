import numpy as np
# import os

class Board:
	''' contains the design of board '''

	def __init__(self):
		self._length = 40
		self._breadth = 60
		self._board = np.zeros((self._length, 4*self._breadth), str)
		self._board[:] = "."
		self._sky = "#"
		self._ground = "x"
		self._wall = "#"

		for i in range(self._breadth):
			self._board[0][i] = self._sky
			self._board[1][i] = self._sky
			self._board[self._length - 2][i] = self._ground
			self._board[self._length - 1][i] = self._ground

		for i in range(self._length):
			self._board[i][0] = self._wall
			self._board[i][1] = self._wall
			self._board[i][self._breadth - 2] = self._wall
			self._board[i][self._breadth - 1] = self._wall

	def change(self, x, y, ch):
		self._board[x][y] = ch

	def getLength(self):
		return self._length

	def getBreadth(self):
		return self._breadth

	def printBoard(self):
		# os.system('clear')
		print("\033[2J")
		st = ''
		for i in range(self._length):
			for j in range(self._breadth):
				st += self._board[i][j] + " "
			st += '\n'
		print(st)
			
