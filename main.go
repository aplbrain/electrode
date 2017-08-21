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

	b.AddNeuron("AAAA", NewIAFNeuron())
	b.AddNeuron("AAAB", NewIAFNeuron())
	b.AddNeuron("AAAC", NewIAFNeuron())
	b.AddEdge(SimpleEdge{
		from: [2]string{"AAAA", "soma"},
		to:   [2]string{"AAAB", "soma"},
		// latency: 1,
	})
	b.AddEdge(SimpleEdge{
		from: [2]string{"AAAB", "soma"},
		to:   [2]string{"AAAC", "soma"},
		// latency: 5,
	})
	b.AddEdge(SimpleEdge{
		from: [2]string{"AAAC", "soma"},
		to:   [2]string{"AAAA", "soma"},
		// latency: 2,
	})

	e := b.InsertElectrode("AAAA", "soma")
	e.PinVoltage(10, 10)
	print(e)

	froze, _ := json.MarshalIndent(b.Freeze(), "", "\t")
	freeze := string(froze)
	fmt.Println(freeze)

	b.Simulate()
}
