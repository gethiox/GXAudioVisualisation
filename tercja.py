#!/usr/bin/env python
# coding=utf-8
__author__ = "Xevaquor"

from math import pow, log

#import numpy as np
#import matplotlib.pyplot as plt


class Tercja:
    def __init__(self, start, stop):
        """

        :param start: left value of x
        :param stop: right value of x
        """
        self.base = pow(2, (1. / 3))
        self.minimum_x = start
        self.maximum_x = stop

    def compute(self, xarg):
        """
        Computes value of tercja function ignoring set bounds
        :param xarg: x argument for func
        :return: computed y value
        """
        return self.base ** xarg

    def compute_inverse(self, yarg):
        """
        Computes inverse of tercja
        :param yarg: y argument for func
        :return: corresponding x value
        """
        #nonpositive numbers are out of domain of log func
        #we are silently ignoring it
        if yarg <= 0:
            return 0
        return log(yarg, self.base)

    def get_value_from_x(self, xx):
        """
        Computes value from percentage in interval. For more details please see:
        https://github.com/Xevaquor/GXAudioVisualisation/wiki/Tercja
        :param xx: Percent in interval. Must be in range [0,1]
        Eg: .42 means 42%
        :return: corresponding value of Tercja func
        """
        assert (0 <= xx <= 1)
        return self.compute(xx * (self.maximum_x - self.minimum_x) + self.minimum_x)


if __name__ == "__main__":
    print("For usage info please visit: https://github.com/Xevaquor/GXAudioVisualisation/wiki/Tercja")

    # uncomment following for graph

    # steps = 500
    # a = 7
    # b = 15
    #
    # xd = Tercja(a, b)
    #
    # assert xd.get_value_from_x(.0 == xd.compute(a))
    # assert xd.get_value_from_x(1. == xd.compute(b))
    # assert xd.get_value_from_x(0.5 == xd.compute((a+b)/2.))
    #
    #
    # x = np.linspace(a, b, steps, True)
    # y = xd.compute(x)
    # z = [xd.compute_inverse(i) for i in y]
    #
    # for i, v in enumerate(range(0, 34)):
    #     print(str(i) + ":" + str(xd.compute(i)))
    #
    # plt.plot(x, y, lw=3.7, c='orange')
    # plt.plot(y, z, lw=3.7, c='purple')
    # plt.plot(np.linspace(0, max(y)), np.linspace(0, max(y)), '--k')
    # plt.legend(["Tercja", "Inverse of Tercja"])
    #
    # plt.show()
