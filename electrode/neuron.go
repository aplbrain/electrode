package main

/*
A Segment handles the logic of local biophysics, or, in the simplest case,
such as an IAFNeuron, simulates the neuron AP curve itself.
*/
type Segment interface {
	GetMembranePotential() float64
	SetMembranePotential(float64)
	IncrementMembranePotential(float64) float64
	GetDownstreamEdges() []*Edge
	GetDownstreamSegments() []*Segment
	AddDownstreamEdge(*Edge)
}

/*
A SimpleSegment changes mV according to a prescribed function and does not
simulate ion channels.
*/
type SimpleSegment struct {
	membranePotential  float64
	downstreamEdges    []*Edge
	downstreamSegments []*Segment
}

func (segment *SimpleSegment) GetDownstreamEdges() []*Edge {
	return segment.downstreamEdges
}
func (segment *SimpleSegment) GetDownstreamSegments() []*Segment {
	return segment.downstreamSegments
}

/*
GetMembranePotential returns the membrane potential at a given region.
*/
func (segment *SimpleSegment) GetMembranePotential() float64 {
	return segment.membranePotential
}

/*
SetMembranePotential sets the membrane potential at this location.
*/
func (segment *SimpleSegment) SetMembranePotential(vm float64) {
	segment.membranePotential = vm
}

/*
IncrementMembranePotential increments the membrane potential at this location.
*/
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

	GetSegments() map[string]Segment

	InsertElectrode(string, *Electrode)
	GetSegment(string) Segment
}

/*
A IAFNeuron runs a neuron according to the Integrate-And-Fire formulae.
This version is "leaky": https://en.wikipedia.org/wiki/Biological_neuron_model

The neuron contains only a single segment.
*/
type IAFNeuron struct {
	// The constituent segments:
	segments   map[string]Segment
	electrodes map[string]*Electrode
}

/*
NewIAFNeuron constructs a new IAFNeuron.
*/
func NewIAFNeuron() *IAFNeuron {
	n := IAFNeuron{}
	n.electrodes = make(map[string]*Electrode)
	n.segments = make(map[string]Segment)
	n.segments["soma"] = &SimpleSegment{
		0,
		[]*Edge{},
		[]*Segment{},
	}
	return &n
}

/*
Step through a single timepoint.
*/
func (neuron *IAFNeuron) Step() {
	for sname, seg := range neuron.segments {
		// print(seg.GetDownstreamEdges()[0].GetFrom()[0])

		seg.SetMembranePotential(seg.GetMembranePotential() * 0.9)
		// TODO: Propagate membrane potential to neighbors

		// TODO: Hop edges across synapses.

		if electrode, exists := neuron.electrodes[sname]; exists {
			if electrode.pinCyclesRemaining > 0 {
				electrode.pinCyclesRemaining--
				seg.SetMembranePotential(electrode.input)
			}
			electrode.output = seg.GetMembranePotential()
		}
	}
}

/*
Fire is the canonical Callback for an IAF to Fire.
*/
func (neuron *IAFNeuron) Fire() {
	// TODO: Read listeners and execute
}

func (segment *SimpleSegment) AddDownstreamEdge(e *Edge) {
	segment.downstreamEdges = append(segment.downstreamEdges, e)
}

/*
GetSegment from neuron
*/
func (neuron *IAFNeuron) GetSegment(s string) Segment {
	return neuron.segments[s]
}

/*
GetSegments returns the list of segments
*/
func (neuron *IAFNeuron) GetSegments() map[string]Segment {
	return neuron.segments
}

/*
InsertElectrode into a particular segment.
*/
func (neuron *IAFNeuron) InsertElectrode(s string, e *Electrode) {
	neuron.electrodes[s] = e
}
