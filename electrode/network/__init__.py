#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:33:48 2020

@author: kitchlm1
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from brian2 import * # fix this 
import os


class Network:
    def __init__(self, **kwargs):
        '''
        Create a new brain graph. This will create an empty graph unless
        a networkx graph is passed in as a kwarg
        
        net = Network()
        
        or 
        
        net = Network(graph = nx.read_graphml('c_elegans_control.graphml'))
        
        Parameters
        ----------
        **kwargs : 
            graph:  networkx graph
        '''
        if 'graph' in kwargs:
            self.graph = kwargs['graph']
            
        else:
            self.graph = nx.DiGraph()
        self.original_graph = self.graph.copy()
        
    def add_nodes(self, node_list):
        """
        Add one or more new nodes to the network.
        
        Parameters
        ----------
        node_list: (list of str) 
            list of nodes to add.
        """
       
        self.graph.add_nodes_from(node_list)         
    
    def add_edges(self, edge_list):
        """
        Add one or more new edges to the network.
        
        Parameters
        ----------
        edge_list: list of tuples (source (str), target (str))
            edges to add to the network
        """
        
        self.graph.add_edges_from(edge_list)
        
    def add_weighted_edges(self, edge_list):
        """
        Add one or more new weighted edges to the network.
        
        Parameters
        ----------
        edge_list: list of tuples (source (str), target (str), weight)
            edges and weights to add to the network
        """
        
        self.graph.add_weighted_edges_from(edge_list)

    def ablate(self, ablate_list):
        '''
        ablates one or more nodes from the brain graph

        Parameters
        ----------
        ablate_list : list of nodes (str) to remove from the graph

    
        '''
        self.graph.remove_nodes_from(ablate_list)
        
    def reset(self):
        '''
        undo the ablations


        '''
        
        self.graph = self.original_graph.copy()
        

########## util functions #############


def get_nodes_by_attribute(network, attribute, attribute_value):
    '''
    Returns a list of nodes that have a specific value for a specific attribute

    Parameters
    ----------
    network: networkx network
    attribute: (str)
        attribute name
    attribute_value: (str)
        attribute value

    Returns
    -------
    attr_nodes : list of nodes that have the specific value for a specific attribute

    '''
    
    attr_nodes = []
    for neuron, all_attr in network.graph.nodes(data = True):
        if attribute in all_attr:
            if all_attr[attribute] == attribute_value:
                    attr_nodes.append(neuron)
    return attr_nodes

def get_possible_attributes(network):
    '''
    Returns a list of all possible attributes in the graph

    Parameters
    ----------
    network : networkx network
    

    Returns
    -------
    att_type : list of attributes in the graph

    '''
    
    # get list of possible attributes
    att_type = []
    for node, all_attr in network.graph.nodes(data = True):
        for spec_att in all_attr:
            if spec_att not in att_type:
                att_type.append(spec_att)
    return att_type

def get_attribute_values(network, attribute):
    '''
    Returns the list of all possible values of a specific attribute in the graph

    Parameters
    ----------
    network : networkx network
    attribute (str): attribute name 

    Returns
    -------
    att_values : list of all possible values of a specific attribute in the graph

    '''
    att_values = []
    for node, all_attr in network.graph.nodes(data = True):
        if attribute in all_attr:
            if all_attr[attribute] not in att_values:
                att_values.append(all_attr[attribute])
    return att_values

###############Visualization functions############   
        
def view_brain_graph(network):
    '''
    Plot the brain graph

    Parameters
    ----------
    network : networkx network
        
    '''
    
    pos = nx.spring_layout(network.graph,k=1.5)        # k controls the distance between the nodes and varies between 0 and 1
        # iterations is the number of times simulated annealing is run
        # default k =0.1 and iterations=50
    #bipartite, circular,planar,rescale,spring,spiral,spectrum
    plt.figure(figsize=(50,50)) 
    nx.draw(network.graph, pos,font_size=12, width = 2.0)

def view_brain_graph_circular(network):
    '''
    Plot the brain graph in a circle

    Parameters
    ----------
    network : networkx network
        
    '''
    
    plt.figure(figsize=(50,50)) 
    nx.draw_circular(network.graph, font_size=12, width = 2.0)

     
def view_ablated_brain_graph(network):
    '''
    Plot the brain graph and show which nodes were ablated    

    Parameters
    ----------
    network : networkx network
        
    '''
    #VISUALIZING NODE ABLATION
    #Node color map that adds blue if node exists in control 
    #and perturbed connectome, and red if node exists 
    #in control but NOT perturbed
    node_color_map = []
    for nodes in list(network.original_graph.nodes()):
        if nodes in network.graph.nodes():
            node_color_map.append('blue')
        else:
            node_color_map.append('red')

    #Edge color map that adds blue if edge exists in control/perturbed connectome, and red if edge exists in control but NOT perturbed
    edge_color_map = []
    for edges in list(network.original_graph.edges()):
        if edges in network.graph.edges:
            edge_color_map.append('gray')
        else:
            edge_color_map.append('red')

    pos = nx.spring_layout(network.original_graph,k=1.5)        # k controls the distance between the nodes and varies between 0 and 1
        # iterations is the number of times simulated annealing is run
        # default k =0.1 and iterations=50
    #bipartite, circular,planar,rescale,spring,spiral,spectrum
    plt.figure(figsize=(50,50)) 
    nx.draw(network.original_graph, pos,font_size=12, edge_color = edge_color_map,with_labels=True, node_color = node_color_map, width = 2.0)

def view_ablated_brain_graph_circular(network):
    '''
    Plot the brain graph and show which nodes were ablated

    Parameters
    ----------
    network : networkx network
        
    '''
    #VISUALIZING NODE network
    #Node color map that adds blue if node exists in control 
    #and perturbed connectome, and red if node exists 
    #in control but NOT perturbed
    node_color_map = []
    for nodes in list(network.original_graph.nodes()):
        if nodes in network.graph.nodes():
            node_color_map.append('blue')
        else:
            node_color_map.append('red')

    #Edge color map that adds blue if edge exists in control/perturbed connectome, and red if edge exists in control but NOT perturbed
    edge_color_map = []
    for edges in list(network.original_graph.edges()):
        if edges in network.graph.edges:
            edge_color_map.append('gray')
        else:
            edge_color_map.append('red')

    plt.figure(figsize=(50,50)) 
    nx.draw_circular(network.original_graph, font_size=12, edge_color = edge_color_map,with_labels=True, node_color = node_color_map, width = 2.0)


