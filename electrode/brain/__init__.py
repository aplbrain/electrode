#!/usr/bin/env python3
"""
Brain module.

The master file for the simulator.
"""

from typing import Tuple
import networkx as nx
import numpy as np

from .. import timing
from ..neuron import Neuron
from ..synapse import Synapse


class Electrode:
    def __init__(self, compartment):
        self.compartment = compartment

    def record(self):
        return self.compartment["mV"]

    def stim(self, current: float = 0):
        self.compartment["mV"] = current


class Brain:
    """
    Brains handle simulator-pools.

    More details inline.
    """

    def __init__(self, **kwargs):
        """
        Create a new Brain object to control neurons.

        Arguments:
            time_resolution (int : 500): Number of ns between "frames"

        """
        # Set defaults.
        # Time resolution is 0.5 millis
        self.time_resolution = kwargs.get("time_resolution", timing.ms(0.5))
        self._graph = nx.DiGraph()
        self.loaded = False
        self._neurons = []  # type: List[Neuron]
        self._synapses = []  # type: List[Synapse]

    def __getitem__(self, key):
        """
        Get a neuron or segment data.

        Arguments:
            key (str[2]): The index to look up in the network

        Returns:
            Segment

        """
        if len(key) is 2:
            return self._graph.nodes["{}/{}".format(*key)]
        return self._graph.nodes[key]

    def get_graph(self) -> nx.Graph:
        """
        Get the underlying networkx graph when compiled.

        Arguments:
            None

        Returns:
            networkx.Graph: The underlying compiled graph

        """
        if self.loaded:
            return self._graph

        raise RuntimeError(
            "Cannot retrieve a graph until you have called Brain#compile."
        )

    def compile(self, reduce: bool = True):
        """
        Simplify the graph and load it into the networkx graph.

        Arguments:
            reduce (bool : True): Whether to attempt to reduce degree=2 edges
                to a simplified, more optimized graph.

        Returns:
            None

        """
        self.loaded = True
        self._graph = nx.DiGraph()
        if reduce:
            self._graph = nx.compose_all([neuron.reduce() for neuron in self._neurons])

            for synapse in self._synapses:
                self._graph.add_edge(
                    "/".join(synapse[0]),
                    "/".join(synapse[1]),
                    **{"synapse": synapse[2]}
                )

    def step(self) -> bool:
        """
        Begin running the simulation.

        Return True on every step, unless an error is encountered.

        Arguments:
            None

        Returns:
            bool: True when successful, False otherwise.

        """
        _EPSILON = 2.0  # mV

        for node_id, attrs in self._graph.nodes(data=True):
            attrs["mV"] = ((attrs["mV"] - attrs["resting"]) * 0.62) + attrs["resting"]

            if attrs["mV"] >= attrs["threshold"]:
                attrs["mV"] = attrs["fire_potential"]

        for node_id, attrs in self._graph.nodes(data=True):
            # For each neighbor of node:
            #       If the edge is continuous, "equalize" mV
            #       If the edge is a synapse, "fire" if the mV is high enough
            for (seg0, seg1, link) in self._graph.edges([node_id], data=True):
                if "synapse" in link:
                    if self[seg0]["mV"] >= self[seg0]["fire_potential"] - _EPSILON:
                        self[seg1]["mV"] = min(
                            link["synapse"].postsynaptic_weight
                            * (self.time_resolution),
                            self[seg1]["threshold"],
                        )
                else:
                    raise NotImplementedError("Cannot support multicompartment yet.")
            if attrs["mV"] >= attrs["fire_potential"]:
                attrs["mV"] = attrs["resting"] - _EPSILON
        return True

    def add_neuron(self, neuron):
        """
        Add a new neuron to the network. Adds resultant connections.

        Cannot be run after a call to .compile().

        Arguments:
            neuron (electrode.Neuron): The neuron to add.

        Returns:
            None

        """
        if not isinstance(neuron, Neuron):
            raise TypeError("Neuron must implement electrode.neuron.Neuron.")
        if self.loaded:
            raise RuntimeError(
                "You cannot call `add_neuron` after a call to `compile`."
            )
        self._neurons.append(neuron)

    def add_electrode(self, location) -> Electrode:
        return Electrode(self[location])

    def add_synapse(
        self, synapse: Synapse, source: Tuple[str, str], sink: Tuple[str, str]
    ):
        """
        Add a new synapse to the network.

        Arguments:
            synapse (electrode.Synapse): The synapse to add
            source (str[2]): The presynaptic segment
            sink (str[2]): The postsynaptic segment

        Returns:
            None

        """
        self._synapses.append((source, sink, synapse))
