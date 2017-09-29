#!/usr/bin/env python3
"""
Timing module. Handles time-to-simulation conversions.
"""

NS = 1
MS = 1000 * NS
S = 1000 * MS


def s(num: float) -> int:
    """
    Return `num` many seconds, in steps.

    Arguments:
        num (float): The number of seconds

    Returns:
        int: The number of steps

    """
    return int(S * num)


def ms(num: float) -> int:
    """
    Return `num` many milliseconds, in steps.

    Arguments:
        num (float): The number of milliseconds

    Returns:
        int: The number of steps

    """
    return int(MS * num)


def ns(num: float) -> int:
    """
    Return `num` many nanoseconds, in steps.

    Arguments:
        num (float): The number of nanoseconds

    Returns:
        int: The number of steps

    """
    return int(NS * num)
