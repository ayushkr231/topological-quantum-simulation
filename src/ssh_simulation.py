import numpy as np
import matplotlib.pyplot as plt

def construct_ssh_hamiltonian(N, v, w):
    """
    Constructs the real-space Hamiltonian for a finite SSH chain.
    
    Args:
        N (int): Number of unit cells (Total sites = 2*N)
        v (float): Intracell hopping (A-B within cell)
        w (float): Intercell hopping (B-A between cells)
        
    Returns:
        H (ndarray): The 2N x 2N Hamiltonian matrix
    """
    num_sites = 2 * N
    H = np.zeros((num_sites, num_sites))
    
    # We loop through the sites 0 to 2N-2
    # Site i connects to site i+1
    for i in range(num_sites - 1):
        if i % 2 == 0:
            # Even i (0, 2, 4...) is an A site. 
            # Connection A -> B is INTRA-cell (v)
            H[i, i+1] = v
            H[i+1, i] = v
        else:
            # Odd i (1, 3, 5...) is a B site.
            # Connection B -> A is INTER-cell (w)
            H[i, i+1] = w
            H[i+1, i] = w
            
    # Note: No Periodic Boundary Conditions (Open Chain).
    # This is crucial to see Edge States!
    return H

def simulate_phase_transition():
    print("Running Simulation...")
    
    # --- PARAMETERS ---
    N = 20        # 20 Unit cells = 40 Atoms
    v = 1.0       # Fix intracell hopping to 1.0 (Energy unit)
    
    # Sweep intercell hopping w from 0 to 2.5
    # w < 1: Trivial
    # w = 1: Phase Transition
    # w > 1: Topological
    w_values = np.linspace(0, 2.5, 100)
    
    eigenvalues = []
    
    # --- MAIN LOOP ---
    for w in w_values:
        # 1. Build Matrix
        H = construct_ssh_hamiltonian(N, v, w)
        
        # 2. Diagonalize (The Solver)
        # 'eigh' is optimized for Hermitian matrices
        evals, _ = np.linalg.eigh(H)
        
        # 3. Store Results
        eigenvalues.append(evals)
        
    eigenvalues = np.array(eigenvalues)
    
    # --- PLOTTING ---
    plt.figure(figsize=(10, 6))
    
    # We plot all 2N energy levels for each w
    for i in range(2*N):
        # Plot bulk states in blue
        plt.plot(w_values, eigenvalues[:, i], 'b.', markersize=1.5, alpha=0.4)

    plt.xlabel(r'Intercell Hopping Ratio $w/v$', fontsize=12)
    plt.ylabel(r'Energy $E/v$', fontsize=12)
    plt.title(r'SSH Model: Topological Phase Transition', fontsize=14)
    
    # Add visual guides for the Physics
    plt.axvline(1.0, color='k', linestyle='--', label='Transition ($w=v$)')
    plt.axhline(0, color='r', linestyle=':', alpha=0.5)
    
    # Annotations
    plt.text(0.5, 0.05, 'Trivial Phase\n(Insulator)', ha='center', color='black', fontsize=10)
    plt.text(2.0, 0.05, 'Topological Phase\n(Edge States)', ha='center', color='red', fontsize=10)
    
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    simulate_phase_transition()