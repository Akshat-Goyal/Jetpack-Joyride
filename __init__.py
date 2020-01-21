from input import input_to, Get
from board import Board
from barry import Barry
from coin import Coin
from magnet import Magnet
from speedBoost import SpeedBoost
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
	grid = Board(40, 120, 1)
	barry = Barry(grid.getDim())
	speedBoost = SpeedBoost()
	coin = Coin()
	beam = FireBeam()
	magnet = Magnet()
	bullet = Bullet()
	iceBall = IceBall()
	boss = BossEnemy(grid.getDim())
	obj = {'grid': grid, 'barry': barry, 'coin': coin, 'beam': beam, 'magnet': magnet, 'speedBoost': speedBoost, 'bullet': bullet, 'iceBall': iceBall, 'boss': boss}

	coin.drawCoin(obj, 0)
	beam.drawObstacle(obj, 0)
	speedBoost.drawBoost(obj, 0)
	magnet.makeMagnet(obj, 0)
	barry.drawPerson(obj)

	grid.printBoard()
	print("Score: " + str(barry.getScore()))
	print("Live: " + str(barry.getLive()))
	print("Shield Power:" + str(barry.getShieldPower()) + "  ")

	current_milli_time = lambda: int(round(time.time() * 1000))
	prev_time = current_milli_time()
	milis_per_frame = 60
	getch = Get()

	while(True):
		isBossReady = 0
		if current_milli_time() - prev_time > milis_per_frame:
			isBossReady |= grid.shift(obj)
			isBossReady |= grid.shift(obj)
			if speedBoost.isBoostOn():
				isBossReady |= grid.shift(obj)
				isBossReady |= grid.shift(obj)
			prev_time = current_milli_time()

		ch = input_to(getch)
		barry.render(obj)
		bullet.render(obj)
		if isBossReady:
			boss.render(obj)
		iceBall.render(obj)
		bullet.changeY(2, obj)
		barry.checkShield()
		iceBall.changeY(obj)
		magnet.checkMagnet(obj)
		speedBoost.checkBoostTime()

		if ch != 'w' or ch != 'W':
			barry.gravity(obj)
		if ch == ' ':
			barry.activateShield()
		elif ch == 'k' or ch == 'K':
			bullet.makeWeapon(barry.getXY()[0] + int((barry.getDisp().shape[0] - 1) / 2), barry.getXY()[1] + barry.getDisp().shape[1], obj)
		elif ch == 'd' or ch == 'D':
			barry.move(2, obj)
		elif ch == 'a' or ch == 'A':
			barry.move(-2, obj)
		elif ch == 'w' or ch == 'W':
			barry.jump(-2, obj)
		elif ch == 'q' or ch == 'Q':
			break

		if isBossReady:
			boss.checkBoss(obj)
		magnet.drawObstacle(obj)
		bullet.drawWeapon(obj)
		barry.drawPerson(obj)
		if isBossReady:
			iceBall.drawWeapon(obj)
			boss.drawPerson(obj)

		grid.printBoard()
		print("Score: " + str(barry.getScore()))
		print("Live: " + str(barry.getLive()))
		print("Shield Power:" + str(barry.getShieldPower()) + "  ")
		if isBossReady:
			print("Boss Enemy:" + str(boss.getLive()) + " ")