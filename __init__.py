from input import input_to, Get
from board import Board
from barry import Barry
from coin import Coin
from fireBeams import FireBeam
import os
import time

if __name__ == "__main__":
	os.system('clear')
	grid = Board(40, 60, 5)
	coin = Coin()
	coin.drawCoin(grid, 0)
	barry = Barry(grid, 2)
	beam = FireBeam()
	beam.drawFireBeams(grid, 0)
	barry.drawPerson(grid)
	grid.printBoard()
	print("Score: " + str(barry.getScore()))
	print("Live: " + str(barry.getLive()))
	current_milli_time = lambda: int(round(time.time() * 1000))
	prev_time = current_milli_time()
	milis_per_frame = 60
	getch = Get()

	while(True):
		if current_milli_time() - prev_time > milis_per_frame:
			grid.shift(barry, coin, beam)
			prev_time = current_milli_time()

		ch = input_to(getch)
		barry.render(grid)
		barry.gravity(grid)
		if ch == 'd' or ch == 'D':
			barry.move(1, grid, coin, beam)
		elif ch == 'a' or ch == 'A':
			barry.move(-1, grid, coin, beam)
		elif ch == 'w' or ch == 'W':
			barry.jump()
		elif ch == 'q' or ch == 'Q':
			break
		barry.drawPerson(grid)
		grid.printBoard()
		print("Score: " + str(barry.getScore()))
		print("Live: " + str(barry.getLive()))