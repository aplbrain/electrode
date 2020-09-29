"""
Brain module
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from brian2 import * # fix this 
import os
from tqdm import tqdm

class Brain:
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
