package main

/*
Neuron is the interface for a singular biological neuron.
Likely implemented by a point-model or a full biophysical model.
*/
type Neuron interface {
	// Simulates a single timestep of a neuron.
	Step()

	// Gets the instantaneous membrane potential for a neuron.
	GetMembranePotential() float64

	// Call all actions that rely on a neuron's firing of AP:
	Fire()

	// Excites a neuron:
	Excite(float64) float64
}

/*
A HodgkinHuxleyNeuron runs a neuron according to the HH formulae.
*/
type HodgkinHuxleyNeuron struct {
	excitation float64
}

/*
Step through a single timepoint.
*/
func (neuron HodgkinHuxleyNeuron) Step() {
	neuron.excitation *= 0.5

}

/*
A IAFNeuron runs a neuron according to the Integrate-And-Fire formulae.
This version is "leaky": https://en.wikipedia.org/wiki/Biological_neuron_model
*/
type IAFNeuron struct {
	excitation float64
}

/*
Step through a single timepoint.
*/
func (neuron IAFNeuron) Step() {
	// println(neuron.excitation)
	neuron.excitation *= 0.9
}

/*
Excite a neuron in 0 time.
*/
func (neuron IAFNeuron) Excite(e float64) float64 {
	neuron.excitation += e
	return neuron.excitation
}

/*
Fire is the canonical Callback for an IAF to Fire.
*/
func (neuron IAFNeuron) Fire() {
	// TODO: Read listeners and execute
}

/*
GetMembranePotential for a given neuron:
*/
func (neuron IAFNeuron) GetMembranePotential() float64 {
	// Not implemented:
	return 0
}
