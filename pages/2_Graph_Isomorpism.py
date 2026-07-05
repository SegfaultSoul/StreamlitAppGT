import os

import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from utils import lab_header, get_source_code, header, setup_page, draw_graph, adjacency_matrix_input, layout_control, footer

setup_page("Experiment 2: Graph Isomorphism")

lab_header()

# Data from JSON
aim = "<b>Aim:</b> To implement isomorphism verification in order to compare structural equivalence between two graphs."

header("Graph Isomorphism", aim)
sc = get_source_code("Expt 2")

theory = r"""
<div class="theory-card">

### Isomorphism
Isomorphism in graph theory refers to a structural equivalence between two graphs G1=(V1, E1) and G2=(V2, E2). Formally, G1 and G2 are isomorphic, denoted as G1\congG2, if there exists a bijection f:V1$\to$V2 such that any two vertices u and v are adjacent in G1 if and only if f(u) and f(v) are adjacent in G2. This means that while the two graphs may be drawn differently or have different vertex labels, their underlying connectivity and topological properties are identical. In essence, an isomorphism is a "relabeling" of vertices that preserves all adjacency and non-adjacency relationships.

For two graphs to be considered isomorphic, they must satisfy several necessary conditions known as graph invariants. These invariants include having the same number of vertices 
|V1| = |V2|, the same number of edges |E1| = |E2|, and identical degree sequences when sorted. However, these conditions are not always sufficient to prove isomorphism; for example, two graphs might share the same degree sequence but possess different internal structures, such as different cycle lengths or connectivity patterns. Therefore, proving isomorphism often requires demonstrating that a specific mapping preserves the entire edge set E across both vertex sets.

### General Algorithm to Implement Isomorphism
The general algorithm for implementing isomorphism verification typically employs a series of heuristic filters designed to quickly identify non-isomorphic graphs before attempting the computationally intensive task of finding a vertex-to-vertex mapping. Since the Graph Isomorphism problem is computationally complex, the algorithm first checks basic structural properties that must remain invariant under any isomorphism. If any of these initial checks fail, we can conclude that G1\congG2 without proceeding further, which is crucial for efficiency when working with large datasets in libraries like NetworkX.

If the basic invariants match, the algorithm moves toward a more exhaustive structural comparison and the construction of a bijection function. The specific steps involved in a general verification process are as follows:

Step 1: Compare the total number of vertices and the total number of edges. If |V1|=|V2| or |E1|=|E0|, the graphs are not isomorphic.

Step 2: Compute the degree of every vertex and compare the sorted degree sequences of both graphs. They must be identical.

Step 3: Compare the number of connected components in both graphs and ensure that the size of each corresponding component matches.

Step 4: Compute the length and count of cycles within the graphs. Isomorphic graphs must have the same number of cycles of any given length k (e.g., both must have the same number of triangles).

Step 5: Construct a candidate bijection function f:V1$\to$V2. The algorithm must verify that for every pair (u, v) \in E1, the pair (f(u), f(v)) exists in E2. If such a mapping is successfully found, the graphs are confirmed to be isomorphic.
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
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("Graph $G_1$")
        default_matrix_g1 = [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0]
        ]
        G1, matrix1 = adjacency_matrix_input(default_matrix_g1, key="g1")
        pos1 = layout_control(G1, key="g1")

    with col_input2:
        st.subheader("Graph $G_2$")
        default_matrix_g2 = [
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0]
        ]
        G2, matrix2 = adjacency_matrix_input(default_matrix_g2, key="g2")
        pos2 = layout_control(G2, key="g2")
    
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        draw_graph(G1, pos1, title="Graph $G_1$")
        
    with col_viz2:
        draw_graph(G2, pos2, title="Graph $G_2$")
        
    st.markdown("###  Isomorphism Analysis")
    
    v1, v2 = G1.number_of_nodes(), G2.number_of_nodes()
    e1, e2 = G1.number_of_edges(), G2.number_of_edges()
    d1 = sorted([d for n, d in G1.degree()], reverse=True)
    d2 = sorted([d for n, d in G2.degree()], reverse=True)
    
    is_iso = nx.is_isomorphic(G1, G2)
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.write(f"**Vertex Count Match**: {'Yes' if v1 == v2 else 'No'} ({v1} vs {v2})")
        st.write(f"**Edge Count Match**: {'Yes' if e1 == e2 else 'No'} ({e1} vs {e2})")
    with res_col2:
        st.write(f"**Degree Sequence Match**: {'Yes' if d1 == d2 else 'No'}")
        st.markdown(f"**Is Isomorphic**: {'Yes (TRUE)' if is_iso else 'No (FALSE)'}")
    
    if is_iso:
        nm = nx.isomorphism.GraphMatcher(G1, G2)
        if nm.is_isomorphic():
            st.success(f"**Found Mapping**: {nm.mapping}")

footer()
