import colorama
from colorama import Back, Fore, Style

class Person:
	def __init__(self, x, y, disp, col):
		self._x = x
		self._y = y
		self._disp = disp
		self._col = col

	# draws person on the grid
	def drawPerson(self, obj):
		if self._x == None:
			return
		dim = self._disp.shape
		for i in range(dim[0]):
			for j in range(dim[1]):
				if self._disp[i][j] != ' ':
					obj['grid'].set_XY(self._x + i, self._y + j, self._col + self._disp[i][j])

	# removes the person from the grid
	def render(self, obj):
		if self._x == None:
			return
		dim = self._disp.shape
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