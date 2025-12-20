import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SSH Model Simulator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HEADER & INTRODUCTION ---
st.title("⚛️ Topological Phase Transition: SSH Model")
st.markdown("""
**Author:** Ayush Kumar (IISER Bhopal / IIT Madras)

This interactive dashboard simulates the **Su-Schrieffer-Heeger (SSH) Hamiltonian** for a 1D dimerized lattice. 
It demonstrates the **Bulk-Boundary Correspondence** by visualizing the emergence of zero-energy edge modes.
""")

# --- SIDEBAR: EXPERIMENTAL PARAMETERS ---
st.sidebar.header("🔬 Simulation Parameters")

with st.sidebar.expander("Lattice Configuration", expanded=True):
    N = st.slider("Unit Cells (N)", min_value=5, max_value=40, value=20, help="Total sites = 2N")
    st.caption(f"Total Sites: {2*N}")

with st.sidebar.expander("Hopping Amplitudes", expanded=True):
    v = st.slider("Intracell Hopping (v)", 0.1, 2.0, 1.0, step=0.1, help="Hopping within the unit cell (A-B)")
    w = st.slider("Intercell Hopping (w)", 0.0, 2.5, 0.5, step=0.05, help="Hopping between unit cells (B-A)")

st.sidebar.markdown("---")
st.sidebar.info(
    "**Theory Note:**\n"
    "- **Trivial Phase:** $w < v$\n"
    "- **Topological Phase:** $w > v$"
)

# --- PHYSICS ENGINE ---
def get_hamiltonian(N, v, w):
    """Generates the SSH Hamiltonian matrix."""
    dim = 2 * N
    H = np.zeros((dim, dim))
    for i in range(dim - 1):
        if i % 2 == 0:
            H[i, i+1] = v; H[i+1, i] = v # Intracell
        else:
            H[i, i+1] = w; H[i+1, i] = w # Intercell
    return H

# Perform Calculation
H = get_hamiltonian(N, v, w)
eigenvalues, eigenvectors = np.linalg.eigh(H)

# Identify Zero Modes (Smallest absolute energy)
# We sort by absolute energy to find the modes closest to E=0
sort_indices = np.argsort(np.abs(eigenvalues))
zero_modes_indices = sort_indices[:2] # Top 2 closest to zero
energy_gap = 2 * np.abs(eigenvalues[sort_indices[2]]) # Approx gap to next state

# --- DASHBOARD LAYOUT ---
col1, col2 = st.columns([1, 1])

# --- PANEL 1: ENERGY SPECTRUM ---
with col1:
    st.subheader("1. Energy Spectrum")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    
    # Plot eigenvalues
    sites = np.arange(2*N)
    ax1.plot(sites, eigenvalues, 'o-', color='navy', markersize=4, linewidth=0.8, label='Bulk States')
    
    # Highlight Zero Mode Energies
    if w > v:
        ax1.plot(sites[:2], eigenvalues[zero_modes_indices], 'ro', markersize=6, label='Edge Modes')
    
    ax1.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.set_ylabel(r"Energy ($E/v$)")
    ax1.set_xlabel("State Index")
    ax1.set_title(f"Band Structure (Gap $\Delta \\approx {energy_gap:.2f}v$)")
    ax1.legend(loc='upper left', fontsize=8)
    ax1.grid(True, alpha=0.2)
    st.pyplot(fig1)

    # Status Indicator
    if w > v:
        st.success(f"✅ **Topological Phase** ($w > v$)\n\nZero-energy edge modes present.")
    elif w < v:
        st.warning(f"⚠️ **Trivial Phase** ($w < v$)\n\nInsulating bulk, no zero modes.")
    else:
        st.error(f"⚡ **Phase Transition** ($w = v$)\n\nGap closes.")

# --- PANEL 2: WAVEFUNCTION LOCALIZATION ---
with col2:
    st.subheader("2. Edge State Localization")
    
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    
    if w > v:
        # Plot probability density |psi|^2 for the two zero modes
        for idx in zero_modes_indices:
            psi = eigenvectors[:, idx]
            prob_density = np.abs(psi)**2
            ax2.plot(np.arange(2*N), prob_density, '.-', label=f"E = {eigenvalues[idx]:.4f}")
            
        ax2.set_title("Wavefunction Probability Density $|\psi|^2$")
        ax2.set_xlabel("Lattice Site")
        ax2.legend()
        st.pyplot(fig2)
        st.caption("Note: The probability density is peaked at the boundaries (Site 0 and Site 2N).")
        
    else:
        # In trivial phase, just plot a bulk state to show it's delocalized
        mid_state_idx = sort_indices[N] # Pick a state in the middle of the band
        psi = eigenvectors[:, mid_state_idx]
        ax2.plot(np.arange(2*N), np.abs(psi)**2, 'g.-', label="Bulk State", alpha=0.6)
        ax2.set_title("Bulk State Density (Delocalized)")
        ax2.set_xlabel("Lattice Site")
        ax2.set_ylim(0, 0.5) # Fix scale to avoid jumping
        st.pyplot(fig2)
        st.caption("In the trivial phase, electrons are delocalized across the chain.")

# --- EXPANDER: THEORETICAL BACKGROUND ---
st.divider()
with st.expander("📚 Theoretical Background (Click to Expand)"):
    st.markdown("### The Hamiltonian")
    st.latex(r"H = \sum_{n} (v |n,A\rangle\langle n,B| + w |n,B\rangle\langle n+1,A| + h.c.)")
    
    st.markdown("""
    **Key Concepts:**
    1. **Chiral Symmetry:** The Hamiltonian anticommutes with the sublattice operator $\sigma_z$, ensuring the energy spectrum is symmetric around $E=0$.
    2. **Winding Number:** A topological invariant $\\nu$ which is 0 for $v>w$ and 1 for $w>v$.
    3. **Bulk-Boundary Correspondence:** The number of edge pairs equals the winding number.
    """)