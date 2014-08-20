#!/usr/bin/env python
# coding=utf-8
__author__ = "Xevaquor"

from math import pow, log

# import numpy as np
# import matplotlib.pyplot as plt

base = pow(2, (1. / 3))


def compute(xarg):
	"""
	Computes value of tercja function ignoring set bounds
	:param xarg: x argument for func
	:return: computed y value
	"""
	return base ** xarg


def compute_inverse(yarg):
	"""
	Computes inverse of tercja
	:param yarg: y argument for func
	:return: corresponding x value
	"""
	# non positive numbers are out of domain of log func
	#we are silently ignoring it
	if yarg <= 0:
		return 0
	return log(yarg, base)


def get_value_from_x(xx, minimum_x, maximum_x):
	"""
	Computes value from percentage in interval. For more details please see:
	https://github.com/Xevaquor/GXAudioVisualisation/wiki/Tercja
	Eg: .42 means 42%
	:param xx: Percent in interval. Must be in range [0,1]
	:param minimum_x: Lower x bound
	:param maximum_x: Upper x bound
	:return: corresponding value of Tercja func
	"""
	assert (0 <= xx <= 1)
	return compute(xx * (maximum_x - minimum_x) + minimum_x)


if __name__ == "__main__":
	print("For usage info please visit: https://github.com/Xevaquor/GXAudioVisualisation/wiki/Tercja")

	# uncomment following for plot

	# steps = 500
	# a = 7
	# b = 15
	#
	# assert get_value_from_x(.0 == compute(a), a, b)
	# assert get_value_from_x(1. == compute(b), a, b)
	# assert get_value_from_x(0.5 == compute((a + b) / 2.), a, b)
	#
	# x = np.linspace(a, b, steps, True)
	# y = compute(x)
	# z = [compute_inverse(i) for i in y]
	#
	# for i, v in enumerate(range(0, 34)):
	# 	print(str(i) + ":" + str(compute(i)))
	#
	# plt.plot(x, y, lw=3.7, c='orange')
	# plt.plot(y, z, lw=3.7, c='purple')
	# plt.plot(np.linspace(0, max(y)), np.linspace(0, max(y)), '--k')
	# plt.legend(["Tercja", "Inverse of Tercja"])
	#
	# plt.show()
