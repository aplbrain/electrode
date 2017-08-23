package main

import (
	"fmt"
	"time"
)

func main() {
	// Create a new Brain and set its simulator:
	b := Brain{
		simulator: NewLocalNeuronPoolSimulator(),
	}

	popn := int(1e2)
	for i := 0; i < popn; i++ {
		b.AddNeuron(fmt.Sprintf("%d", i), NewIAFNeuron())
	}

	for i := 0; i < popn; i++ {
		for j := 0; j < popn; j++ {
			if i != j {
				b.AddEdge(&SimpleEdge{
					from: [2]string{fmt.Sprintf("%d", i), "soma"},
					to:   [2]string{fmt.Sprintf("%d", j), "soma"},
				})
			}
		}
	}

	e1 := b.InsertElectrode("0", "soma")
	_ = b.InsertElectrode("50", "soma")

	ticker := time.NewTicker(4 * time.Second)
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
