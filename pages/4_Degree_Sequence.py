import os

import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from utils import lab_header, get_source_code, header, setup_page, draw_graph, adjacency_matrix_input, layout_control, footer

setup_page("Experiment 4: Degree Sequence")

lab_header()

# Data from JSON
aim = "<b>Aim:</b> To implement construction of a graph for a given degree sequence and to verify if a sequence is graphic, using Havel-Hakimi algorithm."

header("Degree Sequence", aim)
sc = get_source_code("Expt 4")

theory = r"""
<div class="theory-card">

### Degree Sequence
A degree sequence of an undirected graph is a sequence of non-negative integers representing the degrees of its vertices, typically arranged in a non-increasing order such that $d_1 \ge d_2 \ge \dots \ge d_n$. This sequence serves as a numerical summary of the graph's local connectivity, where each integer di indicates how many edges are incident to vertex vi. A fundamental property of any degree sequence is governed by the Handshaking Lemma, which states that the sum of all degrees in the sequence must be an even number. Mathematically, for a graph $G = (V, E)$, the relation is:

A sequence is termed graphic if there exists a simple graph (a graph with no self-loops or multiple edges) that realizes that specific sequence. Not every sequence of integers is graphic; for example, a sequence is immediately disqualified if the sum of its elements is odd or if the maximum degree d1 is greater than or equal to the number of vertices n. Understanding these sequences is crucial in network synthesis, as it allows us to determine if a physical network with specific port requirements for each node can actually be constructed before attempting the physical or logical layout.

### Algorithm (Havel-Hakimi)
The Havel-Hakimi algorithm is an iterative recursive method used to determine whether a given sequence of non-negative integers is graphic and to provide a basis for constructing the corresponding simple graph. The algorithm relies on a reduction step: a sequence S={d1,d2,...,dn} is graphic if and only if the modified sequence S' is graphic, where S' is obtained by removing the largest degree d1 and subtracting 1 from the next d1 largest degrees in the remaining sequence. This process is repeated until the sequence either becomes all zeros (proving it is graphic) or results in an invalid state, such as a negative number or having fewer than d1 elements left to decrement.
In a practical implementation, the sequence must be re-sorted in non-increasing order after every subtraction step to ensure the next "hub" vertex is processed correctly. The algorithm effectively simulates the process of connecting a vertex with the highest degree requirement to the other available vertices that have the highest remaining capacities. If the algorithm terminates successfully with a sequence of zeros, we can conclude that the original degree sequence is realizable as a simple graph.
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
    st.subheader("Input Degree Sequence")
    seq_input = st.text_input("Enter degree sequence (comma separated)", "5, 4, 4, 3, 2, 2, 1, 1")
    
    try:
        sequence = sorted([int(x.strip()) for x in seq_input.split(",")], reverse=True)
    except:
        st.error("Invalid input. Please enter numbers separated by commas.")
        sequence = []

    is_graphic = nx.is_graphical(sequence)
    
    if is_graphic:
        G = nx.havel_hakimi_graph(sequence)
        pos = layout_control(G, key="expt4")
    else:
        st.warning("The sequence is NOT graphic. Displaying a default empty graph.")
        G = nx.Graph()
        G.add_nodes_from(range(len(sequence)))
        pos = nx.spring_layout(G)
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        draw_graph(G, pos, title="Graph Realization")
        
    with col2:
        st.subheader("Havel-Hakimi Analysis")
        st.write(f"**Input Sequence**: {sequence}")
        st.write(f"**Sum of Degrees**: {sum(sequence)}")
        st.write(f"**Graphic**: {'Yes' if is_graphic else 'No'}")
        
        if sequence:
            st.markdown("### Step-by-Step Reduction")
            temp_seq = sequence.copy()
            steps = [temp_seq.copy()]
            
            while temp_seq and any(d > 0 for d in temp_seq):
                d = temp_seq.pop(0)
                if d > len(temp_seq):
                    break
                for i in range(d):
                    temp_seq[i] -= 1
                temp_seq.sort(reverse=True)
                steps.append(temp_seq.copy())
                if any(d < 0 for d in temp_seq):
                    break
            
            for i, step in enumerate(steps):
                st.write(f"Step {i}: {step}")

footer()
