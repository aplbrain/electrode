#!/usr/bin/env python3
"""
Neuron classes (implementations of neuron).

You can implement Neuron to generate your own simulation type.
"""

from abc import ABCMeta, abstractmethod
import typing

import uuid
import networkx as nx


class Neuron:
    """
    The base Neuron class.

    Implement me!

    """

    @abstractmethod
    def frame(self) -> bool:
        """
        Iterate a frame in the neuron space.

        In a simplified network fabric simulation, this is not used.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Generate a string representation.

        Should be enough to repro a neuron in simple cases.
        """
        pass

    @abstractmethod
    def reduce(self) -> nx.Graph:
        """
        Reduce the neuron to a graph representation.

        The simple point-model neurons all reduce to a single node, "soma".

        Arguments:
            None

        Returns:
            networkx.Graph

        """
        pass

    
class HodgkinHuxleyNeuron(Neuron):
    """
    Hodgkin-Huxley point-model neuron.

    References:
        - [https://en.wikipedia.org/wiki/Threshold_potential]
        - [https://en.wikipedia.org/wiki/Hodgkin%E2%80%93Huxley_model]

    """

    def __init__(
        self,
        name: str = None,
        resting_potential: float = -75,
        fire_potential: float = 40,
        threshold_potential: float = -53,
    ) -> None:
        """
        Create a new Hodgkin-Huxley model point-neuron.

        Accepts as arguments:
            resting_potential (int : -75): Resting potential of the cell
            fire_potential (int : -75): AP_max of the cell
            threshold_potential (int : -75): Threshold for activation

        """
        if name:
            self.name = name
        else:
            self.name = str(uuid.uuid4())

        self.resting_potential = resting_potential
        self.fire_potential = fire_potential
        self.threshold_potential = threshold_potential

    def frame(self):
        """
        Iterate a frame in the neuron space.

        In a simplified network fabric simulation, this is not used.
        """
        pass

    def __repr__(self) -> str:
        """
        Generate a string representation.

        Simple enough to repro a neuron in simple cases.
        """
        return (
            "HodgkinHuxley(name='{}', "
            + "resting_potential={}, "
            + "fire_potential={}, "
            + "threshold_potential={})"
        ).format(
            self.name,
            self.resting_potential,
            self.fire_potential,
            self.threshold_potential,
        )

    def reduce(self) -> nx.Graph:
        """
        Reduce the neuron to a graph representation.

        The simple point-model neurons all reduce to a single node, "soma".

        Arguments:
            None

        Returns:
            networkx.Graph

        """
        g = nx.DiGraph()
        g.add_node(
            "{}/soma".format(self.name),
            **{
                "mV": self.resting_potential,
                "resting": self.resting_potential,
                "threshold": self.threshold_potential,
                "fire_potential": self.fire_potential,
            }
        )
        return g


class LeakyIntegratedandFire(Neuron):
    """
    Leaky Integrated and Fire neuron.

    References:
        - [https://en.wikipedia.org/wiki/Threshold_potential]
        - [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5557947/pdf/41598_2017_Article_7418.pdf]


    self.neuron_group.namespace['tau'] = 10*ms #membrane time constant
        self.neuron_group.namespace['vr'] = -40*mV #reset potential
        self.neuron_group.namespace['vth'] = 20*mV #threshold potential
        self.neuron_group.namespace['vh'] = -69.5*mV #holding potential
        self.neuron_group.namespace['Eleak'] = 0*mV
        self.neuron_group.namespace['g_leak'] = 1*usiemens

    eq: dv/dt = -(v-I/g)/tau

    threshold='v > vth'
    refractory='2*ms'
    method='exact'
    reset='v= vr'

    """
    
    def __init__(
            self,
            name: str = None,
            resting_potential: float = -75,
            fire_potential: float = 40,
            threshold_potential: float = -53,
    ) -> None:

        """
        Create a new LIF neuron

        Accepts as arguments:
            resting_potential (int : -75): Resting potential of the cell
            fire_potential (int : -75): AP_max of the cell
            threshold_potential (int : -75): Threshold for activation

        """
        if name:
            self.name = name
        else:
            self.name = str(uuid.uuid4())

        self.resting_potential = resting_potential
        self.fire_potential = fire_potential
        self.threshold_potential = threshold_potential

    
    def Frame():
        """
        Iterate a frame in the neuron space.

        In a simplified network fabric simulation, this is not used.
        """
        pass

    def __repr__(self):
        pass
    
    def reduce(self):
        pass
