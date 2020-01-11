
class Person:

    def __init__(self, x, y, dim, disp):
        self._x = x
        self._y = y
        self._dim = dim
        self._disp = disp

    def drawPerson(self, grid):
        for i in range(self._dim[0]):
            for j in range(self._dim[1]):
                grid.change(self._x + i, self._y + j, self._disp[i][j])

    def render(self, grid):
        for i in range(self._dim[0]):
            for j in range(self._dim[1]):
                grid.change(self._x + i, self._y + j, '.')