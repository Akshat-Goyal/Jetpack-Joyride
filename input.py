"""Defining input class."""
import sys
import termios
import tty
import signal
import time


class Tick:
	def __init__(self):
		self.__tick2_frame = 0
		self.__tick2_fps = 20000000   # real raw FPS
		self.__tick2_t0 = time.time()

	def tick(self, fps = 60):
		n = self.__tick2_fps/fps
		self.__tick2_frame += 1
		while n > 0: n -= 1
		if time.time() - self.__tick2_t0 > 1:
		    self.__tick2_t0 = time.time()
		    self.__tick2_fps = self.__tick2_frame
		    self.__tick2_frame = 0


class Get:
	"""Class to get input."""

	def __call__(self):
		"""Defining __call__."""
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch


class AlarmException(Exception):
	"""Handling alarm exception."""
	pass


def alarmHandler(signum, frame):
	"""Handling timeouts."""
	raise AlarmException


def input_to(getch, timeout=0.1):
	"""Taking input from user."""
	signal.signal(signal.SIGALRM, alarmHandler)
	signal.setitimer(signal.ITIMER_REAL, timeout)
	try:
		text = getch()
		signal.alarm(0)
		return text
	except AlarmException:
		signal.signal(signal.SIGALRM, signal.SIG_IGN)
		return None