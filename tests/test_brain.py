#!/usr/bin/env python3

import unittest

from electrode.brain import Brain
from electrode.neuron import Neuron


class TestBrain(unittest.TestCase):

    def test_no_add_after_load(self):
        """
        Test that you cannot call `add_neuron` after `load`.

        This should throw a runtime exception.
        """
        brain = Brain()
        brain.add_neuron(Neuron())
        brain.compile()
        with self.assertRaises(RuntimeError):
            brain.add_neuron(Neuron())
