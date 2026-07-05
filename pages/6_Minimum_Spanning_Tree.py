import os

import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from utils import lab_header, get_source_code, header, setup_page, draw_graph, adjacency_matrix_input, layout_control, footer

setup_page("Experiment 6: Minimum Spanning Tree")

lab_header()

# Data from JSON
aim = "<b>Aim:</b> To implement kruskal’s algorithm to generate the minimum spanning tree ensuring all vertices are connected with minimum edge weights and no cycles."

header("Minimum Spanning Tree", aim)
sc = get_source_code("Expt 6")

theory = r"""
<div class="theory-card">

Let $G = (V, E)$ be a connected graph where each edge e \in E is assigned a real-valued weight $w(e)$. In many practical applications, G represents a potential communications network where the vertices V = {$v_1$, $v_2$, ..., vn} are stations and the weights represent construction costs. The objective is to determine a connected subgraph H = (V, EH) such that the total weight, defined by the summation formula:

is minimized. Bondy and Murty demonstrate that such an optimal subgraph must be a tree. If H contained a cycle C, the removal of any edge e \in C would result in a subgraph H' = H - e that remains connected but possesses a strictly smaller weight, w(H') = w(H) - $w(e)$ (assuming $w(e)$ > 0). Thus, any minimal connected subgraph containing all vertices v of G is a spanning tree.
A spanning tree T of G is a subgraph that is both acyclic and connected, containing every vertex in V. A spanning tree of v vertices must contain exactly v - 1 edges. An optimal tree T* is defined as a spanning tree that satisfies the condition:
w(T*) = min{ w(T) : T  is a spanning tree of G}
The existence of an optimal tree is guaranteed for any finite connected graph, as the number of spanning trees is finite. The problem of finding T* is solved by selecting a set of edges {$e_1$, $e_2$, ..., e$n-1$} that minimizes the sum of weights while satisfying the constraint that no subset of these edges forms a cycle.
### Kruskal’s Algorithm
The construction of an optimal tree T is achieved through the following iterative procedure:
Step 1: Choose an edge $e_1$ from E such that w($e_1$) is as small as possible.
Step 2: If edges $e_1$, $e_2$, ..., ei have been chosen, select the next edge ei+1  from the set E - {$e_1$, $e_2$, 	..., ei} such that the subgraph G[{$e_1$, $e_2$, ... ei+1}] is acyclic and the weight w(ei+1) is as small as possible subject to the acyclic condition.
Step 3: The algorithm terminates when i+1 = n - 1.
The resulting set of edges {$e_1$, $e_2$, ..., e$n-1$} forms the edge set of an optimal spanning tree of G. The algorithm's validity rests on the property that a greedy choice at each step consistently leads to a global minimum.
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
        [0, 4, 0, 0, 8, 0, 0, 0, 0],
        [4, 0, 8, 0, 11, 0, 0, 0, 0],
        [0, 8, 0, 7, 0, 2, 0, 4, 0],
        [0, 0, 7, 0, 0, 0, 0, 14, 9],
        [8, 11, 0, 0, 0, 7, 1, 0, 0],
        [0, 0, 2, 0, 7, 0, 6, 0, 0],
        [0, 0, 0, 0, 1, 6, 0, 2, 0],
        [0, 0, 4, 14, 0, 0, 2, 0, 10],
        [0, 0, 0, 9, 0, 0, 0, 10, 0]
    ]
    G, matrix = adjacency_matrix_input(default_matrix, key="expt6")
    pos = layout_control(G, key="expt6")
    
    # Calculate MST steps manually for visualization
    sorted_edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    mst_T = nx.Graph()
    mst_T.add_nodes_from(G.nodes())
    steps = []
    for u, v, d in sorted_edges:
        if not nx.has_path(mst_T, u, v):
            mst_T.add_edge(u, v, **d)
            steps.append({"Edge": (u, v), "Weight": d['weight'], "Status": "Added"})
        else:
            steps.append({"Edge": (u, v), "Weight": d['weight'], "Status": "Skipped (Cycle)"})
        if mst_T.number_of_edges() == G.number_of_nodes() - 1:
            # Continue to show remaining edges as skipped? 
            # Docs code continues until all sorted edges are checked or n-1 edges added.
            pass

    col1, col2 = st.columns(2)
    
    with col1:
        draw_graph(G, pos, title="Original Weighted Graph", edge_labels=True)
        
    with col2:
        draw_graph(G, pos, title="Minimum Spanning Tree (Highlighted)", highlight_edges=list(mst_T.edges()), edge_labels=True)
        
    st.markdown("### Kruskal's Analysis")
    st.write(f"**Total MST Weight**: {sum(d['weight'] for u, v, d in mst_T.edges(data=True))}")
    
    st.markdown("**Step-by-Step Edge Processing**")
    steps_df = pd.DataFrame([
        {"Step": i+1, "Edge": f"({s['Edge'][0]}, {s['Edge'][1]})", "Weight": s['Weight'], "Action": s['Status']} 
        for i, s in enumerate(steps)
    ])
    st.table(steps_df)

footer()
