#!/usr/bin/env python3
"""
Brain module.
The master file for the simulator.
"""

#for electrode
from typing import Tuple
import networkx as nx #2.4
import numpy as np
import os

from .. import timing
from ..neuron import Neuron
from ..synapse import Synapse

#for brian2
from brian2 import * 

############# Brian 2 #############

class Brian2_Brain:
    def __init__(self):
        '''
        Create a new brian2 brain. 

        '''
        self._neuron_groups = {}
        self._synapses = {}
        self._neuronmonitors = {}
        self._synapsemonitors ={}
        self._spikemonitors = {}
  
    def add_group_of_neurons(self, node_list, group_name, neuronmodel):
        '''
        Create a brian2 neuron group for a group of neurons. 

        Parameters
        ----------
        node_list : list of str
            list of the nodes to add to this neuron group.
        group_name : str
            name of this neuron group
        neuronmodel : Brian2_NeuronModel
            the neuron model to use

        Returns
        -------
        None.

        '''
       
        self._neuron_groups[group_name] = neuronmodel
        self._neuronmonitors[group_name], self._spikemonitors[group_name] =  self._neuron_groups[group_name].setUpMonitors()
        
        
    def add_single_neuron(self, node_name, neuronmodel):
        '''
        Creates a brian2 neuron group for a single new neuron.

        Parameters
        ----------
        node_name : str
            name of the node to create a neuron for
        neuronmodel : Brian2_NeuronModel
            the neuron model to use

        Returns
        -------
        None.

        '''
    
       
        self._neuron_groups[node_name] = neuronmodel
        self._neuronmonitors[node_name], self._spikemonitors[node_name] =  self._neuron_groups[node_name].setUpMonitors()
        


    def add_synapses(self, synapse_group_name, source_ng, target_ng, edges, model, on_pre, **kwargs):
        '''
        Creates synapse between neuron groups following Brian2 

        Parameters
        ----------
        synapse_group_name : str
            name for this synapse group.
        source_ng : brian2 neuron group
        target_ng : brian2 neuron group
        edges : list of tuples
            edges connecting the neurons in the groups
        model : TYPE
            DESCRIPTION.
        on_pre : TYPE
            DESCRIPTION.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        ## todo pass kwargs to Synapses
    
        self._synapses[synapse_group_name] = Synapses(source_ng.neuron_group, target_ng.neuron_group, model, on_pre, name='synapses*')
        
        for (u, v, c) in edges:
            i = source_ng.name_index[u]
            j = target_ng.name_index[v]
            self._synapses[synapse_group_name].connect(i=i,j=j)
            self._synapses[synapse_group_name].w[i, j] = float(c)
        
        if 'delay' in kwargs:
            self._synapses[synapse_group_name].delay = kwargs['delay']
        self._synapsemonitors[synapse_group_name] = StateMonitor(self._synapses[synapse_group_name], 'v', record=True)
        
         

    def run_simulation(self, time):
        '''
        run a brian2 simulation 

        Parameters
        ----------
        time : int 
            time in ms to run the simulation

        Returns
        -------
        None.

        '''
        
       if hasattr(self, 'sim_network') == False:
           self.sim_network = Network()
           for n in self._neuron_groups.values():
               self.sim_network.add(n.neuron_group)
               
           self.sim_network.add(self._synapses.values(),  self._neuronmonitors.values(), self._synapsemonitors.values(), 
                                      self._spikemonitors.values() )
           self.sim_network.store()
       self.sim_network.run(time*ms)
       
    def reset_stimulation(self):
        '''
        reset the simulation to the starting point

        Returns
        -------
        None.

        '''
       self.sim_network.restore()

############# Electrode #############

class Electrode:
    def __init__(self, compartment):
        self.compartment = compartment

    def record(self):
        return self.compartment["mV"]

    def stim(self, current: float = 0):
        self.compartment["mV"] = current


class Electrode_Brain:
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
        if len(key) == 2:
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