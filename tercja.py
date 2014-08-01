__author__ = "Xevaquor"

from math import *
import numpy as np
import matplotlib.pyplot as plt


class Tercja:
	def __init__(self, start, stop):
		self.magic = 33.  # this magic number is quite arbitrary. I am not a musician so
		# I mostly do not ever understand what I am coding :D
		self.start = start
		self.stop = stop
		self.minimum_y = 1  # because x^0 = 1
		self.maximum_y = self.compute(33)


	def compute(self, x):
		return (pow(2, (1. / 3))) ** x

	def get_value(self, xx):
		value = self.compute(xx / (self.stop[0] - self.start[0]) * self.magic)
		relative = value / (self.maximum_y - self.minimum_y)
		return (self.stop[1] - self.start[1]) * relative + self.start[1]



def narf(x):
	return (pow(2, (1. / 3))) ** x

def normalized_narf(x1, x2, x):
	diff = x2 - x1
	normalized = x * 1.0 / diff
	newx = normalized * 33
	buff = narf(newx)
	return buff


minima = 0
maxima = 1000

max_value_plot = maxima
steps = 1000
a = (minima, 1000)
b = (maxima, 10000)

xd = Tercja(a,b)

xd.stop = (maxima, xd.compute(33))
x = np.linspace(minima, max_value_plot, steps)
y = []
for i in x:
	y.append(normalized_narf(minima, maxima, i))
z = []
for i in x:
	z.append(xd.get_value(i))

plt.ylim([0, max([max(y), max(z)]) * 1.07])
plt.plot(x, y)
plt.plot(x, z, 'r')
plt.show()