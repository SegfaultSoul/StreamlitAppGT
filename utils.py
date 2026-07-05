import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def setup_page(title):
    st.set_page_config(
        page_title=title,
        page_icon=None,
        layout="wide"
    )
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #f8fafc;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #f1f5f9;
            padding: 8px 16px 0px 16px;
            border-radius: 10px 10px 0px 0px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 45px;
            padding: 0px 20px;
            background-color: transparent;
            border-radius: 5px 5px 0px 0px;
            font-weight: 600;
            color: #475569;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            color: #4f46e5 !important;
            border-bottom: 2px solid #4f46e5;
        }
        .theory-card {
            background-color: #ffffff;
            padding: 2.5rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            margin-bottom: 2rem;
            color: #1e293b;
            line-height: 1.6;
        }
        .lab-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            margin-bottom: 1.5rem;
            color: #1e293b;
        }
        h1, h2, h3 {
            color: #1e293b !important;
        }
        p, li, span {
            color: #334155 !important;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            height: 3em;
            background-color: #4f46e5;
            color: white;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

def lab_header():
    st.markdown(
        "<div style='text-align: center; color: #64748b; padding-bottom: 1rem; font-size: 1.1rem; font-weight: 600; border-bottom: 1px solid #e2e8f0; margin-bottom: 2rem;'>"
        "CMP-226 Graph Theory and Combinatorics Lab"
        "</div>",
        unsafe_allow_html=True
    )

def get_source_code(expt_key):
    import json
    import os
    try:
        # Resolve path relative to this file
        base_path = os.path.dirname(__file__)
        with open(os.path.join(base_path, 'source_code.json'), 'r') as f:
            data = json.load(f)
        return data.get(expt_key, {"code": "No code found.", "output": "No output found.", "images": []})
    except Exception as e:
        return {"code": f"Error loading code: {e}", "output": "Error loading output.", "images": []}

def draw_graph(G, pos=None, title="Graph Visualization", highlight_edges=None, node_colors=None, edge_labels=False, directed=False):
    fig, ax = plt.subplots(figsize=(10, 7), facecolor='white')
    
    if pos is None:
        pos = nx.spring_layout(G, seed=42)
    
    if node_colors is None:
        node_colors = "#AFA9EC"
    
    # Nodes
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=1000, 
                           edgecolors="#1e293b", linewidths=1.5)
    
    # Edges
    if highlight_edges:
        # Convert highlight edges to standardized tuples for matching
        std_highlights = set()
        for e in highlight_edges:
            if len(e) >= 2:
                std_highlights.add(tuple(sorted((e[0], e[1]))))
        
        other_edges = []
        high_edges = []
        for u, v in G.edges():
            if tuple(sorted((u, v))) in std_highlights:
                high_edges.append((u, v))
            else:
                other_edges.append((u, v))
                
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=other_edges, edge_color="#cbd5e1", 
                               width=1, alpha=0.5, arrows=directed)
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=high_edges, edge_color="#ef4444", 
                               width=3, arrows=directed)
    else:
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#475569", width=1.5, arrows=directed)
    
    # Labels
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=11, font_weight="bold", font_color="#1e293b")
    
    if edge_labels:
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax, font_size=9, font_color="#475569")
    
    ax.set_title(title, fontsize=14, pad=20, fontweight='bold')
    ax.axis("off")
    st.pyplot(fig)

def adjacency_matrix_input(default_matrix, key=""):
    st.subheader("Adjacency Matrix Input")
    
    # Track if the default matrix changed (e.g., via a preset)
    if f"last_default_{key}" not in st.session_state:
        st.session_state[f"last_default_{key}"] = np.array(default_matrix)
    
    # If the provided default_matrix is different from the last one, reset session state
    if not np.array_equal(st.session_state[f"last_default_{key}"], np.array(default_matrix)):
        st.session_state[f"last_default_{key}"] = np.array(default_matrix)
        st.session_state[f"matrix_{key}"] = np.array(default_matrix)
        st.session_state[f"n_nodes_{key}"] = len(default_matrix)
        # Use st.rerun() to ensure the number_input and data_editor get the new values
        st.rerun()

    if f"n_nodes_{key}" not in st.session_state:
        st.session_state[f"n_nodes_{key}"] = len(default_matrix)
    
    col_size, _ = st.columns([1, 3])
    with col_size:
        n = st.number_input("Number of Nodes", min_value=1, max_value=25, 
                           value=st.session_state[f"n_nodes_{key}"], key=f"num_{key}")
    
    if n != st.session_state[f"n_nodes_{key}"]:
        st.session_state[f"n_nodes_{key}"] = n
        
    if f"matrix_{key}" not in st.session_state:
        st.session_state[f"matrix_{key}"] = np.array(default_matrix)
    
    curr_matrix = st.session_state[f"matrix_{key}"]
    curr_n = curr_matrix.shape[0]
    
    if n != curr_n:
        new_matrix = np.zeros((n, n), dtype=int)
        min_n = min(n, curr_n)
        new_matrix[:min_n, :min_n] = curr_matrix[:min_n, :min_n]
        st.session_state[f"matrix_{key}"] = new_matrix
        curr_matrix = new_matrix

    df = pd.DataFrame(curr_matrix, 
                      index=[f"V{i}" for i in range(n)], 
                      columns=[f"V{i}" for i in range(n)])
    
    edited_df = st.data_editor(df, key=f"am_{key}", width="stretch")
    
    # Update session state with edited values
    matrix = edited_df.values
    st.session_state[f"matrix_{key}"] = matrix
    
    G = nx.from_numpy_array(matrix)
    
    st.info("Edit the matrix values above. Use non-zero values for edges, and values > 1 for weights. Change 'Number of Nodes' to resize.")
    
    return G, matrix

def layout_control(G, key=""):
    st.subheader("Layout and Positioning")
    layout_type = st.selectbox("Layout Type", 
                               ["Spring", "Circular", "Shell", "Random", "Custom (x,y)"], 
                               key=f"layout_sel_{key}")
    
    if layout_type == "Custom (x,y)":
        n = G.number_of_nodes()
        
        # Persist custom positions in session state
        state_key = f"custom_pos_df_{key}"
        if state_key not in st.session_state or len(st.session_state[state_key]) != n:
            import math
            initial_pos = []
            for i in range(n):
                angle = 2 * math.pi * i / n
                initial_pos.append({"Node": i, "x": round(math.cos(angle), 2), "y": round(math.sin(angle), 2)})
            st.session_state[state_key] = pd.DataFrame(initial_pos)
        
        edited_df = st.data_editor(st.session_state[state_key], num_rows="fixed", 
                                   key=f"pos_editor_{key}", width="stretch")
        st.session_state[state_key] = edited_df
        
        return {row["Node"]: (row["x"], row["y"]) for _, row in edited_df.iterrows()}
    
    if layout_type == "Spring": return nx.spring_layout(G, seed=42)
    if layout_type == "Circular": return nx.circular_layout(G)
    if layout_type == "Shell": return nx.shell_layout(G)
    return nx.random_layout(G, seed=42)

def header(title="CMP-226 Graph Theory and Combinatorics Lab", subtitle="An interactive environment for exploring graph algorithms and theoretical properties"):
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3rem;">{title}</h1>
        {f'<p style="font-size: 1.1rem; color: #64748b;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def footer():
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #64748b; padding: 2rem; font-size: 1rem;'>"
        "Varad Kamat | 24B-CO-508 | Semester 4"
        "</div>",
        unsafe_allow_html=True
    )
