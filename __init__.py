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

	coin.makeCoin(obj, 0)
	barry.drawPerson(obj)
	beam.drawObstacle(obj, 0)
	speedBoost.makeBoost(obj, 0)
	magnet.makeMagnet(obj, 0)

	grid.printBoard(obj)

	current_milli_time = lambda: int(round(time.time() * 1000))
	prev_time = current_milli_time()
	milis_per_frame = 60
	getch = Get()

	while(True):
		if int(round(time.time())) - stime > 200:
			grid.gameOver(obj)

		if current_milli_time() - prev_time > milis_per_frame:
			boss.set_ready(grid.shift(obj))
			boss.set_ready(grid.shift(obj))
			if speedBoost.get_isBoostOn():
				boss.set_ready(grid.shift(obj))
				boss.set_ready(grid.shift(obj))
			prev_time = current_milli_time()

		ch = input_to(getch)

		barry.render(obj)
		bullet.render(obj)
		if boss.get_isReady():
			boss.render(obj)
			iceBall.render(obj)

		speedBoost.checkBoostTime()
		barry.checkShield()
		magnet.checkMagnet(obj)
		if boss.get_isReady():
			iceBall.set_XY(obj)
			boss.checkBoss(obj)
		bullet.set_XY(4, obj)

		if ch != 'w' or ch != 'W':
			barry.gravity(obj)
		if ch == ' ':
			barry.set_shieldOn(obj)
		elif ch == 'k' or ch == 'K':
			bullet.makeWeapon(barry.get_XY()[0] + int((barry.get_disp().shape[0] - 1) / 2), barry.get_XY()[1] + barry.get_disp().shape[1], obj)
		elif ch == 'd' or ch == 'D':
			barry.move(2, obj)
		elif ch == 'a' or ch == 'A':
			barry.move(-2, obj)
		elif ch == 'w' or ch == 'W':
			barry.jump(-2, obj)
		elif ch == 'q' or ch == 'Q':
			break
		
		barry.changeDisp(obj)
		barry.move(0, obj)

		coin.drawCoin(obj)
		magnet.drawObstacle(obj)
		speedBoost.drawBoost(obj)
		dragonBoost.drawBoost(obj)
		bullet.drawWeapon(obj)
		barry.drawPerson(obj)
		if boss.get_isReady():
			boss.drawPerson(obj)
			iceBall.drawWeapon(obj)

		grid.printBoard(obj)
