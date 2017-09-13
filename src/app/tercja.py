#!/usr/bin/env python

__author__ = "Xevaquor"

from math import pow, log

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
    # we are silently ignoring it
    if yarg <= 0:
        return 0
    return log(yarg, base)


def get_value_from_x(xx, minimum_x, maximum_x):
    """
    Computes value from percentage in interval.
    Eg: .42 means 42%
    :param xx: Percent in interval. Must be in range [0,1]
    :param minimum_x: Lower x bound
    :param maximum_x: Upper x bound
    :return: corresponding value of Tercja func
    """
    assert (0 <= xx <= 1)
    return compute(xx * (maximum_x - minimum_x) + minimum_x)
