""" The base Neuron class  """


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from brian2 import * # fix this 
import os

class NeuronModel:
    def __init__(self, neuron_list, activation_list, execTime, equation, threshold, refactory, method, reset=None):
        '''
        
        Parameters
        ----------
        neuron_list : list of nodes to add.
        activation_list : list of activations per node.
        execTime : TYPE
            DESCRIPTION.
        equation : TYPE
            DESCRIPTION.
        threshold : TYPE
            DESCRIPTION.
        refactory : TYPE
            DESCRIPTION.
        method : TYPE
            DESCRIPTION.
        reset : TYPE, optional
            DESCRIPTION. The default is None.
        Returns
        -------
        None.
        '''
        simulation_duration = execTime
        eqs = equation
        self.name_index = { neuron_list[x] : x for x in range(len(neuron_list))} 
        
        # Threshold and refractoriness are only used for spike counting
        self.neuron_group = NeuronGroup(len(neuron_list), eqs,
                                   threshold=threshold,
                                   refractory=refactory,
                                   method=method,
                                   reset=reset,  name='neuron*')
        for i in range(len(neuron_list)):
            self.neuron_group.I[i] = activation_list[i]


    def setUpMonitors(self):
        # monitors to record the data
        return StateMonitor(self.neuron_group, True , record=True), SpikeMonitor(self.neuron_group) 

        
class HodgkinHuxley(NeuronModel):
    
    def __init__(self, neuron_list, activation_list, execTime, equation, threshold, refactory, method, reset=None):
        #inherit from NeuronModel
        super().__init__(neuron_list, activation_list, execTime, equation, threshold, refactory, method, reset=None)
        
 
        self.neuron_group.namespace['area'] = 20000*umetre**2
        self.neuron_group.namespace['Cm'] = 1*ufarad*cm**-2 * self.neuron_group.namespace['area']
        self.neuron_group.namespace['gl'] = 5e-5*siemens*cm**-2 * self.neuron_group.namespace['area']
        self.neuron_group.namespace['El'] = -65*mV
        self.neuron_group.namespace['EK'] = -90*mV
        self.neuron_group.namespace['ENa'] = 50*mV
        self.neuron_group.namespace['g_na'] = 100*msiemens*cm**-2 * self.neuron_group.namespace['area']
        self.neuron_group.namespace['g_kd'] = 30*msiemens*cm**-2 * self.neuron_group.namespace['area']
        self.neuron_group.namespace['VT'] = -63*mV

       
        self.neuron_group.v = self.neuron_group.namespace['El']

    

class LeakyIntegratedandFire(NeuronModel):
    """
    new_net = nx.relabel_nodes(net,node_dict) 
    # relabel neuron string names with integer values (e.g. 'ADAL' == 0)
    """
    def __init__(self, neuron_list, activation_list, execTime, equation, threshold, refactory, method, reset=None):
        
        #inherit from NeuronModel
        super().__init__(neuron_list, activation_list, execTime, equation, threshold, refactory, method, reset=None)
   
        
        self.neuron_group.namespace['tau'] = 10*ms #membrane time constant
        self.neuron_group.namespace['vr'] = -40*mV #reset potential
        self.neuron_group.namespace['vth'] = 20*mV #threshold potential
        self.neuron_group.namespace['vh'] = -69.5*mV #holding potential
        self.neuron_group.namespace['Eleak'] = 0*mV
        self.neuron_group.namespace['g_leak'] = 1*usiemens

        
        self.neuron_group.v = self.neuron_group.namespace['vh'] #initial voltage
        self.neuron_group.g = self.neuron_group.namespace['g_leak'] 
