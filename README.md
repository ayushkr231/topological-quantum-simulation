[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://topological-quantum-simulation-bkws4kw33mrwn8jrcpm9r4.streamlit.app/)

**Author:** Ayush Kumar
**Affiliation:** IISER Bhopal / IIT Madras

### Overview
This project simulates the topological phase transition in a 1D dimerized lattice (SSH Model). The goal is to verify the **Bulk-Boundary Correspondence** numerically and investigate the robustness of edge states on **NISQ (Noisy Intermediate-Scale Quantum)** devices.

I employed a hybrid approach:
1.  **Classical Simulation:** Exact diagonalization to establish theoretical bounds.
2.  **Quantum Simulation:** Implemented on **Qiskit** using Trotterization and Quantum Phase Estimation (QPE) to benchmark hardware stability.

### The Physics
The Hamiltonian for the chain is given by:

$$H = \sum_{n} (v |n,A\rangle\langle n,B| + w |n,B\rangle\langle n+1,A| + h.c.)$$

where:
- $v$: Intracell hopping amplitude.
- $w$: Intercell hopping amplitude.
- $h.c.$: Hermitian conjugate (adds reverse hopping processes).

**Phase Diagram:**
1.  **Trivial Phase ($v > w$):** The bulk has an energy gap, and there are no states at $E=0$.
2.  **Topological Phase ($w > v$):** The bulk gap remains open, but two degenerate states appear at exactly $E=0$. These are localized at the edges of the chain.

---

### Part 1: Classical Simulation Results
Running the simulation for $N=20$ unit cells yields the following spectrum:

![Spectrum Plot](ssh_spectrum.png)
*(Fig 1: As $w$ crosses $v$, the gap closes and reopens, leaving behind edge modes at zero energy.)*

---

### Part 2: Quantum Simulation (Qiskit)
I benchmarked the **Quantum Phase Estimation (QPE)** algorithm to detect these topological phases on a quantum computer.

**Method:**
- Mapped the Hamiltonian to qubits using **Jordan-Wigner transformation**.
- Implemented first-order **Trotterization** for time evolution ($U = e^{-iHt}$).
- Used 8 evaluation qubits for high-precision energy detection.

**Calibration Result (Vacuum State):**
The algorithm successfully recovered the vacuum energy ($E=0$) with **$10^{-4}$ precision**, validating the Trotter-Suzuki decomposition.


[Results] Top Detected Energies (Vacuum):
Bitstring  | Prob   | Phase    | Energy (Est) | Error
-------------------------------------------------------
00000000   | 1.000  | 0.0000   | 0.0000       | 0.0000

---

### Part 3: Noise Robustness Study
I investigated the stability of the topological edge states on **NISQ devices** by introducing depolarizing noise channels.

**Experiment:**
- **Initial State:** Single electron localized at the edge ($|1000\rangle$).
- **Noise Model:** 2% Depolarizing Error on all gates (simulating current hardware limits).
- **Result:** The zero-energy peak, which is sharp in the ideal case, completely decoheres into a flat spectrum.

```text
[Noisy Results] dominant measurements:
Energy     | Count 
--------------------
-0.0147    | 88
 0.0638    | 85
-0.0295    | 82
-0.0442    | 80
 0.1276    | 77
