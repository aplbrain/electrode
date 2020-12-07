from electrode import Brain, LIAFNeuron, Electrode


class TestBrain:
    def test_can_create_brain(self):
        b = Brain()
        assert isinstance(b, Brain)

    def test_can_add_neuron_to_brain(self):
        b = Brain()
        b.add_neuron("A", LIAFNeuron())
        assert len(b.neurons()) == 1
        assert "A" in b.neurons()

    # def test_can_add_synapse_between_neurons(self):
    #     b = Brain()
    #     b.add_neuron("A", LIAFNeuron())
    #     b.add_neuron("B", LIAFNeuron())
    #     b.add_synapse("A", "B", LIAFSynapse())
    #     assert len(b.synapses()) == 1


class TestElectrode:
    def test_can_add_electrode(self):
        b = Brain()
        b.add_neuron("A", LIAFNeuron())
        e = b.add_electrode("A")
        assert isinstance(e, Electrode)

    def test_electrode_can_measure(self):
        b = Brain()
        b.add_neuron("A", LIAFNeuron())
        e = b.add_electrode("A")
        assert e.measure() == 0

    def test_electrode_can_pin(self):
        b = Brain()
        b.add_neuron("A", LIAFNeuron())
        e = b.add_electrode("A")
        e.pin(500)
        b.step()
        assert e.measure() == 500
        b.run(50)
        assert e.measure() != 500

