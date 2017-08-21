package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	// Create a new Brain and set its simulator:
	b := Brain{
		simulator: NewLocalNeuronPoolSimulator(),
	}

	b.AddNeuron("AAAA", new(IAFNeuron))
	b.AddNeuron("AAAB", new(IAFNeuron))
	b.AddNeuron("AAAC", new(IAFNeuron))
	b.AddEdge(Edge{
		from:    [2]string{"AAAA", "1"},
		to:      [2]string{"AAAB", "1"},
		latency: 1,
	})
	b.AddEdge(Edge{
		from:    [2]string{"AAAB", "1"},
		to:      [2]string{"AAAC", "1"},
		latency: 5,
	})
	b.AddEdge(Edge{
		from:    [2]string{"AAAC", "1"},
		to:      [2]string{"AAAA", "1"},
		latency: 2,
	})

	froze, _ := json.MarshalIndent(b.Freeze(), "", "\t")
	freeze := string(froze)
	fmt.Println(freeze)
}
