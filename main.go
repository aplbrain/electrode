package main

import (
	"strings"
)

func main() {
	// Create a new Brain and set its simulator:
	b := Brain{
		simulator: NewLocalNeuronPoolSimulator(),
	}

	// Demonstrate brain freeze:
	output := b.Freeze()
	printableResult := ""
	for k, v := range output {
		printableResult += k + strings.Repeat(" ", 15-len(k)) + v + "\n"
	}
	// fmt.Println(printableResult)

	b.AddNeuron("AAAA", IAFNeuron{})
	b.AddNeuron("AAAB", IAFNeuron{})
	b.AddNeuron("AAAC", IAFNeuron{})
	b.AddEdge(Edge{
		from:    "AAAA",
		to:      "AAAB",
		latency: 1,
	})
	b.AddEdge(Edge{
		from:    "AAAA",
		to:      "AAAC",
		latency: 5,
	})

	// Run a single step:
	b.Simulate()
}
