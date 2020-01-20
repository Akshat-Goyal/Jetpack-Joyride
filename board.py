import numpy as np
import sys
import colorama
from colorama import Fore, Back, Style

class Board:
	''' contains the design of board '''

	def __init__(self, length, breadth, frame):
		self._length = length
		self._breadth = breadth
		self._frame = frame
		self._col = Back.BLACK + Fore.BLACK
		self._board = np.zeros((self._length, 2 * self._breadth), dtype = object)
		self._board[:] = self._col + " "
		self._sky = np.array([[Back.BLUE + Fore.BLUE + '#'], [Back.BLUE + Fore.BLUE + '#']])
		self._ground = np.array([[Back.GREEN + Fore.GREEN + 'x'], [Back.GREEN + Fore.GREEN + 'x']])
		self._curCol = 0
		self.createBoundry()

	def createBoundry(self):
		for i in range(0, 2 * self._breadth, self._sky.shape[1]):
			self._board[:min(self._sky.shape[0], self._length), i:min(i+self._sky.shape[1], 2*self._breadth)] = self._sky[:min(self._sky.shape[0], self._length), :min(self._sky.shape[1], 2*self._breadth-i)]

		for i in range(0, 2 * self._breadth, self._ground.shape[1]):
			self._board[max(0, self._length-self._ground.shape[0]):, i:min(i+self._ground.shape[1], 2*self._breadth)] = self._ground[max(0, self._ground.shape[0]-self._length):, :min(self._ground.shape[1], 2*self._breadth-i)]

	def shift(self, obj):
		if not self._frame and not self._curCol:
			return True
		obj['barry'].render(obj)
		obj['bullet'].render(obj)

		if not self._curCol:
			self._frame -= 1
			self._board[self._sky.shape[0]:self._length - self._ground.shape[0], self._breadth:] = self._col + ' '
			obj['coin'].drawCoin(obj, 1)
			obj['beam'].drawObstacle(obj, 1)
			obj['magnet'].makeMagnet(obj, 1)
			if self._frame:				
				obj['speedBoost'].drawBoost(obj, 1)

		obj['beam'].changeY(obj)
		obj['magnet'].changeY(obj)
		obj['speedBoost'].changeY(obj)

		self._curCol += 1
		self._board[:, :2 * self._breadth - self._curCol] = self._board[:, 1:2 * self._breadth - self._curCol + 1]
		self._curCol %= self._breadth

		obj['bullet'].changeY(0, obj)
		obj['barry'].move(0, obj)
		obj['bullet'].drawWeapon(obj)
		obj['barry'].drawPerson(obj)
		return False		
		
	def setBoardXY(self, x, y, ch):
		self._board[x][y] = ch
	
	def getBoardXY(self, x, y):
		return self._board[x][y]

	def getDim(self):
		return [[self._sky.shape[0], self._length - self._ground.shape[0]], [0, self._breadth]]

	def getCol(self):
		return self._col

	def gameOver(self):
		print("Game Over")
		sys.exit(0)

	def printBoard(self):
		print("\033[0;0f", end="")
		st = ''
		for i in range(self._length):
			for j in range(self._breadth):
				st += self._board[i][j]
			st += '\n'
		print(st)
