#!/usr/bin/env python3

import unittest

from electrode.neuron import HodgkinHuxleyNeuron


class TestNeuron(unittest.TestCase):

    def test_str_hh_neuron(self):
        """
        Test that you cannot call `add_neuron` after `load`.

        This should throw a runtime exception.
        """
        nrn = HodgkinHuxleyNeuron(name="test")
        self.assertEqual(
            str(nrn),
            "HodgkinHuxley(name='test', "
            "resting_potential=-75, threshold_potential=-53)",
            36,
        )

    def test_reduce_hh_neuron(self):
        """
        Test that you cannot call `add_neuron` after `load`.

        This should throw a runtime exception.
        """
        nrn = HodgkinHuxleyNeuron(name="test")
        self.assertEqual(
            nrn.reduce().nodes(),
            ["test/soma"]
        )
