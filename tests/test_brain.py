#!/usr/bin/env python3
"""
Copyright 2017 The Johns Hopkins University Applied Physics Laboratory.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest

from electrode.brain import Brain
from electrode.synapse import SimpleSynapse
from electrode.neuron import HodgkinHuxleyNeuron


class TestBrain(unittest.TestCase):
    """
    Global tests for brain simulator.

    .
    """

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

    def test_get_segment_from_brain(self):
        """
        Test that you can get a segment by indexing.

        .
        """
        brain = Brain()
        brain.add_neuron(HodgkinHuxleyNeuron(name="1"))
        brain.add_neuron(HodgkinHuxleyNeuron(name="2"))
        brain.compile()
        self.assertEqual(type(brain["1", "soma"]), dict)

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
                    SimpleSynapse(1.),
                    (str(i), "soma"),
                    (str(j), "soma")
                )
        brain.compile()

        self.assertEqual(len(brain.get_graph().nodes()), 10)
        self.assertEqual(len(brain.get_graph().edges()), 55)

    def test_mV_decay(self):
        """
        Test that membrane potential goes down over time.

        .
        """
        brain = Brain()
        brain.add_neuron(HodgkinHuxleyNeuron(name="1"))
        brain.add_neuron(HodgkinHuxleyNeuron(name="2"))
        brain.add_synapse(
            SimpleSynapse(1.),
            ("1", "soma"),
            ("2", "soma")
        )
        brain.compile()

        brain['1', 'soma']['mV'] = -20
        self.assertEqual(brain["1", "soma"]['mV'], -20)
        brain.step()
        self.assertNotEqual(brain["1", "soma"]['mV'], -20)
