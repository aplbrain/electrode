package main

import (
	"encoding/json"
	"fmt"
	"time"
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

/*
Simulate the brain, stepping through until stopped.
TODO: How to stop?!
*/
func (brain *Brain) Simulate() {
	brain.simulator.Init()

	ticker := time.NewTicker(50 * time.Millisecond)
	quit := make(chan struct{})
	go func() {
		for {
			select {
			case <-ticker.C:
				for _, v := range brain.simulator.GetElectrodes() {
					fmt.Printf("\r %f", v.Read())
				}
			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()

	for f := 0; f < 1; f++ {
		brain.simulator.Step()
	}

}

/*
AddNeuron adds a neuron to the brain's simulator. It is simply a pass-through,
and is entirely agnostic about what the simulator does with it.
*/
func (brain *Brain) AddNeuron(s string, n Neuron) string {
	return brain.simulator.AddNeuron(s, n)
}

/*
AddEdge adds an edge between two neurons — and specifically, between two
Segments. This is how you make a synapse happen!
*/
func (brain *Brain) AddEdge(e Edge) int {
	return brain.simulator.AddEdge(e)
}

/*
InsertElectrode adds an electrode to the brain for IO.
*/
func (brain *Brain) InsertElectrode(neuron, location string) *Electrode {
	return brain.simulator.InsertElectrode(neuron, location)
}
