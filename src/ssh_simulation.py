"""
SSH Model Simulation
Author: Ayush Kumar
Date: Dec 2025
Description: Numerical diagonalization of the Su-Schrieffer-Heeger Hamiltonian 
to observe the topological phase transition and zero-energy edge modes.
"""

import numpy as np
import matplotlib.pyplot as plt

def get_hamiltonian(N, v, w):
    """
    Constructs the SSH Hamiltonian for a chain with N unit cells (2N sites).
    v: intra-cell hopping (A-B)
    w: inter-cell hopping (B-A)
    """
    dim = 2 * N
    H = np.zeros((dim, dim))
    
    # Constructing the matrix elements
    # logic: site i connects to i+1 with alternating strengths v and w
    for i in range(dim - 1):
        if i % 2 == 0:
            # Inside the unit cell (A -> B)
            H[i, i+1] = v
            H[i+1, i] = v
        else:
            # Between unit cells (B -> A of next cell)
            H[i, i+1] = w
            H[i+1, i] = w
            
    return H

def check_hermiticity(H):
    # Sanity check: Hamiltonian must be Hermitian for real eigenvalues
    return np.allclose(H, H.T.conj())

def main():
    # --- System Parameters ---
    N = 20          # Number of unit cells
    v = 1.0         # Hopping strength v (fixed)
    w_range = np.linspace(0, 2.5, 100) # We sweep w from 0 to 2.5v
    
    print(f"Simulating SSH chain with {2*N} sites...")
    
    eigenvalues = []
    
    for w in w_range:
        H = get_hamiltonian(N, v, w)
        
        # Physics check
        if not check_hermiticity(H):
            raise ValueError("Error: Matrix is not Hermitian!")
            
        # Diagonalize
        evals, _ = np.linalg.eigh(H)
        eigenvalues.append(evals)
        
    eigenvalues = np.array(eigenvalues)
    
    # --- Plotting the Spectrum ---
    plt.figure(figsize=(10, 6))
    
    # Plotting all energy levels
    for i in range(2*N):
        plt.plot(w_range, eigenvalues[:, i], 'b.', markersize=1.2)
        
    # Visual markers for phase transition
    plt.axvline(1.0, color='black', linestyle='--', alpha=0.6, label='Transition ($w=v$)')
    plt.axhline(0, color='red', linestyle=':', alpha=0.5)
    
    plt.xlabel('Inter-cell hopping $w$ (units of $v$)', fontsize=12)
    plt.ylabel('Energy $E/v$', fontsize=12)
    plt.title(f'SSH Model Spectrum (N={N} Unit Cells)', fontsize=14)
    plt.text(0.2, 0.5, "Trivial Phase\n(Insulator)", fontsize=10, ha='center', color='gray')
    plt.text(2.2, 0.5, "Topological Phase\n(Edge States)", fontsize=10, ha='center', color='red')
    
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('ssh_spectrum.png', dpi=300)
    print("Simulation complete. Plot saved as 'ssh_spectrum.png'")
    plt.show()

if __name__ == "__main__":
    main()