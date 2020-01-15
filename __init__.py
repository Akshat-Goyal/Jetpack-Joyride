from input import input_to, Get
from board import Board
from barry import Barry
from coin import Coin
from magnet import Magnet
from fireBeams import FireBeam
import os
import time

if __name__ == "__main__":
	os.system('clear')
	grid = Board(40, 60, 5)
	coin = Coin()
	coin.drawCoin(grid, 0)
	barry = Barry(grid, 2, 10, 60)
	beam = FireBeam()
	magnet = Magnet()
	beam.drawFireBeams(grid, 0)
	barry.drawPerson(grid)
	grid.printBoard()
	print("Score: " + str(barry.getScore()))
	print("Live: " + str(barry.getLive()))
	print("Shield Power:" + str(barry.getShieldPower()) + " ")
	current_milli_time = lambda: int(round(time.time() * 1000))
	prev_time = current_milli_time()
	milis_per_frame = 60
	getch = Get()

	while(True):
		if current_milli_time() - prev_time > milis_per_frame:
			grid.shift(barry, coin, beam, magnet)
			prev_time = current_milli_time()

		ch = input_to(getch)
		barry.checkShield()
		barry.render(grid)
		magnet.checkMagnet(barry, grid, coin, beam)
		if ch == ' ':
			barry.activateShield()
		elif ch == 'd' or ch == 'D':
			barry.move(2, grid, coin, beam)
		elif ch == 'a' or ch == 'A':
			barry.move(-2, grid, coin, beam)
		elif ch == 'w' or ch == 'W':
			barry.jump(-2, grid, coin, beam)
		elif ch == 'q' or ch == 'Q':
			break
		if ch != 'w':
			barry.gravity(grid, coin, beam)
		magnet.drawMagnet(grid)
		barry.drawPerson(grid)
		grid.printBoard()
		print("Score: " + str(barry.getScore()))
		print("Live: " + str(barry.getLive()))
		print("Shield Power:" + str(barry.getShieldPower()) + " ")