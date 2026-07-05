import os

import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from utils import lab_header, get_source_code, header, setup_page, draw_graph, adjacency_matrix_input, layout_control, footer

setup_page("Experiment 8: Walks, Trails & Paths")

lab_header()

# Data from JSON
aim = "<b>Aim:</b> To implement generation of closed walks, trails and paths in a connected graph."

header("Walks, Trails & Paths", aim)
sc = get_source_code("Expt 8")

theory = r"""
<div class="theory-card">

In the formal study of connectivity, a walk in a graph G is defined as a finite non-null sequence W = $v_0$ $e_1$ $v_1$ $e_2$ ... ek vk, whose terms are alternately vertices and edges, such that for 1 $\le$ i $\le$ k, the ends of edge ei are vi-1 and vi. The integer k is referred to as the length of the walk, representing the total count of edges traversed. A walk is categorized as closed if its initial and terminal vertices are identical ($v_0$ = vk); otherwise, it is considered an open walk.
To differentiate between specific types of traversals and analyze graph connectivity more precisely, we apply specific constraints on the repetition of vertices and edges within the sequence:
Trail: A walk is defined as a trail if all its edges $e_1$, $e_2$, ..., ek are distinct. While edges cannot be repeated in a trail, vertices may be revisited. A closed trail, where the start and end vertices are the same, is often referred to as a circuit.
Path: A walk is defined as a path if all its vertices $v_0$, $v_1$, ..., vk are distinct. Since distinct vertices inherently imply that the edges connecting them must also be distinct, every path is necessarily a trail. A closed path (where $v_0$ = vk but all internal vertices are distinct) is known as a cycle.
Mathematically, these structures form a clear hierarchy of restrictions: every path is a trail, and every trail is a walk. This classification is fundamental to graph theory, as in a connected graph, there exists at least one path between any two distinct vertices. This existence of paths serves as the foundational basis for generating these sequences algorithmically and determining the overall reachability within a network.
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
        [0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 1, 1, 0]
    ]
    G, matrix = adjacency_matrix_input(default_matrix, key="expt8")
    pos = layout_control(G, key="expt8")
    
    st.subheader("Generate Traversal")
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        source = st.selectbox("Start Node", list(G.nodes()), index=0)
    with col_t2:
        target = st.selectbox("End Node", list(G.nodes()), index=len(G.nodes())-1)
    with col_t3:
        type_sel = st.selectbox("Type", ["Shortest Path", "All Simple Paths", "All Trails (via DFS)"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if type_sel == "Shortest Path":
            try:
                path = nx.shortest_path(G, source=source, target=target)
                edges = list(zip(path, path[1:]))
                draw_graph(G, pos, title="Shortest Path", highlight_edges=edges)
            except:
                st.error("No path found")
                path = []
        elif type_sel == "All Simple Paths":
            paths = list(nx.all_simple_paths(G, source=source, target=target))
            if paths:
                path_idx = st.select_slider("Select Path", options=range(len(paths)))
                path = paths[path_idx]
                edges = list(zip(path, path[1:]))
                draw_graph(G, pos, title=f"Simple Path {path_idx+1}", highlight_edges=edges)
            else:
                st.error("No path found")
                path = []
        else:
            # Trails (Edges distinct) - use a simple DFS for demonstration
            def find_all_trails(graph, current, end, visited_edges, current_path):
                if current == end:
                    yield current_path
                for neighbor in graph.neighbors(current):
                    edge = tuple(sorted((current, neighbor)))
                    if edge not in visited_edges:
                        yield from find_all_trails(graph, neighbor, end, visited_edges | {edge}, current_path + [neighbor])
            
            trails = list(find_all_trails(G, source, target, set(), [source]))
            if trails:
                trail_idx = st.select_slider("Select Trail", options=range(len(trails)))
                path = trails[trail_idx]
                edges = list(zip(path, path[1:]))
                draw_graph(G, pos, title=f"Trail {trail_idx+1}", highlight_edges=edges)
            else:
                st.error("No trail found")
                path = []

    with col2:
        st.subheader("Traversal Analysis")
        if path:
            st.write(f"**Length**: {len(path)-1}")
            st.write(f"**Vertices**: {rf' \rightarrow '.join([f'V{v}' for v in path])}")
            
            is_path = len(set(path)) == len(path)
            edges_traversed = list(zip(path, path[1:]))
            std_edges = [tuple(sorted(e)) for e in edges_traversed]
            is_trail = len(std_edges) == len(set(std_edges))
            
            st.markdown(f"- **Is Path?**: {'Yes' if is_path else 'No'}")
            st.markdown(f"- **Is Trail?**: {'Yes' if is_trail else 'No'}")
            st.markdown(f"- **Is Walk?**: Yes (Always)")
            
            if path[0] == path[-1] and len(path) > 1:
                st.success("This is a **CLOSED** traversal (Circuit/Cycle)")
            else:
                st.info("This is an **OPEN** traversal")

footer()
