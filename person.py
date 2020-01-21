import colorama
from colorama import Back, Fore, Style

class Person:
	def __init__(self, x, y, disp, lives, col):
		self._x = x
		self._y = y
		self._disp = disp
		self._col = col

	def drawPerson(self, obj):
		dim = self._disp.shape
		if self._x == None:
			return
		for i in range(dim[0]):
			for j in range(dim[1]):
				if self._disp[i][j] != ' ':
					obj['grid'].set_XY(self._x + i, self._y + j, self._col + self._disp[i][j])

	def render(self, obj):
		dim = self._disp.shape
		if self._x == None:
			return
		for i in range(dim[0]):
			for j in range(dim[1]):
				if self._disp[i][j] != ' ':
					obj['grid'].set_XY(self._x + i, self._y + j, obj['grid'].get_col() + ' ')

	def get_XY(self):
		return [self._x, self._y]

	def set_XY(self, x, y):
		self._x = x
		self._y = y

	def get_disp(self):
		return self._disp