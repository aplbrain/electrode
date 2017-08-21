package main

/*
A NeuronPoolSimulator simulates a pool of Neurons.
*/
type NeuronPoolSimulator interface {
	Step()
	GetNeuron(string) Neuron
	GetNeurons() map[string]Neuron
	AddNeuron(string, Neuron) string
	GetType() string
	AddEdge(Edge) int
	GetEdges() []Edge
	Init()
	InsertElectrode(string, string) *Electrode
	GetElectrodes() map[[2]string]Electrode
}
