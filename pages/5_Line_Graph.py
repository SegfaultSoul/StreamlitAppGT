import os

import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from utils import lab_header, get_source_code, header, setup_page, draw_graph, adjacency_matrix_input, layout_control, footer

setup_page("Experiment 5: Line Graph")

lab_header()

# Data from JSON
aim = "<b>Aim:</b> Convert the original graph into its line graph, where each edge of the original graph becomes a vertex in the new graph, and adjacency is defined by shared endpoints in the original graph."

header("Line Graph", aim)
sc = get_source_code("Expt 5")

theory = r"""
<div class="theory-card">

The concept of a line graph, often denoted as L(G), serves as a fundamental transformation in structural analysis where the roles of vertices and edges are systematically shifted. In this framework, the vertex set of the line graph, V(L(G)), is defined as being in one-to-one correspondence with the edge set of the original graph, E(G). This means that every edge present in the initial graph is represented as a distinct node within the resulting line graph. The core relationship that dictates the topology of L(G) is the adjacency between these new vertices. Two vertices in the line graph are considered adjacent if and only if the two edges they represent in the original graph G share a common endpoint. Essentially, the line graph captures the connectivity and incidence of the edges within the original structure, translating edge-to-vertex incidence into vertex-to-vertex adjacency.

Mathematical definitions within the field further clarify that if an edge e in G is incident with vertices u and v, the degree of the corresponding vertex in L(G) is determined by the degrees of u and v in the original graph. Specifically, the degree of a vertex in L(G) representing edge $uv$ is calculated as 
$d_G(u)$ + $d_G(v)$ - 2

as the edge $uv$ itself is subtracted from the count of edges incident to its endpoints. This transformation preserves certain structural properties; for instance, the line graph of a cycle graph $C_n$ is isomorphic to the cycle graph itself, while the line graph of a path graph $P_n$ results in a path graph P$n-1$. This mapping is crucial for understanding dualities in graph theory, where problems related to edges in an original graph, such as edge coloring or matching, can be re-framed as vertex-related problems within the line graph context.

### Algorithm
The algorithmic construction of a line graph follows a rigorous sequence of set operations and adjacency evaluations to ensure the structural integrity of the transformation. The process begins with an exhaustive listing of all edges in the original graph G, which serves as the foundational data for building the new vertex set. Upon initializing an empty graph L(G), a vertex is instantiated for every edge identified in G. This creates a vacant structure where the total number of nodes in L(G) is exactly equal to the cardinality of the edge set E(G). This mapping ensures that every edge-based relationship from the source graph is eligible for representation in the derived graph.

Once the vertex set is established, the algorithm proceeds to the critical phase of defining connectivity. This is achieved by performing a pairwise comparison of all original edges in G. For every pair of edges, the algorithm performs an incidence check to determine if they are incident to a common vertex in the original graph. If a shared vertex is found, it signifies that the two edges are adjacent in G, and consequently, a new edge must be drawn between their representative vertices in L(G). By systematically evaluating every possible pair of edges, the algorithm accurately translates the physical intersections of the original graph into the logical adjacencies of the line graph. The resulting adjacency matrix or list for L(G) provides a complete and formal representation of the original graph's edge-connectivity.
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
        [0, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 0, 0],
        [1, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0]
    ]
    G, matrix = adjacency_matrix_input(default_matrix, key="expt5")
    pos_g = layout_control(G, key="expt5")
    
    LG = nx.line_graph(G)
    pos_lg = nx.spring_layout(LG, seed=42)
    
    col1, col2 = st.columns(2)
    
    with col1:
        draw_graph(G, pos_g, title="Original Graph $G$")
        
    with col2:
        draw_graph(LG, pos_lg, title="Line Graph $L(G)$")
        
    st.markdown("###  Transformation Analysis")
    st.write(f"**Original Graph**: {G.number_of_nodes()} Nodes, {G.number_of_edges()} Edges")
    st.write(f"**Line Graph**: {LG.number_of_nodes()} Nodes, {LG.number_of_edges()} Edges")
    
    if LG.number_of_nodes() > 0:
        st.markdown("**Edge Mapping Table**")
        mapping_data = []
        for i, edge in enumerate(G.edges()):
            u, v = edge
            deg_lg = G.degree(u) + G.degree(v) - 2
            mapping_data.append({"Edge in G": f"({u}, {v})", "Vertex in L(G)": i, "Degree in L(G)": deg_lg})
        st.table(pd.DataFrame(mapping_data))

footer()
