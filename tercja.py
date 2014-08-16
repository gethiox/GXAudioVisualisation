__author__ = "Xevaquor"

from math import *
import numpy as np
import matplotlib.pyplot as plt


factor = pow(2, (1. / 3))


class Tercja:
    def __init__(self, start, stop):
        """

		:param start: tuple with starting (left-down) point (x,y)
		:param stop:  tuple with ending (top-right) point (x,y)
		"""
        self.magic = 1.  # this magic number is quite arbitrary. I am not a musician so
        # I mostly do not ever understand what I am coding :D
        self.minimum_x = start
        self.maximum_x = stop
        self.minimum_y = self.compute(start)  # because x^0 = 1
        self.maximum_y = self.compute(self.magic)


    @staticmethod
    def compute(x):
        return (pow(2, (1. / 3))) ** x

    @staticmethod
    def inverted_compute(x):
        if x <= 0:
            return 0
        return log(x, factor)

    def get_value_from_x(self, xx):
        assert (0 <= xx <= 1)
        value = self.compute((self.magic * xx * (self.maximum_x - self.minimum_x)+ self.minimum_x))
        return value

    def get_value_from_y(self, yy):
        assert (0 <= yy <= 1)
        value = self.inverted_compute(self.magic * yy / (self.maximum_y - self.minimum_y) + self.minimum_y)
        return value


if __name__ == "__main__":
    # example usage:
    # xd = Tercja((0, 0), (100, 100))
    # xd = Tercja((0, 0), (100, 100))
    # y = xd.get_value(70)

    # uncoment following for graph

    steps = 5000
    a = 49
    b = 50

    xd = Tercja(a, b)
    dd = Tercja(a, b * 4)

    x = np.linspace(0, 100, steps)
    y = []
    line = []
    y2 = []
    y3 = []
    z = []
    for i in x:
        y.append(xd.compute(i))
        line.append(i)
        y2.append(xd.inverted_compute(i))
        y3.append(dd.compute(i))
    for i in x:
        z.append(xd.get_value_from_x(i/100.))

    print(z)
    # print(line)
    # plt.plot(x, y, lw=4., c='purple')
    # plt.plot(x, y2, lw=4., c='orange')
    # plt.plot(x, y3, lw=1., c='red')
    plt.plot(x,z, lw=2., c='blue')
    plt.plot(x, line, '--k')
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)

    #plt.axis('equal')
    plt.show()