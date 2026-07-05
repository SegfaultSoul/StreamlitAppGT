import os

import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from utils import lab_header, get_source_code, header, setup_page, draw_graph, adjacency_matrix_input, layout_control, footer

setup_page("Experiment 1: Basic Graphs")

lab_header()


# Data from JSON
aim = "<b>Aim:</b> To implement basic graphs such as null graph, complete graph, cycle graph, path graph, complete bipartite graph and wheel graph."

header("Basic Graphs", aim)
sc = get_source_code("Expt 1")


theory = r"""
<div class="theory-card">

### NetworkX
NetworkX is a comprehensive Python library designed for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks. It provides high-performance data structures for representing many types of networks, including directed and undirected graphs, multigraphs, and self-loops. As a student working with graph theory, this tool is essential because it allows for the programmatic generation of standard graphs and the implementation of complex algorithms like shortest paths, clustering, and centrality measures with minimal boilerplate code.

The library is built to handle large-scale graphs efficiently and integrates seamlessly with the broader scientific Python ecosystem, such as NumPy and SciPy. Its flexibility allows us to load and store networks in standard and non-standard file formats, making it a staple for academic research and practical applications in social network analysis, biological networks, and infrastructure modeling.

### Matplotlib
Matplotlib is a cross-platform, data visualization and graphical plotting library for Python and its numerical extension NumPy. While it is a general-purpose tool for creating static, animated, and interactive visualizations, in the context of graph theory, it serves as the primary rendering engine for NetworkX. It provides the "canvas" upon which nodes, edges, and labels are drawn, allowing us to customize the aesthetics of our graphs through various layouts, color maps, and line styles.

By using the pyplot module, we can fine-tune the visual representation of mathematical structures to better understand their properties. It handles the coordinate mapping of vertices and the drawing of edges, which is crucial when we need to visually distinguish between different graph topologies like bipartite or wheel graphs. Its robust API ensures that we can export our generated graphs into high-quality formats suitable for lab reports and presentations.





### Graph
a graph G is defined as an ordered triple (V(G), E(G), $\psi_G$). This structure consists of a nonempty set V(G) of vertices and a set E(G) of edges, which must be disjoint from the vertex set. The third element, $\psi_G$, is an incidence function that associates each edge of the graph with an unordered pair of vertices. These vertices are not necessarily distinct, which accounts for the possibility of loops where an edge connects a vertex to itself. If an edge e is associated with vertices u and v such that $\psi_G$(e) = $uv$, then e is said to join u and v, and these vertices are the ends of e.

### Null Graph($N_n$)
A Null Graph (also known as an empty graph) is a graph $G = (V, E)$ where the edge set E is empty, meaning there are no edges connecting any of the vertices. In this structure, every vertex exists as an isolated point with a degree of zero. It represents the simplest form of a graph where the connectivity is null, serving as a foundational concept when building more complex structures or discussing graph complements.

In a null graph with n vertices, the total number of edges is:
|E| = 0

Despite the lack of edges, the order of the graph is still defined by the number of vertices in set V. It is primarily used in theoretical proofs and as a starting point for graph construction algorithms in NetworkX.

### Complete Graph ( $K_n$ )
A Complete Graph is a simple undirected graph in which every pair of distinct vertices is connected by a unique edge. This means that every vertex is adjacent to every other vertex in the graph, representing a state of maximum connectivity for a simple graph. In standard notation, a complete graph with n vertices is denoted as $K_n$, and it is inherently regular because every vertex has the same degree, specifically $n-1$.

The total number of edges in a complete graph $K_n$ is given by the combination formula:
$$|E| = \binom{n}{2}$$

Because of its uniform structure, the complete graph is often used to test the efficiency of graph algorithms and serves as a vital component in understanding cliques and Ramsey theory.

### Cycle Graph ( $C_n$ )
A Cycle Graph is a graph that consists of a single cycle, where the vertices are connected in a closed chain such that each vertex is visited exactly once and the last vertex connects back to the first. For a graph to be considered a cycle graph $C_n$, it must have at least three vertices ($n \ge 3$). It is a 2-regular graph, meaning every vertex in the structure has a degree of exactly 2.

In a cycle graph with n vertices, the number of edges is exactly equal to the number of vertices:
|V| = |E| = n

Cycle graphs are fundamental in studying Hamiltonian circuits and network redundancy. They represent the simplest closed-loop topology and are often found as subgraphs within more complex interconnected systems.

### Path Graph ( $P_n$ )
A Path Graph is a graph whose vertices can be arranged in a linear sequence $v_{1}, v_{2}, \dots, v_{n}$ such that the edges only exist between consecutive vertices in the list.
 Unlike a cycle graph, a path graph is not closed; it has two distinct endpoints (leaves) that have a degree of 1, while all internal vertices have a degree of 2. It represents the most basic form of a connected tree structure.

For a path graph $P_n$ consisting of n vertices, the number of edges is always:
|E| = $n-1$

Path graphs are essential for understanding the concept of "distance" and "diameter" in graph theory. They serve as the baseline for algorithms involving traversal, such as Breadth-First Search (BFS) and Depth-First Search (DFS).

### Complete Bipartite Graph ( $K_{m,n}$ )
A Complete Bipartite Graph is a special type of bipartite graph where the vertex set V is partitioned into two disjoint sets, V1 and V2, such that every vertex in V1 is connected to every vertex in V2, but no edges exist between vertices within the same set. It is denoted as $K_{m,n}$, where m and n are the number of vertices in the respective partitions.

The total number of vertices in this graph is $m+n$, and the total number of edges is calculated as:
|E| = $m \times n$

These graphs are used extensively in modeling relationships between two different classes of objects, such as users and products in a recommendation system or workers and tasks in an assignment problem.

### Wheel Graph ( $W_n$ )
A Wheel Graph is a graph formed by taking a cycle graph C$n-1$ and connecting a single universal vertex, known as the "hub," to every vertex of that cycle. The vertices of the original cycle are referred to as the "rim." Consequently, a wheel graph $W_n$ always has n vertices, where one vertex (the hub) has a degree of $n-1$ and the remaining $n-1$ vertices (the rim) each have a degree of 3.

### The total number of edges in a wheel graph $W_n$ is
|E| = 2($n-1$)

Wheel graphs are significant in the study of planar graphs and structural graph theory. They are highly connected and often used as a basic architecture for centralized networks where a single controller communicates with a surrounding ring of nodes.
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
    st.subheader("Graph Presets")
    preset = st.selectbox("Select a Preset Graph", 
                          ["None", "Null Graph (N5)", "Complete Graph (K6)", "Path Graph (P5)", "Complete Bipartite (K3,4)", "Cycle Graph (C8)", "Wheel Graph (W6)"])
    
    n = 6
    default_matrix = np.zeros((n, n), dtype=int)
    
    if preset == "Null Graph (N5)":
        n = 5
        G_pre = nx.empty_graph(n)
        default_matrix = nx.to_numpy_array(G_pre, dtype=int)
    elif preset == "Complete Graph (K6)":
        n = 6
        G_pre = nx.complete_graph(n)
        default_matrix = nx.to_numpy_array(G_pre, dtype=int)
    elif preset == "Path Graph (P5)":
        n = 5
        G_pre = nx.path_graph(n)
        default_matrix = nx.to_numpy_array(G_pre, dtype=int)
    elif preset == "Complete Bipartite (K3,4)":
        n = 7
        G_pre = nx.complete_bipartite_graph(3, 4)
        default_matrix = nx.to_numpy_array(G_pre, dtype=int)
    elif preset == "Cycle Graph (C8)":
        n = 8
        G_pre = nx.cycle_graph(n)
        default_matrix = nx.to_numpy_array(G_pre, dtype=int)
    elif preset == "Wheel Graph (W6)":
        n = 6
        G_pre = nx.wheel_graph(n)
        default_matrix = nx.to_numpy_array(G_pre, dtype=int)
    else:
        # Default empty matrix
        default_matrix = np.zeros((6, 6), dtype=int)

    G, matrix = adjacency_matrix_input(default_matrix, key="expt1")
    pos = layout_control(G, key="expt1")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        draw_graph(G, pos, title="Basic Graph Visualization")
        
    with col2:
        st.subheader("Graph Analysis")
        st.write(f"**Nodes**: {G.number_of_nodes()}")
        st.write(f"**Edges**: {G.number_of_edges()}")
        st.write(f"**Density**: {nx.density(G):.2f}")
        if G.number_of_nodes() > 0:
            st.write(f"**Connected**: {nx.is_connected(G)}")
            st.write(f"**Degree Sequence**: {sorted([d for n, d in G.degree()], reverse=True)}")

footer()
