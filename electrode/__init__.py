"""
Electrode2
"""

import abc
from typing import Callable, Dict, Hashable

from brian2 import NeuronGroup, SpikeMonitor, Network, StateMonitor, ms, mV, run

import networkx as nx

__version__ = "0.2.0"


class Neuron(abc.ABC):
    """
    A base class for Neuron objects.
    """

    def get_membrane_potential(self):
        ...


class Brian2Neuron(Neuron):
    def __init__(
        self,
        model: str = "dv/dt = -v/(10*ms) : volt",
        threshold: str = "v > -50*mV",
        reset="v = -70*mV",
        refractory: str = "5*ms",
    ) -> None:
        self._fire_callbacks = []
        self._time_step_size_ms = 0.12

        self._group = NeuronGroup(
            1, model, threshold=threshold, reset=reset, refractory=refractory
        )
        self._monitor = StateMonitor(
            self._group, ("v",), record=[0]
        )
        self._net = Network(self._group, self._monitor)

    def add_fire_hook(self, cb: Callable) -> None:
        self._fire_callbacks.append(cb)

    def step(self):
        self._net.run(self._time_step_size_ms * ms)

    def get_membrane_potential(self):
        return 1000*float(self._monitor.v[0][-1])


class LIAFNeuron(Neuron):
    """
    A leaky integrate-and-fire neuron.

    https://files.meetup.com/469457/spiking-neurons.pdf
    """

    def __init__(self):
        self._fire_callbacks = []
        self._time_step_size_ms = 0.12
        self._membrane_potential_V = 0
        self._resistance_kohm = 1
        self._capacitance_uF = 10

        self._input_current_amp = 0

        self._refractory_ms = 6
        self._refractory_until_ms = 0
        self._age = 0

        self._spike_threshold_V = 1
        self._spike_delta_V = 0.5
        self._time_constant_ms = self._resistance_kohm * self._capacitance_uF

    def _fire(self):
        for cb in self._fire_callbacks:
            cb(self)

    def add_fire_hook(self, cb: Callable):
        self._fire_callbacks.append(cb)

    def step(self):
        if self._age > self._refractory_until_ms:
            self._membrane_potential_V += (
                (
                    (-1 * self._membrane_potential_V)
                    + (self._input_current_amp * self._resistance_kohm)
                )
                / (self._time_constant_ms)
            ) * self._time_step_size_ms
            if self._membrane_potential_V >= self._spike_threshold_V:
                self._membrane_potential_V += self._spike_delta_V
                self._refractory_until_ms = self._age + self._refractory_ms
                self._fire()
        else:
            self._membrane_potential_V = 0
        # Leak summed current:
        self._input_current_amp *= 0.9
        self._age += self._time_step_size_ms

    def get_membrane_potential(self):
        return self._membrane_potential_V

    def add_current(self, target_amp):
        self._input_current_amp += target_amp

    def set_current(self, target_amp):
        self._input_current_amp = target_amp

    def set_membrane_potential(self, target_V):
        self._input_current_amp = target_V / self._resistance_kohm


class Synapse:
    """
    An abstract Synapse object that manages connectivity of Neurons.
    """

    def __init__(self):
        self.u = None
        self.v = None

    def connect(self, u, v):
        self.u = u
        self.v = v


class BasicCurrentSynapse(Synapse):
    def __init__(self, current: float = 1.5):
        self._current = current

    def get_output_current(self):
        return self._current


class Electrode:
    """
    An electrode can read and write to a cell.
    """

    def __init__(self, target: Neuron) -> None:
        self._target = target

    def measure(self) -> float:
        """
        Get the membrane potential at the target location.
        """
        return self._target.get_membrane_potential()

    def pin(self, target_V: float) -> None:
        """
        Pin to a target mV.
        """
        self._target.set_membrane_potential(target_V)


class Brain:
    """
    A base class for running simulations.

    """

    def __init__(self) -> None:
        """
        Create a new Brain object.
        """
        self._graph = nx.MultiDiGraph()

    def add_neuron(self, name: Hashable, neuron: Neuron) -> Hashable:
        """
        Add a neuron to the network.

        """
        self._graph.add_node(name, neuron=neuron)
        return name

    def neurons(self) -> Dict[Hashable, Neuron]:
        return {name: n["neuron"] for name, n in self._graph.nodes(data=True)}

    def get_neuron(self, name: Hashable) -> Neuron:
        return self.neurons()[name]

    def add_synapse(self, u: Hashable, v: Hashable, synapse: Synapse = None) -> None:

        if u not in self._graph:
            raise ValueError(f"Unknown neuron ID {u}.")
        if v not in self._graph:
            raise ValueError(f"Unknown neuron ID {v}.")

        synapse = synapse or BasicCurrentSynapse()
        synapse.connect(self.get_neuron(u), self.get_neuron(v))

        self.get_neuron(u).add_fire_hook(
            lambda u: self.get_neuron(v).add_current(synapse.get_output_current())
        )
        self._graph.add_edge(u, v, synapse=synapse)

        return None

    def add_electrode(self, location: Hashable) -> Electrode:
        """
        Add an electrode targeted to the specified neuron.
        """
        e = Electrode(self.get_neuron(location))
        return e

    def step(self) -> None:
        """
        Perform one step of the brian simulation.
        """
        for _, neuron in self.neurons().items():
            neuron.step()

    def run(self, frame_count: int) -> None:
        """
        Run several steps of the brian simulation.

        """
        for _ in range(frame_count):
            self.step()
