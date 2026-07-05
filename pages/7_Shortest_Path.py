import os

import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from utils import lab_header, get_source_code, header, setup_page, draw_graph, adjacency_matrix_input, layout_control, footer

setup_page("Experiment 7: Shortest Path")

lab_header()

# Data from JSON
aim = "<b>Aim:</b> To implement the shortest path algorithm in order to compute the shortest path between two vertices in a weighted graph."

header("Shortest Path", aim)
sc = get_source_code("Expt 7")

theory = r"""
<div class="theory-card">

A weighted graph G is a graph in which each edge e is assigned a real number $w(e)$, called its weight. The weight of a path P, denoted by w(P), is defined as the sum of the weights of the edges comprising the path:


For any two vertices u and v in G, the distance d(u, v) is the weight of a shortest (u, v)-path. In the case where no path exists between u and v, d(u, v) = \infty . To determine the shortest distance from a source vertex $u_0$ to all other vertices v \in V, the algorithm maintains a set S of vertices whose shortest distances from $u_0$ have already been established. For each vertex v \in V\S, a label $\lambda(v)$ is maintained, representing the current upper bound on d($u_0$, v). This label is defined by the minimum weight of paths from $u_0$ to v whose intermediate vertices are all contained within the set S:


The algorithm assumes all edge weights are non-negative ($w(e)$ $\ge$ 0), ensuring that once a vertex is added to S, its label $\lambda(v)$ equals the true shortest distance d($u_0$, v).
Based on the provided image from the Bondy and Murty textbook, here are the exact algorithmic steps for Dijkstra’s Algorithm, formatted for clarity and ease of use in documents like Google Docs:
### Dijkstra’s Algorithm
Step 1: Set l($u_0$) = 0, l(v) = \infty  for v = $u_0$, S0 = {$u_0$} and $i = 0$.

Step 2:For each v \in S’i, replace l(v) by min{l(v), l(ui) + w(uiv)}. Compute minv\inS’i{l(v)} and let ui+1 denote a vertex for which this minimum is attained. Set Si+1 = Si \cup{ui+1}.

Step 3: If i = \nu-1, stop. If i < \nu-1, replace i by i+1 and go to step 2.
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
        [0, 1, 9, 0, 0, 14],
        [1, 0, 10, 15, 0, 0],
        [9, 10, 0, 11, 0, 2],
        [0, 15, 11, 0, 6, 0],
        [0, 0, 0, 6, 0, 9],
        [14, 0, 2, 0, 9, 0]
    ]
    G, matrix = adjacency_matrix_input(default_matrix, key="expt7")
    pos = layout_control(G, key="expt7")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        source = st.selectbox("Select Source Vertex", list(G.nodes()), index=0)
    with col_sel2:
        target = st.selectbox("Select Target Vertex", list(G.nodes()), index=len(G.nodes())-1)
    
    
    try:
        path = nx.shortest_path(G, source=source, target=target, weight='weight')
        path_edges = list(zip(path, path[1:]))
        path_weight = nx.shortest_path_length(G, source=source, target=target, weight='weight')
    except:
        path = []
        path_edges = []
        path_weight = 0
        st.error("No path exists between the selected vertices.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        draw_graph(G, pos, title="Shortest Path (Highlighted)", highlight_edges=path_edges, edge_labels=True)
        
    with col2:
        st.subheader("Path Analysis")
        st.write(f"**Source**: $V_{source}$")
        st.write(f"**Target**: $V_{target}$")
        st.markdown(rf"**Shortest Path**: {rf' \rightarrow '.join([f'$V_{v}$' for v in path]) if path else 'N/A'}")
        st.markdown(f"**Total Path Weight**: ### {path_weight}")
        
        if path:
            st.markdown("**Path Details**")
            details = []
            current_w = 0
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                w = G[u][v]['weight']
                current_w += w
                details.append({"Step": i+1, "From": f"V{u}", "To": f"V{v}", "Weight": w, "Total": current_w})
            st.table(pd.DataFrame(details))

footer()
