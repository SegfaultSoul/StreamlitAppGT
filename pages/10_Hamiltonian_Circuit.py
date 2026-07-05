import os

import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from utils import lab_header, get_source_code, header, setup_page, draw_graph, adjacency_matrix_input, layout_control, footer

setup_page("Experiment 10: Hamiltonian Circuit")

lab_header()

# Data from JSON
aim = "<b>Aim:</b> To implement a method that determines whether a graph contains a hamiltonian circuit that is a cycle that visits every vertex exactly once except the starting vertex."

header("Hamiltonian Circuit", aim)
sc = get_source_code("Expt 10")

theory = r"""
<div class="theory-card">

A Hamiltonian circuit (or Hamiltonian cycle) is a closed loop in a graph G that visits every vertex exactly once and returns to the starting vertex. A graph that possesses such a circuit is called a Hamiltonian graph.

While the concept is simple, the fundamental characterization of these graphs is significantly more complex than that of Eulerian graphs. There is no simple necessary and sufficient condition to determine if a general graph is Hamiltonian, and the decision problem is known to be NP-complete.

Because there is no absolute test for general graphs, graph theory relies on necessary conditions and sufficient conditions to analyze them:

### Necessary Condition (Connectivity and Toughness)
If a graph G is Hamiltonian, then for any non-empty proper subset of vertices S \subset V, the number of connected components of the graph G - S cannot exceed the number of vertices in S. Mathematically, $c(G - S)$ $\le$ |S|. If removing a set of vertices breaks the graph into more pieces than the number of vertices removed, the graph cannot be Hamiltonian.

### Sufficient Conditions (Degrees of Vertices)
Dirac’s Theorem (1952): If G is a simple graph with $n \ge 3$ vertices, and the degree of every vertex is at least n/2, then G is Hamiltonian.

Ore’s Theorem (1960): If G is a simple graph with $n \ge 3$ vertices, and for every pair of non-adjacent vertices u and v, the sum of their degrees is d(u) + $d(v)$ $\ge$ n, then G is Hamiltonian.

### Algorithms for Hamiltonian Circuits
Because the problem is NP-complete, two algorithmic approaches are generally used: one for testing sufficiency (Closure) and one for exhaustive searching (Backtracking).

### The Closure Algorithm
The closure of a graph helps determine if it meets the sufficient conditions for a Hamiltonian circuit. A graph is Hamiltonian if and only if its closure is Hamiltonian.

Step 1: Initialization: Let G be a graph with n vertices. Set the current graph C = G.

Step 2: Search for Non-adjacent Pairs: Scan the graph C for any pair of non-adjacent vertices, u and v, such that their combined degree is d(u) + $d(v)$ $\ge$ n.

Step 3: Edge Addition: If such a pair exists, add a new edge $uv$ to C to connect them. Update the degrees of u and v.

Step 4: Iteration and Termination: Repeat Steps 2 and 3 until no such pairs of non-adjacent vertices can be found. The resulting graph is the closure, denoted as C(G).
</div>
"""

doc_tab, code_tab, lab_tab = st.tabs(["Documentation", "Source Code", "Interactive Laboratory"])

with doc_tab:
    st.markdown(theory, unsafe_allow_html=True)


with code_tab:
    st.subheader("Implementation Detail")
    st.code(sc["code"], language="python")
    
    if sc.get("images"):
        st.subheader("Experiment Output")
        for img_path in sc["images"]:
            # Images are relative to project root, so we prepend '../' since pages are in subfolder
            st.image(os.path.join("..", img_path))
            
    elif sc["output"] and sc["output"] != "No output found.":
        st.subheader("Experiment Output")
        st.code(sc["output"])
with lab_tab:
    default_matrix = [
        [0, 1, 0, 0, 1, 0],
        [1, 0, 1, 0, 1, 1],
        [0, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 1],
        [1, 1, 0, 1, 0, 1],
        [0, 1, 1, 1, 1, 0]
    ]
    G, matrix = adjacency_matrix_input(default_matrix, key="expt10")
    pos = layout_control(G, key="expt10")
    
    # Check for Hamiltonian Cycle using Backtracking from Docs
    def find_hamiltonian_circuit(G):
        total_nodes = len(G.nodes)
        if total_nodes == 0:
            return None
        start_node = list(G.nodes)[0]
        path = [start_node]
        def backtrack(current_node):
            if len(path) == total_nodes:
                if G.has_edge(current_node, start_node):
                    return path + [start_node]
                return None
            for neighbor in G.neighbors(current_node):
                if neighbor not in path:
                    path.append(neighbor)
                    result = backtrack(neighbor)
                    if result:
                        return result
                    path.pop()
            return None
        return backtrack(start_node)

    ham_cycle = find_hamiltonian_circuit(G)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if ham_cycle:
            edges = list(zip(ham_cycle, ham_cycle[1:]))
            draw_graph(G, pos, title="Hamiltonian Circuit Found", highlight_edges=edges)
        else:
            draw_graph(G, pos, title="No Hamiltonian Circuit Found")

    with col2:
        st.subheader("Hamiltonian Analysis")
        n = G.number_of_nodes()
        st.write(f"**Nodes (n)**: {n}")
        
        # Dirac's Check
        min_deg = min([d for n, d in G.degree()]) if n > 0 else 0
        dirac = min_deg >= n/2 if n >= 3 else False
        st.write(f"**Dirac's Condition ($\\delta \\ge n/2$)**: {'Yes' if dirac else 'No'} ({min_deg} vs {n/2})")
        
        # Ore's Check
        ore = True
        non_adj = []
        nodes = list(G.nodes())
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if not G.has_edge(nodes[i], nodes[j]):
                    sum_deg = G.degree(nodes[i]) + G.degree(nodes[j])
                    if sum_deg < n:
                        ore = False
                    non_adj.append((nodes[i], nodes[j], sum_deg))
        
        if n >= 3:
            st.write(rf"**Ore's Condition ($d(u)+d(v) \ge n$)**: {'Yes' if ore else 'No'}")
        
        if ham_cycle:
            st.success("**Hamiltonian Circuit**: " + rf" \rightarrow ".join([f"V{v}" for v in ham_cycle]))
        else:
            st.error("No Hamiltonian Circuit found using exhaustive search.")

footer()
