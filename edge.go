package main

/*
Edge objects contain edge-information that underly the connectivity of
a simple connectome model.
*/
type Edge interface {
	// from, to [2]string
	// latency  int64
	// weight   float64
	// // Unused:
	// lambda float64
	// tau    float64
}

/*
A SimpleEdge represents the simplest edge (a zero-time synapse.
*/
type SimpleEdge struct {
	from, to [2]string
}
