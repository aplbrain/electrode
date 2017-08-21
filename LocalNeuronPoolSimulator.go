package main

import (
	"sync"
)

/*
Edge objects contain edge-information that underly the connectivity of
a simple connectome model.
*/
type Edge struct {
	from, to [2]string
	latency  int64
	weight   float64
	// Unused:
	lambda float64
	tau    float64
}

/*
A LocalNeuronPoolSimulator runs all simulation on the user's local machine.
It uses a map of neurons to keep track.
*/
type LocalNeuronPoolSimulator struct {
	neurons map[string]Neuron
	edges   []Edge
}

/*
NewLocalNeuronPoolSimulator creates a new LocalNeuronPoolSimulator
*/
func NewLocalNeuronPoolSimulator() *LocalNeuronPoolSimulator {
	n := LocalNeuronPoolSimulator{}
	n.neurons = make(map[string]Neuron)
	n.edges = make([]Edge, 0)
	return &n
}

/*
Init initializes the simulator.
*/
func (nsim *LocalNeuronPoolSimulator) Init() {
	// Schedule all edge firings for this simulator:
	// var wge sync.WaitGroup
	// for e := 0; e < len(nsim.edges); e++ {
	// 	wge.Add(1)
	// 	go func(ee Edge) {
	// 		time.Sleep(time.Millisecond * time.Duration(ee.latency))
	// 		// time.Sleep(time.Second * time.Duration(ee.latency))
	// 		// timer := time.NewTimer(time.Second * time.Duration(ee.latency))
	// 		// <-timer.C

	// 		println("!", ee.latency)
	// 		nsim.neurons[ee.to].Excite(ee.weight)
	// 		defer wge.Done()
	// 	}(nsim.edges[e])
	// }
	// wge.Wait()
}

/*
Step through a single timestep.
*/
func (nsim *LocalNeuronPoolSimulator) Step() {
	var wg sync.WaitGroup
	for _, n := range nsim.neurons {
		wg.Add(1)
		go func(ni Neuron) {
			ni.Step()
			defer wg.Done()
		}(n)
	}
	wg.Wait()
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
	// fmt.Println(len(nsim.edges))
	return len(nsim.edges)
}
