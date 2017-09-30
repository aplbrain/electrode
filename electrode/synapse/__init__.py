#!/usr/bin/env python3
"""
Synapse classes (implementations of Synapse).

You can implement Synapse to generate your own simulation type.
"""

from abc import ABCMeta, abstractmethod
import typing


class Synapse:
    """
    The base Synapse class.

    Implement me!

    """

    @abstractmethod
    def __repr__(self) -> str:
        """
        Generate a string representation.

        Should be enough to repro a neuron in simple cases.
        """
        pass


class SimpleSynapse(Synapse):
    """
    Hodgkin-Huxley point-model neuron.

    References:
        - [https://en.wikipedia.org/wiki/Threshold_potential]
        - [https://en.wikipedia.org/wiki/Hodgkin%E2%80%93Huxley_model]

    """

    def __init__(self, postsynaptic_weight: float) -> None:
        """
        Create a new simple synapse.

        Arguments:
            postsynaptic_weight (float): The mV to induce downstream

        """
        self.postsynaptic_weight = postsynaptic_weight

    def __repr__(self) -> str:
        """
        Generate a string representation.

        Simple enough to repro a neuron in simple cases.
        """
        return (
            "SimpleSynapse(postsynaptic_weight={})".format(
                self.postsynaptic_weight
            )
        )
