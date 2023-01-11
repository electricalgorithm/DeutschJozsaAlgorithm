"""
This module implements the Deutsch-Jozsa algorithm using Qiskit.
"""
import numpy as np
from qiskit import Aer
from qiskit import QuantumCircuit, assemble, transpile
from qiskit.circuit.instruction import Instruction


class DJAlgorithm:
    """This class implements the Deutsch-Jozsa algorithm."""

    @staticmethod
    def simulate(oracle_block: QuantumCircuit) -> dict:
        """
        Run the Deutsch-Jozsa algorithm on the simulator.

        :param oracle_block: The oracle block to check with Deutsch-Jozsa algorithm.
        :return: The result of the algorithm as dictionary. Check "result" attribute.
        """
        circuit = DJAlgorithm._construct_the_circuit(oracle_block)
        aer_sim = Aer.get_backend("aer_simulator")
        transpiled_dj_circuit = transpile(circuit, aer_sim)
        qobj = assemble(transpiled_dj_circuit)
        results = aer_sim.run(qobj).result()
        answer = results.get_counts()

        if "0" * (circuit.num_qubits - 1) in answer:
            return {"result": "Constant"}
        else:
            return {"result": "Balanced"}

    @staticmethod
    def give_a_balanced_oracle(inputs_count: int) -> Instruction:
        """Returns a balanced oracle function.

        :param inputs_count: The number of input qubits.
        :return: The balanced oracle function as Instruction.
        """
        # Get the number of input qubits.
        random_number = np.random.randint(1, 2**inputs_count)
        inputs = format(random_number, "0" + str(inputs_count) + "b")

        # Create a quantum circuit with the number of input qubits + 1 output qubit.
        oracle = QuantumCircuit(inputs_count + 1, inputs_count)

        # Place X gates on the start of input qubit lines.
        for index, qubit in enumerate(reversed(inputs)):
            if qubit == "1":
                oracle.x(index)

        # Apply the oracle block.
        for index, qubit in enumerate(inputs):
            oracle.cx(index, inputs_count)

        # Place X-gates on the end of input qubits lines.
        for index, qubit in enumerate(reversed(inputs)):
            if qubit == "1":
                oracle.x(index)

        inst = oracle.to_instruction()
        inst.name = "BalancedOracle"
        return inst

    @staticmethod
    def give_a_constant_oracle(inputs_count: int) -> Instruction:
        """Returns a constant oracle function.

        :param inputs_count: The number of input qubits.
        :return: The balanced oracle function as Instruction.
        """
        # Create a quantum circuit with the number of input qubits + 1 output qubit.
        oracle = QuantumCircuit(inputs_count + 1)

        if np.random.randint(2) == 1:
            oracle.x(inputs_count)

        inst = oracle.to_instruction()
        inst.name = "ConstantOracle"
        return inst

    @staticmethod
    def _construct_the_circuit(oracle_block: QuantumCircuit) -> QuantumCircuit:
        """It creates the circuit for the Deutsch-Jozsa algorithm.

        :param oracle_block: The oracle block to check with Deutsch-Jozsa algorithm.
        :return: The circuit for the Deutsch-Jozsa algorithm.
        """
        # Get the number of input qubits.
        input_length = oracle_block.num_qubits - 1

        _circuit = QuantumCircuit(input_length + 1, input_length)

        # Apply Hadamard gates to all input qubits.
        for qubit in range(input_length):
            _circuit.h(qubit)

        # Convert the last qubit to |-) state.
        _circuit.x(input_length)
        _circuit.h(input_length)
        _circuit.barrier()

        # Apply the oracle block.
        _circuit.append(
            oracle_block, range(oracle_block.num_qubits), range(oracle_block.num_clbits)
        )
        _circuit.barrier()

        # Apply Hadamard gates to all input qubits.
        for qubit in range(input_length):
            _circuit.h(qubit)
        _circuit.barrier()

        # Measure all input qubits and put them to classical bits.
        for qubit in range(input_length):
            _circuit.measure(qubit, qubit)

        return _circuit


if __name__ == "__main__":
    print("===================================")
    print("Deutsch-Jozsa Algorithm Simulation")
    print("===================================")

    # Get the number of input qubits.
    inputs_count = int(input("> Enter the number of input qubits: "))

    # Get the oracle block.
    oracle_type = input("> Enter the type of oracle (c)onstant/(b)alanced: ")
    oracle_type = oracle_type.lower()
    if oracle_type == "constant" or oracle_type == "c":
        block_to_test = DJAlgorithm.give_a_constant_oracle(inputs_count)
    elif oracle_type == "balanced" or oracle_type == "b":
        block_to_test = DJAlgorithm.give_a_balanced_oracle(inputs_count)
    else:
        print("Invalid oracle type.")
        exit(1)

    # Run the algorithm.
    result = DJAlgorithm.simulate(block_to_test)
    print("Result: " + result["result"])
