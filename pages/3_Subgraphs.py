import os

import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from utils import lab_header, get_source_code, header, setup_page, draw_graph, adjacency_matrix_input, layout_control, footer

setup_page("Experiment 3: Subgraphs")

lab_header()

# Data from JSON
aim = "<b>Aim:</b> To implement generation of various subgraphs, such as induced subgraph, spanning subgraph, and edge deleted subgraphs."

header("Subgraphs", aim)
sc = get_source_code("Expt 3")

theory = r"""
<div class="theory-card">

### Subgraph
A subgraph H=(V', E') is a graph such that the vertex set V' is a subset of the vertex set V of a larger graph G, and the edge set E' is a subset of the edge set E of G, with the condition that every edge in E' must have its endpoints in V'. In simpler terms, a subgraph is formed by selecting a group of vertices and edges from a parent graph without adding any new connections that didn't exist in the original structure. This concept is fundamental for breaking down complex networks into smaller, more manageable components for localized analysis.

The relationship between a graph G and its subgraph H is mathematically expressed as:
V '\subseteq V and E' \subseteq E \cap  (V'×V')

Subgraphs are used to identify specific patterns within a network, such as cliques or paths. In a computational context, generating subgraphs allows us to focus on "ego networks" or specific clusters of interest, which is a common requirement in social network analysis and biological modeling.

### Spanning Subgraph
A spanning subgraph is a subgraph H=(V', E') of a graph $G = (V, E)$ such that V'=V. This means the subgraph contains every single vertex present in the original graph, but it may contain only a subset of the edges. A spanning subgraph preserves the "skeleton" of the vertex set while simplifying the connectivity, often used to find the most efficient way to connect all nodes in a network, such as in the case of a Spanning Tree.

For any graph G with n vertices and m edges, the number of possible spanning subgraphs is:
N = 2m

Each edge in G has two choices: to be included in the spanning subgraph or not. Common examples include Hamiltonian paths, which visit every vertex exactly once, and Minimum Spanning Trees (MSTs), which connect all vertices with the minimum possible total edge weight.

### Induced Subgraph
An induced subgraph G[S] is a subgraph formed from a graph $G = (V, E)$ by taking a subset of vertices S \subseteq V and including every edge from the original graph that has both endpoints in S. Unlike a general subgraph where we can choose which edges to include, in an induced subgraph, once the vertices are chosen, the edges are automatically determined by the original graph's topology. If an edge exists between two selected vertices in G, it must also exist in the induced subgraph G[S].

### The edge set E' of an induced subgraph is defined as
E' = { (u,v) \in E : u, v \in S}

Induced subgraphs are critical for studying hereditary properties of graphs, properties that, if they hold for G, must also hold for any induced subgraph. They are frequently used in algorithm design to check for the presence of forbidden subgraphs, such as in the characterization of perfect graphs or interval graphs.

### Edge Induced Subgraph
An Edge Induced Subgraph is a subgraph G[E'] formed by a subset of edges E' \subseteq E(G) and all the vertices in G that are endpoints of the edges in E'. In this case, the selection of edges dictates which vertices will be part of the subgraph. Any vertex that is not an endpoint of at least one edge in the selected subset E' is excluded from the resulting subgraph. This is effectively the opposite logic of a vertex-induced subgraph, as the connectivity defines the membership of the vertices.

The edge-induced subgraph of G on edge set E' is denoted as G[E'], where the vertex set is defined as:
V(G[E']) = {v \in V(G) : ∃e \in E' incident to v}

This is particularly useful when we want to isolate specific interactions or transactions within a system. For example, in a transport network, an edge-induced subgraph might represent only the active flight paths, automatically excluding any airports that do not have active flights during a specific time frame.

### Algorithms for Subgraph Generation
The algorithm to generate subgraphs involves procedural filtering of the parent graph's components based on the type of subgraph required. For a general subgraph, the algorithm typically accepts a user-defined list of vertices and edges, verifying that each edge’s endpoints are present in the vertex list before construction. For induced subgraphs, the process is automated: the user provides only the vertex subset S, and the algorithm iterates through E(G) to identify and include all pairs (u,v) where both u,v\inS.



The specific steps for implementing these in a programming environment like NetworkX are as follows:

Step 1: Define the parent graph G with its full set of vertices V and edges E.

Step 2 (Induced): Select a subset S\subsetV. Use a filtering function to retain only edges whose endpoints are both in S.

Step 3 (Spanning): Keep all vertices V. Randomly or logically select a subset of edges E'\subsetE to form the spanning structure.

Step 4 (Edge-Induced): Select a subset of edges E'\subsetE. Identify all unique vertices that act as endpoints for E' and create the new graph using these components.

Step 5: Use visualization tools like Matplotlib to display the original graph alongside the generated subgraph to verify structural integrity.
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
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    ]
    G, matrix = adjacency_matrix_input(default_matrix, key="expt3")
    pos = layout_control(G, key="expt3")
    
    sub_type = st.selectbox("Select Subgraph Type", ["Induced (by Nodes)", "Induced (by Edges)", "Spanning Tree", "Edge Deleted"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        draw_graph(G, pos, title="Original Graph")
        
    with col2:
        H = G.copy()
        if sub_type == "Induced (by Nodes)":
            selected_nodes = st.multiselect("Select Nodes", list(G.nodes()), default=list(G.nodes())[:5])
            H = G.subgraph(selected_nodes)
            draw_graph(H, pos, title="Induced Subgraph (Nodes)")
            
        elif sub_type == "Induced (by Edges)":
            edge_list = list(G.edges())
            edge_options = [f"{u}-{v}" for u, v in edge_list]
            selected_edges_str = st.multiselect("Select Edges", edge_options, default=edge_options[:3] if edge_options else [])
            selected_edges = [tuple(map(int, e.split("-"))) for e in selected_edges_str]
            H = G.edge_subgraph(selected_edges)
            draw_graph(H, pos, title="Induced Subgraph (Edges)")
            
        elif sub_type == "Spanning Tree":
            if nx.is_connected(G):
                H = nx.minimum_spanning_tree(G)
                draw_graph(H, pos, title="Spanning Tree")
            else:
                st.warning("The graph is not connected. Generating a spanning forest.")
                H = nx.minimum_spanning_tree(G)
                draw_graph(H, pos, title="Spanning Forest")
            
        elif sub_type == "Edge Deleted":
            edge_to_delete = st.selectbox("Select Edge to Delete", list(G.edges()))
            if edge_to_delete:
                H.remove_edge(*edge_to_delete)
            draw_graph(H, pos, title=rf"Graph $G - \{{{edge_to_delete}\}}$")

footer()
