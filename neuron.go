package main

type Segment interface {
	GetMembranePotential() float64
	SetMembranePotential(float64)
	IncrementMembranePotential(float64) float64
}

type SimpleSegment struct {
	membranePotential float64
}

func (segment *SimpleSegment) GetMembranePotential() float64 {
	return segment.membranePotential
}
func (segment *SimpleSegment) SetMembranePotential(vm float64) {
	segment.membranePotential = vm
}
func (segment *SimpleSegment) IncrementMembranePotential(vm float64) float64 {
	segment.SetMembranePotential(vm)
	return segment.GetMembranePotential()
}

/*
Neuron is the interface for a singular biological neuron.
Likely implemented by a point-model or a full biophysical model.
*/
type Neuron interface {
	// Simulates a single timestep of a neuron.
	Step()

	// Call all actions that rely on a neuron's firing of AP:
	Fire()

	GetSegments() []Segment
}

/*
A IAFNeuron runs a neuron according to the Integrate-And-Fire formulae.
This version is "leaky": https://en.wikipedia.org/wiki/Biological_neuron_model

The neuron contains only a single segment.
*/
type IAFNeuron struct {
	// The constituent segments:
	segments []Segment
}

/*
NewIAFNeuron constructs a new IAFNeuron.
*/
func NewIAFNeuron() *IAFNeuron {
	n := IAFNeuron{}
	return &n
}

/*
Step through a single timepoint.
*/
func (neuron *IAFNeuron) Step() {
	//
}

/*
Fire is the canonical Callback for an IAF to Fire.
*/
func (neuron *IAFNeuron) Fire() {
	// TODO: Read listeners and execute
}

/*
GetSegments returns the list of segments
*/
func (neuron *IAFNeuron) GetSegments() []Segment {
	return neuron.segments
}
