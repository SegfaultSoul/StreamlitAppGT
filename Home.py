import streamlit as st
from utils import setup_page, footer, header

setup_page("Graph Theory Lab - Home")

header()

st.markdown("""
Welcome to the interactive **Graph Theory Lab**. This application provides a comprehensive platform to explore, visualize, and experiment with various graph-theoretical concepts and algorithms.

### Syllabus and Experiments
This mini-project covers 11 core experiments as part of the Graph Theory curriculum:

1.  **Basic Graphs**: Implementation of fundamental graph types ($N_n, K_n, C_n, P_n, W_n, K_{m,n}$).
2.  **Isomorphism**: Verifying structural equivalence between two graphs using invariants and mappings.
3.  **Subgraphs**: Generating induced, spanning, and edge-deleted subgraphs.
4.  **Degree Sequence**: Havel-Hakimi theorem and graph construction from degree sequences.
5.  **Line Graph**: Converting graphs to their line graph counterparts.
6.  **Minimum Spanning Tree (MST)**: Implementing Kruskal's algorithm for optimal connectivity.
7.  **Shortest Path**: Dijkstra's algorithm for weighted graphs.
8.  **Walks, Trails, and Paths**: Exploring connectivity structures and cycle classifications.
9.  **Eulerian Graphs**: Fleury's algorithm and Eulerian circuit/trail verification.
10. **Hamiltonian Graphs**: Closure algorithm and exhaustive search for Hamiltonian cycles.
11. **Graph Coloring**: Greedy vertex coloring and chromatic number estimation.

---

### Key Features
- **Adjacency Matrix Input**: Direct control over graph topology using matrix representations.
- **Custom Positioning**: Explicitly control node placement using $(x, y)$ coordinates.
- **Dynamic Visualization**: Instant updates and visual highlights for algorithm results.
- **Comprehensive Theory**: Mathematical definitions and formulas rendered in LaTeX.

### Getting Started
Select an experiment from the sidebar to begin exploring. Every experiment comes with a functional default example.
""")
st.markdown('</div>', unsafe_allow_html=True)

footer()
