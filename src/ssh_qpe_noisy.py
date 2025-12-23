"""
SSH Model: Robustness Against Noise (Completes All 3 Tasks)
Author: Ayush Kumar
"""

import os
import sys
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import PauliEvolutionGate, PhaseEstimation
from qiskit.synthesis import LieTrotter
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# Ensure we can import from the local src/ directory where ssh_quantum.py lives
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from ssh_quantum import build_qubit_hamiltonian

def run_noisy_simulation():
    print("--- Final Task: Robustness Against Depolarizing Noise ---")
    
    # --- 1. SETUP ---
    N = 2         # 4 System Qubits
    v = 0.1       # Small hopping
    w = 1.5       # Large hopping (Deep Topological Phase)
    
    num_eval_qubits = 6   # Lowered slightly for speed
    time = 20.0           # Long evolution to resolve small energies
    
    # Build Hamiltonian
    H = build_qubit_hamiltonian(N, v, w)
    
    # --- 2. PREPARE THE "EDGE" STATE (THE FIX) ---
    print("Initializing system with 1 electron at the edge...")
    
    # Construct QPE Circuit
    synthesis = LieTrotter(reps=2)
    U_gate = PauliEvolutionGate(H, time=time, synthesis=synthesis)
    qpe = PhaseEstimation(num_eval_qubits, U_gate)
    
    qc = QuantumCircuit(qpe.num_qubits, num_eval_qubits)
    
    # Apply X to the first system qubit to create an electron |...001>
    qc.x(num_eval_qubits) 
    
    qc.append(qpe, range(qpe.num_qubits))
    qc.measure(range(num_eval_qubits), range(num_eval_qubits))
    
    # --- 3. ADD NOISE (THE FINAL TASK) ---
    print("\nSimulating NISQ Device Noise (2% Depolarizing)...")
    
    noise_model = NoiseModel()
    error_prob = 0.02  # 2% error rate
    
    # Add error to gates
    error_gate1 = depolarizing_error(error_prob, 1)
    error_gate2 = depolarizing_error(error_prob, 2)
    noise_model.add_all_qubit_quantum_error(error_gate1, ["u1", "u2", "u3", "x", "h"])
    noise_model.add_all_qubit_quantum_error(error_gate2, ["cx"])
    
    # --- 4. RUN SIMULATION ---
    backend = AerSimulator()
    qc_transpiled = transpile(qc, backend=backend)
    
    # Run Noisy
    job_noisy = backend.run(qc_transpiled, noise_model=noise_model, shots=4096)
    counts_noisy = job_noisy.result().get_counts()
    
    # --- 5. ANALYZE RESULTS ---
    print("\n[Noisy Results] dominant measurements:")
    print(f"{'Energy':<10} | {'Count':<6}")
    print("-" * 20)
    
    sorted_counts = sorted(counts_noisy.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for bitstring, count in sorted_counts:
        # Convert to Energy
        decimal = int(bitstring, 2)
        phase = decimal / (2**num_eval_qubits)
        if phase > 0.5: phase -= 1.0
        energy = phase * (2 * np.pi) / time
        
        print(f"{energy:.4f}     | {count}")

    print(f"\nObservation: With {error_prob*100}% noise, the peak spreads out.")

if __name__ == "__main__":
    run_noisy_simulation()