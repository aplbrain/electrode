from brainx import Brain
from netx import Network
from neuronModelx import NeuronModel
import networkx as nx
import timing
from brian2 import *

def configureSynapses(net, brain):
    edges = net.graph.edges.data('weight', default=1)

    
    #pull out the synapses that are within and between the neuron groups
    HHedges = []
    LIFedges = []
    HH_LIFedges = []
    for e in edges:
        if e[0] in brain._neuron_groups['HH_neurons'].name_index.keys():
            if e[1] in brain._neuron_groups['HH_neurons'].name_index.keys():
                HHedges.append(e)
            elif e[1] in brain._neuron_groups['LIF_neurons'].name_index.keys():
                HH_LIFedges.append(e)
        elif e[0] in brain._neuron_groups['LIF_neurons'].name_index.keys():
            if e[1] in brain._neuron_groups['LIF_neurons'].name_index.keys():
                LIFedges.append(e)
            elif e[1] in brain._neuron_groups['LIF_neurons'].name_index.keys():
                HH_LIFedges.append(e)

    #set up inputs for the synapse creation
    smodel = 'w:1'
    on_pre = 'v_post+=w*100*mV'

    #add the synapses between the HH neurons
    source = brain._neuron_groups['HH_neurons']
    brain.add_synapses('HHsynapses', source,source, HHedges, smodel, on_pre)

    #add the synapses between the LIF neurons
    source = brain._neuron_groups['LIF_neurons']
    brain.add_synapses('LIFsynapses', source,source, LIFedges, smodel, on_pre)

    #add the synapses between the HH and LIF neurons
    source = brain._neuron_groups['HH_neurons']
    target = brain._neuron_groups['LIF_neurons']
    brain.add_synapses('HH_LIFsynapses', source, target, HH_LIFedges, smodel, on_pre)

def createHHModel(aBrain):
    exectTime = 1*second
    
    eqs = Equations('''
    dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I)/Cm : volt 
    dm/dt = 0.32*(mV**-1)*4*mV/exprel((13.*mV-v+VT)/(4*mV))/ms*(1-m)-0.28*(mV**-1)*5*mV/exprel((v-VT-40.*mV)/(5*mV))/ms*m : 1
    dn/dt = 0.032*(mV**-1)*5*mV/exprel((15.*mV-v+VT)/(5*mV))/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
    dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
    I : amp
    ''')
    threshold='v > -40*mV'
    refractory='v > -40*mV'
    method='exponential_euler' 
    
    activation_list = [.25*nA] * 199
    neuron_list = list(net.graph.nodes)[198:-1]
    
    aBrain.add_group_of_neurons(neuron_list, 'HH_neurons', neuronModel.HodgkinHuxley(neuron_list, activation_list, exectTime, eqs, threshold, refractory, method, reset))

    return aBrain

def createLIFModel(aBrain):
    
    #set up the inputs for the LIF model
    exectTime = 1*second

    eqs = '''
          dv/dt = -(v-I/g)/tau : volt
          I : amp
          g : siemens'''

    threshold='v > vth'
    refractory='2*ms'
    method='exact'
    reset='v= vr'

    #set up the nodes to add to the LIF neuron group
    neuron_list = list(net.graph.nodes)[0:198]
    
    #set up the list of actiavtions for the LIF neurons
    #this should be a list, with one value per neuron
    activation_list = [25*nA] * 198

    #add the LIF neuron group
    aBrain.add_group_of_neurons(
        neuron_list, 'LIF_neurons', neuronModel.LeakyIntegrateandFire(
            neuron_list, activation_list, exectTime, eqs, threshold, refractory, method, reset
        )
    )

    print(aBrain._neuron_groups['LIF_neurons'])
    
    return aBrain

def createBrain():
    #load in a brain graph
    #'''
    #graph = nx.read_graphml('c_elegans_control.graphml')
    #print(type(graph))
    net = Network(graph = nx.read_graphml('c_elegans_control.graphml'))
    #'''

    #print info on the graph
    print(nx.info(net.graph))

    #create a brain 
    simpleBrain = Brain()

    #check that the neuron group dictionary is empty
    print(simpleBrain._neuron_groups)

    return simpleBrain, net


def main():
    

    brain, net = createBrain()
    
    brain = createLIFModel(brain)

    brain = createHHModel(brain)

    configureSynapses(net, brain)
    
if __name__ == "__main__":
    main()
