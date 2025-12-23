"""
SSH Model: High-Precision Quantum Phase Estimation (QPE)
Author: Ayush Kumar
Method: Jordan-Wigner + Trotterization + QPE (8 Evaluation Qubits)
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import PauliEvolutionGate, PhaseEstimation
from qiskit.synthesis import LieTrotter
from qiskit_aer import AerSimulator

# Import the general Hamiltonian builder from your other file
# Make sure ssh_quantum.py is in the same folder (src/)
from ssh_quantum import build_qubit_hamiltonian

def run_precision_qpe():
    print("--- Starting High-Resolution QPE Simulation ---")
    
    # --- 1. SETUP PARAMETERS ---
    N = 2         # 2 Unit cells = 4 Sites (System Qubits)
    v = 0.5       # Intracell hopping
    w = 1.5       # Intercell hopping (Topological Phase: w > v)
    
    # Precision Settings
    num_eval_qubits = 8   # 2^8 = 256 energy bins. (Much sharper resolution)
    trotter_steps = 1     # Keep low for speed, increase to 2-3 for accuracy if needed
    time = 10.0           # Evolution time t. 
                          # Important: Energy = (Phase * 2π) / t
                          # Larger t zooms in on small energy differences (like near E=0)
    
    print(f"System: N={N} ({2*N} Qubits) + {num_eval_qubits} Eval Qubits = {2*N + num_eval_qubits} Total Qubits")
    print(f"Physics: v={v}, w={w} (Topological Phase)")
    
    # --- 2. BUILD HAMILTONIAN & OPERATOR ---
    H = build_qubit_hamiltonian(N, v, w)
    
    # Calculate EXACT Classical Eigenvalues for comparison
    print("\n[Reference] Calculating Classical Eigenvalues...")
    matrix = H.to_matrix()
    exact_evals = np.linalg.eigvalsh(matrix)
    
    # We focus on the ones closest to zero (the edge states)
    # Filter for energies between -2 and 2 to reduce clutter
    print(f"True Energies (Target): {np.sort(exact_evals)[:4]}")

    # Create Time Evolution Operator U = exp(-iHt)
    synthesis = LieTrotter(reps=trotter_steps)
    U_gate = PauliEvolutionGate(H, time=time, synthesis=synthesis)
    
    # --- 3. BUILD CIRCUIT ---
    # Total Qubits = [Evaluation] + [System]
    # QPE automatically handles the layout
    # Use the correctly defined num_eval_qubits variable
    qpe = PhaseEstimation(num_eval_qubits, U_gate)
    
    # The circuit needs (Eval + System) qubits
    qc = QuantumCircuit(qpe.num_qubits, num_eval_qubits)
    
    # Initialization:
    # We leave system in |0000>. 
    # Ideally, we would prepare a specific state, but |0000> has overlap 
    # with multiple eigenstates, so we will see multiple peaks in the spectrum.
    
    qc.append(qpe, range(qpe.num_qubits))
    qc.measure(range(num_eval_qubits), range(num_eval_qubits))
    
    # --- 4. RUN SIMULATION ---
    print("\nRunning Quantum Simulation (Aer)...")
    backend = AerSimulator()
    # Transpile the circuit to a form that Aer supports, avoiding unsupported instructions
    qc_transpiled = transpile(qc, backend=backend)
    job = backend.run(qc_transpiled, shots=4096)  # High shots for clean peaks
    counts = job.result().get_counts()
    
    # --- 5. ANALYZE RESULTS ---
    print("\n[Results] Top Detected Energies:")
    print(f"{'Bitstring':<10} | {'Prob':<6} | {'Phase':<8} | {'Energy (Est)':<10} | {'Error'}")
    print("-" * 65)
    
    # Sort by most frequent measurements (peaks)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:6]
    
    for bitstring, count in sorted_counts:
        probability = count / 4096
        
        # 1. Convert Bitstring to Phase [0, 1)
        # Note: Qiskit's PhaseEstimation is Big-Endian in recent versions, 
        # but the bitstring readout is Little-Endian. 
        # Usually: int(bitstring, 2) / 2^n is the standard mapping.
        decimal = int(bitstring, 2)
        phase = decimal / (2**num_eval_qubits)
        
        # 2. Handle Negative Energies (Phase Wrapping)
        # Eigenvalues e^{-iEt}. If E is negative, phase wraps around 1.0.
        # If phase > 0.5, we interpret it as negative energy.
        if phase > 0.5:
             measured_phase = phase - 1.0
        else:
             measured_phase = phase
             
        # 3. Convert Phase to Energy: E = (Phase * 2π) / t
        energy_est = measured_phase * (2 * np.pi) / time
        
        # 4. Find nearest true eigenvalue to check accuracy
        nearest_true = min(exact_evals, key=lambda x: abs(x - energy_est))
        error = abs(energy_est - nearest_true)
        
        print(f"{bitstring:<10} | {probability:.3f}  | {measured_phase:.4f}   | {energy_est:.4f}       | {error:.4f}")

if __name__ == "__main__":
    run_precision_qpe()