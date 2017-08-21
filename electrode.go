package main

/*
An Electrode can read or write to a neural segment.
*/
type Electrode struct {
	neuron, segment    string
	input              float64
	output             float64
	neuronLookup       map[string](Neuron)
	pinCyclesRemaining int
}

func (electrode *Electrode) Read() float64 {
	return electrode.neuronLookup[electrode.neuron].GetSegment(electrode.segment).GetMembranePotential()

}

func (electrode *Electrode) PinVoltage(v float64, c int) {
	electrode.pinCyclesRemaining = c
	electrode.input = v
	electrode.output = v
}
