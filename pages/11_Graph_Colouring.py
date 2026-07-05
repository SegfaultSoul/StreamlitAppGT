import os

import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from utils import lab_header, get_source_code, header, setup_page, draw_graph, adjacency_matrix_input, layout_control, footer

setup_page("Experiment 11: Graph Colouring")

lab_header()

# Data from JSON
aim = "<b>Aim:</b> To implement the greedy graph colouring algorithm, that assigns colours to the vertices, such that no two adjacent vertices share the same colour, with minimal chromatic number."

header("Graph Colouring", aim)
sc = get_source_code("Expt 11")

theory = r"""
<div class="theory-card">

Graph colouring is a fundamental problem in graph theory that involves assigning labels traditionally referred to as "colours" to the components of a graph subject to specific constraints. The most common variation is vertex colouring, which requires assigning a colour to each vertex of a graph G such that no two adjacent vertices (vertices directly connected by an edge) share the same colour. A colouring that satisfies this condition is known as a proper vertex colouring.

The minimum number of colours required to achieve a proper vertex colouring for a given graph G is called the chromatic number of the graph, denoted by the symbol $\chi(G)$ (chi of G). If a graph can be coloured using k colours, it is termed k-colourable. Graph colouring has numerous practical applications, including scheduling, register allocation in compilers, frequency assignment in mobile networks, and solving Sudoku puzzles.

Determining the exact chromatic number for an arbitrary graph is known to be an NP-complete problem. Because there is no known efficient (polynomial-time) algorithm to find the absolute minimum chromatic number, computer science relies on heuristic approximations. The most common heuristic is the Greedy Graph Colouring Algorithm.

The greedy approach does not guarantee the optimal minimal chromatic number ($\chi(G)$) for every arbitrary sequence of vertices. However, it operates quickly and guarantees that it will never use more than $\Delta(G)$ + 1 colours, where $\Delta(G)$ is the maximum degree (number of incident edges) of any single vertex in the graph. The efficiency and final chromatic count of the greedy algorithm heavily depend on the order in which the vertices are processed; ordering vertices in descending order of their degrees (as seen in the Welsh-Powell algorithm) often yields a result much closer to the true minimum.

### The Greedy Graph Colouring Algorithm
The algorithm operates by picking vertices one by one and assigning the smallest possible colour index (e.g., Colour 1, Colour 2, etc.) that does not create a conflict with its already-coloured neighbors.

Step 1: Vertex Ordering: List all the vertices of the graph G in a specific sequence: $v_{1}$, $v_{2}$, ..., $v_{n}$. (This sequence can be arbitrary, or sorted based on vertex degrees).
Step 2: Initialization: Assign the first available colour (e.g., Colour 1) to the first vertex in the sequence, $v_{1}$.

Step 3: Iteration: For each remaining vertex $v_{i}$ in the sequence (where i ranges from 2 to n), perform the following checks:

Step 4: Conflict Checking: Examine all the adjacent vertices (neighbors) of $v_{i}$. Make a note of all the colours that have already been assigned to these neighboring vertices.

Step 5: Colour Assignment: Assign $v_{i}$ the smallest possible colour index (starting from 1, 2, 3...) that is not present in the list of its neighbors' colours. If all currently used colours are taken by neighbors, introduce a new, higher colour index.

Step 6: Termination: The algorithm stops when all n vertices have been successfully assigned a colour.
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
            # Images are now in the app's images folder, located relative to the app directory itself
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            st.image(os.path.join(base_dir, "images", img_path))
            
    elif sc["output"] and sc["output"] != "No output found.":
        st.subheader("Experiment Output")
        st.code(sc["output"])
with lab_tab:
    default_matrix = [
        [0, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [1, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 1, 0, 1, 1],
        [1, 1, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 1, 1, 0]
    ]
    G, matrix = adjacency_matrix_input(default_matrix, key="expt11")
    pos = layout_control(G, key="expt11")
    
    strategy = st.selectbox("Colouring Strategy (Ordering)", ["largest_first", "saturation_largest_first", "random_sequential", "smallest_last", "independent_set"])
    
    # Perform Colouring
    colour_map = nx.coloring.greedy_color(G, strategy=strategy)
    
    # Convert colour indices to hex colours
    # Using a professional color palette
    palette = ["#4f46e5", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#06b6d4", "#f97316"]
    node_colors = [palette[colour_map[node] % len(palette)] for node in G.nodes()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        draw_graph(G, pos, title="Greedy Graph Colouring", node_colors=node_colors)
        
    with col2:
        st.subheader("Colouring Analysis")
        num_colors = len(set(colour_map.values()))
        st.markdown(f"**Chromatic Number (Heuristic)**: ### {num_colors}")
        st.write(f"**Max Degree ($\\\\Delta$)**: {max([d for n, d in G.degree()]) if G.number_of_nodes() > 0 else 0}")
        st.write(f"**Bound ($\\\\Delta + 1$)**: {max([d for n, d in G.degree()]) + 1 if G.number_of_nodes() > 0 else 1}")
        
        st.markdown("**Vertex Assignments**")
        assignments = [{"Vertex": f"V{n}", "Color Index": c, "Hex": palette[c % len(palette)]} for n, c in sorted(colour_map.items())]
        st.table(pd.DataFrame(assignments))

footer()
