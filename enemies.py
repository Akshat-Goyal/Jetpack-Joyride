from person import Person
import numpy as np

class Enemy(Person):
	def __init__(self, x, y):
		self._disp = np.array([['-', 'O', '-'], ['/', 'o', '\\'], [' ', '^', ' ']])
		Person.__init__(self, x, y, self._disp)