package main

/*
A Brain holds all information required to simulate a neuron pool.
It also holds information about electrode recordings or stimulation.
*/
type Brain struct {
	simulator NeuronPoolSimulator
}

func (brain Brain) Freeze() map[string]string {
	results := map[string]string{
		"Object":        "Brain",
		"SimulatorType": (brain.simulator).GetType(),
	}
	return results
}

func (brain Brain) Simulate() {
	go brain.simulator.Init()

	for {
		brain.simulator.Step()
	}
	// time.Sleep(time.Second)

}

func (brain Brain) AddNeuron(s string, n Neuron) string {
	return brain.simulator.AddNeuron(s, n)
}

func (brain Brain) AddEdge(e Edge) int {
	return brain.simulator.AddEdge(e)
}
