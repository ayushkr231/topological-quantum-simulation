"""
Quantum Simulation of SSH Model
Author: Ayush Kumar
Method: Jordan-Wigner Mapping + SparsePauliOp
"""

import numpy as np
from qiskit.quantum_info import SparsePauliOp

def build_qubit_hamiltonian(N, v, w):
    """
    Maps the SSH Fermi-Hubbard Hamiltonian to Qubit Operators using Jordan-Wigner.
    
    Args:
        N (int): Number of unit cells (Total sites = 2*N)
        v (float): Intracell hopping
        w (float): Intercell hopping
        
    Returns:
        SparsePauliOp: The Hamiltonian expressed as Pauli strings (Sum of X and Y terms).
    """
    num_sites = 2 * N
    terms = []
    
    # We iterate through bonds to create hopping terms
    # Hopping term c^dag_i c_{i+1} + h.c. becomes 0.5 * (X_i X_{i+1} + Y_i Y_{i+1})
    
    for i in range(num_sites - 1):
        # Determine hopping strength (v or w)
        strength = v if (i % 2 == 0) else w
        
        # Construct Pauli String "II...XX...II" and "II...YY...II"
        # Note: Qiskit reads qubits from right to left (Little Endian). 
        # But SparsePauliOp.from_sparse_list is easier to use for indexing.
        
        # X_i X_{i+1} term
        # Each entry in the sparse list is (pauli_string, [qubit_indices], coefficient)
        terms.append(("XX", [i, i+1], strength / 2.0))
        
        # Y_i Y_{i+1} term
        terms.append(("YY", [i, i+1], strength / 2.0))
    
    # Create the Operator
    # Qiskit signature (as used here): from_sparse_list(pauli_list, num_qubits)
    # where each element of pauli_list is (label, qubit_indices, coeff).
    H_qubit = SparsePauliOp.from_sparse_list(terms, num_sites)
    
    return H_qubit

if __name__ == "__main__":
    # --- TEST 1: Sanity Check ---
    print("Building Hamiltonian for N=2 (4 Qubits)...")
    H = build_qubit_hamiltonian(N=2, v=1.0, w=0.5)
    print(f"Number of Pauli Terms: {len(H)}")
    print("\nFirst few terms:")
    print(H)
    
    # --- TEST 2: Exact Diagonalization via Qiskit (Verification) ---
    # Before running QPE, we check if the Qubit Hamiltonian gives the correct eigenvalues 
    # using exact matrix math (not a quantum simulation yet).
    from qiskit.quantum_info import Statevector
    
    # Convert operator to matrix and find eigenvalues
    matrix = H.to_matrix()
    evals = np.linalg.eigvalsh(matrix)
    
    print("\nTarget Eigenvalues (Lowest 4):")
    print(np.sort(evals)[:4])