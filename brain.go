package main

import (
	"encoding/json"
	"os"
)

/*
A Brain holds all information required to simulate a neuron pool.
It also holds information about electrode recordings or stimulation.
*/
type Brain struct {
	simulator NeuronPoolSimulator
}

/*
Freeze the current state of the brain.
*/
func (brain *Brain) Freeze() map[string]string {
	neuronList, _ := json.Marshal(brain.simulator.GetNeurons())
	neuronJSON := string(neuronList)
	results := map[string]string{
		"Object":        "Brain",
		"SimulatorType": (brain.simulator).GetType(),
		"Neurons":       neuronJSON,
	}
	return results
}

//
func (brain *Brain) Simulate() {
	brain.simulator.Init()

	for {
		brain.simulator.Step()
	}

}

//
func (brain *Brain) AddNeuron(s string, n Neuron) string {
	return brain.simulator.AddNeuron(s, n)
}

//
func (brain *Brain) AddEdge(e Edge) int {
	return brain.simulator.AddEdge(e)
}

//
func (brain *Brain) LoadNeuroMLNetwork(file os.File) {
	defer file.Close()

	// var data Query
	// xml.Unmarshal(file, &q)
}
