from input import input_to, Get
from board import Board
from barry import Barry
from coin import Coin
from magnet import Magnet
from boost import SpeedBoost
from fireBeams import FireBeam
from bullet import Bullet
import os
import time

if __name__ == "__main__":
	os.system('clear')
	grid = Board(40, 60, 5)
	barry = Barry(grid.getDim(), 2, 10, 60)
	boost = SpeedBoost(10)
	coin = Coin()
	beam = FireBeam()
	magnet = Magnet()
	bullet = Bullet()
	obj = {'grid': grid, 'barry': barry, 'coin': coin, 'beam': beam, 'magnet': magnet, 'boost': boost, 'bullet': bullet}
	coin.drawCoin(obj, 0)
	beam.drawFireBeams(obj, 0)
	boost.drawBoost(obj, 0)
	magnet.makeMagnet(obj, 0)
	barry.drawPerson(obj)
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
			grid.shift(obj)
			if boost.isBoostOn():
				grid.shift(obj)
			prev_time = current_milli_time()

		ch = input_to(getch)
		barry.render(obj)
		bullet.render(obj)
		bullet.changeY(1, obj)
		barry.checkShield()
		magnet.checkMagnet(obj)
		boost.checkBoostT()
		if ch != 'w' or ch != 'W':
			barry.gravity(obj)
		if ch == ' ':
			barry.activateShield()
		elif ch == 'k' or ch == 'K':
			bullet.makeBullet(barry.getXY()[0] + int((barry.getDisp().shape[0] - 1) / 2), barry.getXY()[1] + 1, obj)
		elif ch == 'd' or ch == 'D':
			barry.move(2, obj)
		elif ch == 'a' or ch == 'A':
			barry.move(-2, obj)
		elif ch == 'w' or ch == 'W':
			barry.jump(-2, obj)
		elif ch == 'q' or ch == 'Q':
			break
		magnet.drawMagnet(obj)
		bullet.drawBullet(obj)
		barry.drawPerson(obj)
		grid.printBoard()
		print("Score: " + str(barry.getScore()))
		print("Live: " + str(barry.getLive()))
		print("Shield Power:" + str(barry.getShieldPower()) + " ")