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

/*
A LocalNeuronPoolSimulator runs all simulation on the user's local machine.
It uses a map of neurons to keep track.
*/
type LocalNeuronPoolSimulator struct {
	electrodes map[[2]string]Electrode
	neurons    map[string]Neuron
	edges      []Edge
}

/*
NewLocalNeuronPoolSimulator creates a new LocalNeuronPoolSimulator
*/
func NewLocalNeuronPoolSimulator() *LocalNeuronPoolSimulator {
	n := LocalNeuronPoolSimulator{}
	n.electrodes = make(map[[2]string]Electrode)
	n.neurons = make(map[string]Neuron)
	n.edges = make([]Edge, 0)
	return &n
}

/*
Init initializes the simulator.
*/
func (nsim *LocalNeuronPoolSimulator) Init() {
	// pass
}

/*
Step through a single timestep.
*/
func (nsim *LocalNeuronPoolSimulator) Step() {
	for _, e := range nsim.edges {
		presyn := nsim.GetNeuron(e.GetFrom()[0]).GetSegment(e.GetFrom()[1]).GetMembranePotential()
		if presyn >= 10 {
			nsim.GetNeuron(e.GetTo()[0]).GetSegment(e.GetTo()[1]).SetMembranePotential(presyn)
			// nsim.GetNeuron(e.GetFrom()[0]).GetSegment(e.GetFrom()[1]).SetMembranePotential(0)
		}
	}

	for _, n := range nsim.neurons {
		n.Step()
	}
}

/*
GetType returns the (string) type of the simulator.
*/
func (nsim *LocalNeuronPoolSimulator) GetType() string {
	return "LocalNeuronPoolSimulator"
}

/*
GetEdges returns the (string) type of the simulator.
*/
func (nsim *LocalNeuronPoolSimulator) GetEdges() []Edge {
	return nsim.edges
}

/*
GetNeuron returns the neuron in the pool from the given key.
*/
func (nsim *LocalNeuronPoolSimulator) GetNeuron(key string) Neuron {
	result, _ := nsim.neurons[key]
	return result
}

/*
GetNeurons returns the list of neurons neuron in the pool.
*/
func (nsim *LocalNeuronPoolSimulator) GetNeurons() map[string]Neuron {
	return nsim.neurons
}

/*
AddNeuron adds the neuron to the pool and returns the final key.
*/
func (nsim *LocalNeuronPoolSimulator) AddNeuron(k string, n Neuron) string {
	_, exists := nsim.neurons[k]
	if exists {
		// uh oh
	} else {
		nsim.neurons[k] = n
	}
	return k
}

/*
AddEdge adds the edge to the pool and returns the edge index.
*/
func (nsim *LocalNeuronPoolSimulator) AddEdge(e Edge) int {
	nsim.edges = append(nsim.edges, e)
	nsim.GetNeuron(e.GetFrom()[0]).GetSegment(e.GetFrom()[1]).AddDownstreamEdge(&e)
	return len(nsim.edges)
}

/*
RegisterElectrode into the brainsim.
*/
func (nsim *LocalNeuronPoolSimulator) RegisterElectrode(n, s string, e *Electrode) {
	nsim.electrodes[[2]string{n, s}] = *e
}

/*
ReadElectrode into the brainsim.
*/
func (nsim *LocalNeuronPoolSimulator) ReadElectrode(n, s string, e *Electrode) {
	nsim.electrodes[[2]string{n, s}] = *e
}

/*
InsertElectrode into the brainsim.
*/
func (nsim *LocalNeuronPoolSimulator) InsertElectrode(n, s string) *Electrode {
	e := Electrode{
		neuron:             n,
		segment:            s,
		output:             0,
		neuronLookup:       nsim.neurons,
		pinCyclesRemaining: 0,
	}
	nsim.neurons[n].InsertElectrode(s, &e)
	nsim.RegisterElectrode(n, s, &e)
	return &e
}

func (nsim *LocalNeuronPoolSimulator) GetElectrodes() map[[2]string]Electrode {
	return nsim.electrodes
}
