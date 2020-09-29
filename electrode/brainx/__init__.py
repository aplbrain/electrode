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
    def __init__(self, **kwargs):
        '''
        Create a new brain. 
        '''
        self._neuron_groups = {}
        self._synapses = {}
        self._neuronmonitors = {}
        self._synapsemonitors ={}
        self._spikemonitors = {}
  
    
        
    def add_neuron(self, node_name, neuron):
        """
        Creates a single new neuron. 
        
        Arguments:
            neuron (electrode.NeuronModel): The neuron to add.
        Returns:
            None
        """
    
       
        self._neuron_groups[node_name] = neuron
        self._neuronmonitors[node_name], self._spikemonitors[node_name] =  self._neuron_groups[node_name].setUpMonitors()
        


    def add_synapses_from_network(self, network, model, on_pre, **kwargs):
        ## todo pass kwargs to Synapses
        """
        Creates all the synapses. Run after creating all neurons.
          
        Arguments:
            network: network class
            model:
            on_pre:
            **kwargs : 
        Returns:
            None
        """
        for (u, v, c) in tqdm(network.graph.edges.data('weight', default=1)):
            i=self._neuron_groups[u].neuron_group
            j=self._neuron_groups[v].neuron_group
            self._synapses[u+'_'+v] = Synapses(i, j, model, on_pre, name='synapses*')
            self._synapses[u+'_'+v].connect(i=i,j=j)
            self._synapses[u+'_'+v].w = float(c)
            if 'delay' in kwargs:
                self._synapses[u+'_'+v].delay = kwargs['delay']
            self._synapsemonitors[u+'_'+v] = StateMonitor(self._synapses[u+'_'+v], 'v', record=True)
            
         


    def run_simulation(self, time):
            
       self.sim_network = Network(self._neuron_groups.values(), self._synapses.values(), 
                                  self._neuronmonitors.values(), self._synapsemonitors.values(), 
                                  self._spikemonitors.values() )
       self.sim_network.run(time*ms)
