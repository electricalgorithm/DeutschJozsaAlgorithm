# Deutsch-Jozsa Algorithm using Qiskit
The Deutsch-Jozsa algorithm is a quantum algorithm for determining the properties of Boolean functions. Specifically, it can determine whether a given function is constant or balanced, where a constant function always evaluates to the same output (either 0 or 1), and a balanced function evaluates to 0 for half of its inputs and 1 for the other half.
It solves the problem of determining the properties of Boolean function on a single input in one query, where a classical algorithm would take at least n/2 queries where n is number of bits in input.

It is one of the first examples of quantum algorithms that provided exponential speedup over their classical counterparts. The circuit diagram of the Deutsch-Jozsa algorithm is as follows for 3 Qubit input:
```
     ┌───┐      ░ ┌─────────────────┐ ░ ┌───┐ ░ ┌─┐   
q_0: ┤ H ├──────░─┤0                ├─░─┤ H ├─░─┤M├───
     ├───┤      ░ │                 │ ░ ├───┤ ░ └╥┘┌─┐
q_1: ┤ H ├──────░─┤1                ├─░─┤ H ├─░──╫─┤M├
     ├───┤┌───┐ ░ │                 │ ░ └───┘ ░  ║ └╥┘
q_2: ┤ X ├┤ H ├─░─┤2 A Oracle Block ├─░───────░──╫──╫─
     └───┘└───┘ ░ │  That We Don't  │ ░       ░  ║  ║ 
c_0: ═════════════╡0     Know       ╞════════════╩══╬═
                  │                 │               ║ 
c_1: ═════════════╡1                ╞═══════════════╩═
                  └─────────────────┘                 
```

## Usage
It is recommended to use a virtual environment to run the program. To install the required dependencies, run the following command:
```bash
$ pip3 install -r requirements.txt
```

To run the program interface, simply run the following command:
```bash
$ python3 djalgorithm.py
```

## Application Interface
```python
from djalgorithm import DJAlgorithm

n = 4  # Number of qubits.

# Create a function to test with.
# some_function = DJAlgorithm.give_a_constant_function(n)
some_function = DJAlgorithm.give_a_balanced_function(n)

# Use the Deutsch-Jozsa algorithm to solve which function it is.
result = DJAlgorithm.simulate(some_function)

# Print the result.
print(result["result"])
```
