import os

import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from utils import lab_header, get_source_code, header, setup_page, draw_graph, adjacency_matrix_input, layout_control, footer

setup_page("Experiment 9: Eulerian Circuit")

lab_header()

# Data from JSON
aim = "<b>Aim:</b> To implement an algorithm that checks for the existence of a eulerian circuit and constructs a circuit that traverses every edge of the graph exactly once."

header("Eulerian Circuit", aim)
sc = get_source_code("Expt 9")

theory = r"""
<div class="theory-card">

An Eulerian circuit (or Euler tour) is defined as a closed trail that traverses every edge of a graph G exactly once. A graph that possesses such a circuit is termed an Eulerian graph. The fundamental characterization of these graphs rests on the degrees of their vertices. For a connected graph to be Eulerian, it is a necessary and sufficient condition that every vertex in the graph has an even degree. This requirement stems from the fact that whenever a trail enters and leaves a vertex, it accounts for two incident edges; thus, to exhaust all edges and return to the starting point, the total number of edges incident to any vertex must be a multiple of two.

The existence of an Eulerian circuit also implies that the graph must be connected, or at least that all edges belong to a single connected component. If a graph contains vertices of odd degree, it may still possess an Eulerian trail (an open trail containing all edges) provided that exactly two vertices have odd degrees; these would serve as the start and end points but it will not contain a circuit. In the implementation of these structures, the parity of the vertex degrees serves as the primary diagnostic for the graph's Eulerian property.

Fleury’s Algorithm
Step1: Initialization: Choose an arbitrary vertex $v_{0}$, and set $W_{0}$ = $v_{0}$.

step2:Edge Selection: Suppose that the trail $W_{i}$ = $v_{0}$$e_{1}$$v_{1}$...$e_{i}$$v_{i}$ has been chosen. Then choose an edge $e_{i}$__1 from E \setminus  {$e_{1}$, $e_{2}$, ..., $e_{i}$} in such a way that: (i) $e_{i}$__1 is incident with $v_{i}$. (ii) Unless there is no alternative, $e_{i}$__1 is not a cut edge of $G_{i}$ = G - {$e_{1}$, $e_{2}$, ..., $e_{i}$}.

Step 3:Termination: Stop when step 2 can no longer be implemented.
By its definition, this algorithm constructs a trail in G that serves as the Eulerian circuit.
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
    st.subheader("Eulerian Presets")
    preset = st.selectbox("Select Preset", ["None", "Eulerian Circuit (Envelope)", "Eulerian Trail (House)"])
    
    default_matrix = np.zeros((6, 6), dtype=int)
    if preset == "Eulerian Circuit (Envelope)":
        # Envelope with cross - all even degrees except...? 
        # Actually K3,3 is eulerian? No, degree 3.
        # Let's use a standard eulerian graph
        G_e = nx.complete_graph(5) # All degrees are 4 (even)
        default_matrix = nx.to_numpy_array(G_e, dtype=int)
    elif preset == "Eulerian Trail (House)":
        # House graph - usually 2 odd degrees
        G_e = nx.house_graph()
        default_matrix = nx.to_numpy_array(G_e, dtype=int)

    G, matrix = adjacency_matrix_input(default_matrix, key="expt9")
    pos = layout_control(G, key="expt9")
    
    def is_bridge(G, u, v):
        if G.degree(u) == 1:
            return False
        visited_before = len(nx.node_connected_component(G, u))
        G.remove_edge(u, v)
        visited_after = len(nx.node_connected_component(G, u))
        G.add_edge(u, v)
        return visited_before > visited_after

    def fleury_algorithm(G, start_node):
        H = G.copy()
        path = []
        curr = start_node
        while H.edges():
            neighbors = list(H.neighbors(curr))
            for v in neighbors:
                if len(neighbors) == 1 or not is_bridge(H, curr, v):
                    path.append((curr, v))
                    H.remove_edge(curr, v)
                    curr = v
                    break
        return path

    start_node = 0
    for node in G.nodes():
        if G.degree(node) % 2 != 0:
            start_node = node
            break
            
    is_eulerian = nx.is_eulerian(G) if G.number_of_nodes() > 0 else False
    has_eulerian_trail = nx.has_eulerian_path(G) if G.number_of_nodes() > 0 else False
    
    col1, col2 = st.columns(2)
    
    with col1:
        if nx.is_connected(G) or G.number_of_edges() == 0:
            if nx.is_eulerian(G) or nx.has_eulerian_path(G):
                path = fleury_algorithm(G, start_node)
                step = st.slider("Step through Traversal", 0, len(path), len(path))
                highlight = path[:step]
                title = "Eulerian Circuit" if nx.is_eulerian(G) else "Eulerian Path"
                draw_graph(G, pos, title=title, highlight_edges=highlight)
            else:
                draw_graph(G, pos, title="Non-Eulerian Graph")
        else:
            st.error("Graph must be connected to find Eulerian traversals.")
            draw_graph(G, pos, title="Disconnected Graph")

    with col2:
        st.subheader("Eulerian Analysis")
        st.write(f"**Is Eulerian**: {'Yes' if is_eulerian else 'No'}")
        st.write(f"**Has Eulerian Trail**: {'Yes' if has_eulerian_trail else 'No'}")
        
        st.markdown("**Vertex Degrees**")
        degrees = [{"Vertex": f"V{n}", "Degree": d, "Parity": "Even" if d % 2 == 0 else "Odd"} for n, d in G.degree()]
        st.table(pd.DataFrame(degrees))
        
        if is_eulerian:
            circuit = list(nx.eulerian_circuit(G))
            st.success(f"**Circuit Found**: {rf' \rightarrow '.join([f'V{u}' for u, v in circuit] + [f'V{circuit[0][0]}'])}")
        elif has_eulerian_trail:
            trail = list(nx.eulerian_path(G))
            st.warning(f"**Trail Found**: {rf' \rightarrow '.join([f'V{u}' for u, v in trail] + [f'V{trail[-1][1]}'])}")

footer()
