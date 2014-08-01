__author__ = "Xevaquor"

from math import *
#import numpy as np
#import matplotlib.pyplot as plt


class Tercja:
	def __init__(self, start, stop):
		"""

		:param start: tuple with starting (left-down) point (x,y)
		:param stop:  tuple with ending (top-right) point (x,y)
		"""
		self.magic = 33.  # this magic number is quite arbitrary. I am not a musician so
		# I mostly do not ever understand what I am coding :D
		self.start = start
		self.stop = stop
		self.minimum_y = 1  # because x^0 = 1
		self.maximum_y = self.compute(self.magic)


	@staticmethod
	def compute(x):
		return (pow(2, (1. / 3))) ** x

	def get_value(self, xx):
		value = self.compute(self.magic * xx / (self.stop[0] - self.start[0]))
		relative = value / (self.maximum_y - self.minimum_y)
		return (self.stop[1] - self.start[1]) * relative + self.start[1]


if __name__ == "__main__":
	# example usage:
	xd = Tercja((0, 0), (100, 100))
	xd = Tercja((0, 0), (100, 100))
	y = xd.get_value(70)

	#uncoment following for graph

	'''steps = 1000
	a = (0, 60)
	b = (100, 100000)

	xd = Tercja(a, b)

	x = np.linspace(a[0], b[0] - 1, steps)
	y = []
	for i in x:
		y.append(xd.get_value(i))

	plt.ylim([0, max(y) * 1.12])
	plt.plot(x, y, lw=4., c='purple')
	plt.show()'''