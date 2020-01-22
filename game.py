from input import input_to, Get
from board import Board
from barry import Barry
from coin import Coin
from magnet import Magnet
from speedBoost import SpeedBoost
from dragonBoost import DragonBoost
from bossEnemy import BossEnemy
from fireBeams import FireBeam
from iceBall import IceBall
from bullet import Bullet
import os
import time
import colorama


if __name__ == "__main__":
	colorama.init(autoreset=True)
	os.system('clear')
	# initialize all objects
	grid = Board(40, 120, 12)
	barry = Barry(grid.get_dim())
	coin = Coin()
	beam = FireBeam()
	magnet = Magnet()
	speedBoost = SpeedBoost()
	dragonBoost = DragonBoost()
	bullet = Bullet()
	iceBall = IceBall()
	boss = BossEnemy(grid.get_dim())
	stime = int(round(time.time()))
	obj = {'grid': grid, 'barry': barry, 'coin': coin, 'beam': beam, 'magnet': magnet, 'speedBoost': speedBoost, 'bullet': bullet, 'iceBall': iceBall, 'boss': boss, 'dragonBoost': dragonBoost, 'stime': stime}

	# constructing a frame/grid
	coin.makeCoin(obj, 0)
	barry.drawPerson(obj)
	beam.makeObstacle(obj, 0)
	speedBoost.makeBoost(obj, 0)
	magnet.makeObstacle(obj, 0)

	# prints the grid
	grid.printBoard(obj)

	current_milli_time = lambda: int(round(time.time() * 1000))
	prev_time = current_milli_time()
	milis_per_frame = 60
	# to get character asynchronoulsy
	getch = Get()

	while(True):
		# if time of the game exceeda
		if int(round(time.time())) - stime > 200:
			grid.gameOver(obj)

		# shift the grid to left continuously after some milli sec.
		if current_milli_time() - prev_time > milis_per_frame:
			boss.set_ready(grid.shift(obj))
			boss.set_ready(grid.shift(obj))
			if speedBoost.get_isBoostOn():
				boss.set_ready(grid.shift(obj))
				boss.set_ready(grid.shift(obj))
			prev_time = current_milli_time()

		# get input from the terminal
		ch = input_to(getch)

		# removes objects from the grid
		barry.render(obj)
		bullet.render(obj)
		iceBall.render(obj)
		if boss.get_isReady():
			boss.render(obj)

		# checks collision and moves obj
		speedBoost.checkBoostTime()
		barry.checkShield()
		magnet.checkMagnet(obj)
		iceBall.set_XY(obj)
		if boss.get_isReady():
			boss.checkBoss(obj)
		bullet.set_XY(4, obj)

		# barry is moved
		if ch != 'w' or ch != 'W':
			barry.gravity(obj)
		if ch == ' ':
			barry.set_shieldOn(obj)
		elif ch == 'k' or ch == 'K':
			barry.fire(obj)
		elif ch == 'd' or ch == 'D':
			barry.move(2, obj)
		elif ch == 'a' or ch == 'A':
			barry.move(-2, obj)
		elif ch == 'w' or ch == 'W':
			barry.jump(-2, obj)
		elif ch == 'q' or ch == 'Q':
			break
		
		# barry's display is checked
		barry.changeDisp(obj)
		barry.move(0, obj)

		# objects are drawn on the grid
		coin.drawCoin(obj)
		magnet.drawObstacle(obj)
		beam.drawObstacle(obj)
		speedBoost.drawBoost(obj)
		dragonBoost.drawBoost(obj)
		bullet.drawWeapon(obj)
		barry.drawPerson(obj)
		iceBall.drawWeapon(obj)
		if boss.get_isReady():
			boss.drawPerson(obj)

		# grid printed on the terminal
		grid.printBoard(obj)
