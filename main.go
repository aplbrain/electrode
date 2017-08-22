package main

import "time"

func main() {
	// Create a new Brain and set its simulator:
	b := Brain{
		simulator: NewLocalNeuronPoolSimulator(),
	}

	b.AddNeuron("AAAA", NewIAFNeuron())
	b.AddNeuron("AAAB", NewIAFNeuron())
	b.AddNeuron("AAAC", NewIAFNeuron())
	b.AddEdge(&SimpleEdge{
		from: [2]string{"AAAA", "soma"},
		to:   [2]string{"AAAB", "soma"},
		// latency: 1,
	})
	b.AddEdge(&SimpleEdge{
		from: [2]string{"AAAB", "soma"},
		to:   [2]string{"AAAC", "soma"},
		// latency: 5,
	})
	b.AddEdge(&SimpleEdge{
		from: [2]string{"AAAC", "soma"},
		to:   [2]string{"AAAA", "soma"},
		// latency: 2,
	})

	e1 := b.InsertElectrode("AAAA", "soma")
	_ = b.InsertElectrode("AAAB", "soma")

	ticker := time.NewTicker(5 * time.Second)
	quit := make(chan struct{})
	go func() {
		for {
			select {
			case <-ticker.C:
				e1.PinVoltage(10, 10)

			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()

	// froze, _ := json.MarshalIndent(b.Freeze(), "", "\t")
	// freeze := string(froze)
	// fmt.Println(freeze)

	b.Simulate()
}
