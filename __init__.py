from input import input_to, Get
from board import Board
from barry import Barry
import time

if __name__ == "__main__":
	grid = Board()
	barry = Barry(grid.getLength()-4, 4)
	barry.drawPerson(grid)
	grid.printBoard()

	while(True):
		# time.sleep(.05)
		getch = Get()
		ch = input_to(getch)
		barry.render(grid)
		if ch == 'd':
			barry.move(0, 1, grid)
		elif ch == 'a':
			barry.move(0, -1, grid)
		elif ch == 'q':
			break
		barry.drawPerson(grid)
		grid.printBoard()