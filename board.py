import numpy as np
import sys
import os
import colorama
from colorama import Fore, Back, Style
import time

class Board:
	''' contains the design of board '''

	def __init__(self, length, breadth, frame):
		self.__length = length
		self.__breadth = breadth
		self.__frame = frame
		self.__col = Back.BLACK + Fore.BLACK
		self.__board = np.zeros((self.__length, 2 * self.__breadth), dtype = object)
		self.__board[:] = self.__col + " "
		self.__sky = np.array([[Back.BLUE + Fore.BLUE + '#'], [Back.BLUE + Fore.BLUE + '#']])
		self.__ground = np.array([[Back.GREEN + Fore.GREEN + 'x'], [Back.GREEN + Fore.GREEN + 'x']])
		self.__curCol = 0
		self.createBoundry()

	def createBoundry(self):
		for i in range(0, 2 * self.__breadth, self.__sky.shape[1]):
			self.__board[:min(self.__sky.shape[0], self.__length), i:min(i+self.__sky.shape[1], 2*self.__breadth)] = self.__sky[:min(self.__sky.shape[0], self.__length), :min(self.__sky.shape[1], 2*self.__breadth-i)]

		for i in range(0, 2 * self.__breadth, self.__ground.shape[1]):
			self.__board[max(0, self.__length-self.__ground.shape[0]):, i:min(i+self.__ground.shape[1], 2*self.__breadth)] = self.__ground[max(0, self.__ground.shape[0]-self.__length):, :min(self.__ground.shape[1], 2*self.__breadth-i)]

	def shift(self, obj):
		if not self.__frame and not self.__curCol:
			return True
		obj['barry'].render(obj)
		obj['bullet'].render(obj)

		if not self.__curCol:
			self.__frame -= 1
			self.__board[self.__sky.shape[0]:self.__length - self.__ground.shape[0], self.__breadth:] = self.__col + ' '
			obj['coin'].makeCoin(obj, 1)
			obj['beam'].drawObstacle(obj, 1)
			obj['magnet'].makeMagnet(obj, 1)
			if self.__frame:				
				obj['dragonBoost'].makeBoost(obj, 1)
				obj['speedBoost'].makeBoost(obj, 1)

		self.__curCol += 1
		self.__board[:, :2 * self.__breadth - self.__curCol] = self.__board[:, 1:2 * self.__breadth - self.__curCol + 1]
		self.__curCol %= self.__breadth

		obj['coin'].set_XY(obj)
		obj['beam'].set_XY(obj)
		obj['magnet'].set_XY(obj)
		obj['speedBoost'].set_XY(obj)
		obj['dragonBoost'].set_XY(obj)

		obj['barry'].checkShield()
		obj['bullet'].set_XY(0, obj)
		obj['barry'].changeDisp(obj)
		obj['barry'].move(0, obj)
		obj['magnet'].checkMagnet(obj)

		obj['coin'].drawCoin(obj)
		obj['magnet'].drawObstacle(obj)
		obj['speedBoost'].drawBoost(obj)
		obj['dragonBoost'].drawBoost(obj)
		obj['bullet'].drawWeapon(obj)
		obj['barry'].drawPerson(obj)
		return False		
		
	def set_XY(self, x, y, ch):
		self.__board[x][y] = ch
	
	def get_XY(self, x, y):
		return self.__board[x][y]

	def get_dim(self):
		return [[self.__sky.shape[0], self.__length - self.__ground.shape[0]], [0, self.__breadth]]

	def get_col(self):
		return self.__col

	def gameOver(self, obj):
		os.system('clear')
		print("\n\n\n")
		print(Back.BLACK + Fore.WHITE + "Time: " + str(int(round(time.time())) - obj['stime']) + "  ", end="")
		print(Back.BLACK + Fore.WHITE + "Score: " + str(obj['barry'].get_score()) + "  ", end="")
		print(Back.BLACK + Fore.WHITE + "Live: " + str(obj['barry'].get_live()) + "  ", end="")
		print(Back.BLACK + Fore.WHITE + "Shield Power: " + str(obj['barry'].get_shieldPower()) + "  ", end="")
		if obj['boss'].get_isReady():
			print(Back.BLACK + Fore.WHITE + "Boss Live: " + str(obj['boss'].get_live()) + "  ", end="")
		print("\n\n\n")
		print(Fore.GREEN + Back.BLACK + "  ________                         ________                     " + "\n",
		Fore.GREEN + Back.BLACK + " /  _____/_____    _____   ____    \_____  \___  __ ___________ " + "\n",
		Fore.GREEN + Back.BLACK + "/   \  ___\__  \  /     \_/ __ \    /   |   \  \/ // __ \_  __ \\" + "\n",
		Fore.GREEN + Back.BLACK + "\    \_\  \/ __ \|  Y Y  \  ___/   /    |    \   /\  ___/|  | \/" + "\n",
		Fore.GREEN + Back.BLACK + " \______  (____  /__|_|  /\___  >  \_______  /\_/  \___  >__|   " + "\n",
		Fore.GREEN + Back.BLACK + "        \/     \/      \/     \/           \/          \/       " + "\n")
		sys.exit(0)

	def gameWon(self, obj):
		os.system('clear')
		print("\n\n\n")
		print(Back.BLACK + Fore.WHITE + "Time: " + str(int(round(time.time())) - obj['stime']) + "  ", end="")
		print(Back.BLACK + Fore.WHITE + "Score: " + str(obj['barry'].get_score()) + "  ", end="")
		print(Back.BLACK + Fore.WHITE + "Live: " + str(obj['barry'].get_live()) + "  ", end="")
		print(Back.BLACK + Fore.WHITE + "Shield Power: " + str(obj['barry'].get_shieldPower()) + "  ", end="")
		if obj['boss'].get_isReady():
			print(Back.BLACK + Fore.WHITE + "Boss Live: " + str(obj['boss'].get_live()) + "  ", end="")
		print("\n\n\n")
		print(Back.BLACK + Fore.GREEN + "  ________                          __      __              " + "\n",
		Back.BLACK + Fore.GREEN + " /  _____/_____    _____   ____    /  \    /  \____   ____  " + "\n",
		Back.BLACK + Fore.GREEN + "/   \  ___\__  \  /     \_/ __ \   \   \/\/   /  _ \ /    \ " + "\n",
		Back.BLACK + Fore.GREEN + "\    \_\  \/ __ \|  Y Y  \  ___/    \        (  <_> )   |  \\" + "\n",
		Back.BLACK + Fore.GREEN + " \______  (____  /__|_|  /\___  >    \__/\  / \____/|___|  /" + "\n",
		Back.BLACK + Fore.GREEN + "        \/     \/      \/     \/          \/             \/ " + "\n")
		sys.exit(0)

	def printBoard(self, obj):
		print("\033[0;0f", end="")
		print(Back.BLACK + Fore.WHITE + "Time: " + str(int(round(time.time())) - obj['stime']) + "  ", end="")
		print(Back.BLACK + Fore.WHITE + "Score: " + str(obj['barry'].get_score()) + "  ", end="")
		print(Back.BLACK + Fore.WHITE + "Live: " + str(obj['barry'].get_live()) + "  ", end="")
		print(Back.BLACK + Fore.WHITE + "Shield Power: " + str(obj['barry'].get_shieldPower()), "  ", end="")
		if obj['boss'].get_isReady():
			print(Back.BLACK + Fore.WHITE + "Boss Live: " + str(obj['boss'].get_live()) + "  ", end="")
		st = Back.BLACK + Fore.BLACK + "\n"
		for i in range(self.__length):
			for j in range(self.__breadth):
				st += self.__board[i][j]
			for j in range(10):
				st += '\033[95m' + " " + '\033[0m'
			st += Back.BLACK + Fore.BLACK + '\n'
		print(st)
