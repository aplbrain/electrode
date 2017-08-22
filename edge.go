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
	GetFrom() [2]string
	GetTo() [2]string
}

/*
A SimpleEdge represents the simplest edge (a zero-time synapse.
*/
type SimpleEdge struct {
	from, to [2]string
}

func (e *SimpleEdge) GetFrom() [2]string {
	return e.from
}

func (e *SimpleEdge) GetTo() [2]string {
	return e.to
}
