#!/usr/bin/env python3
"""
Neuron classes (implementations of neuron).

You can implement Neuron to generate your own simulation type.
"""
#electrode
from abc import ABCMeta, abstractmethod
import typing

import uuid
import networkx as nx

#brian2
from brian2 import * 

############# Brian 2 #############

class Brian2_NeuronModel:
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
        '''
        sets up the monitors to record the neuron groups

        Returns
        -------
        state and spike monitors for the neuron group
            DESCRIPTION.

        '''
        
        return StateMonitor(self.neuron_group, True , record=True), SpikeMonitor(self.neuron_group) 

        
class Brian2_HodgkinHuxley(Brian2_NeuronModel):
    
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

    

class Brian2_LeakyIntegrateandFire(Brian2_NeuronModel):
    
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

############# Electrode #############

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
