#!/usr/bin/env python3

import unittest

from electrode.brain import Brain
from electrode.neuron import HodgkinHuxleyNeuron
from electrode.synapse import SimpleSynapse


class TestBrain(unittest.TestCase):

    def test_no_add_after_load(self):
        """
        Test that you cannot call `add_neuron` after `load`.

        This should throw a runtime exception.
        """
        brain = Brain()
        brain.add_neuron(HodgkinHuxleyNeuron())
        brain.compile()
        with self.assertRaises(RuntimeError):
            brain.add_neuron(HodgkinHuxleyNeuron())

    def test_10x10_brain(self):
        """
        Test that you can create a 10-neuron densely connected brain.

        This should be a pretty simple MVP.
        """
        brain = Brain()
        for i in range(10):
            brain.add_neuron(HodgkinHuxleyNeuron(name=str(i)))

        for i in range(10):
            for j in range(10):
                brain.add_synapse(
                    {},
                    # SimpleSynapse(1),
                    (str(i), "soma"),
                    (str(j), "soma")
                )
        brain.compile()

        self.assertEqual(len(brain._graph.nodes()), 10)
