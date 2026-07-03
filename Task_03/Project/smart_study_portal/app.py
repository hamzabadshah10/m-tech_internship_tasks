import streamlit as st
import pandas as pd
from data import CITY_GRAPH, HEURISTICS
from algorithms import bfs, ucs, a_star

# Helper function to center and bold dataframe contents
def center_df(df):
    return df.style.set_properties(**{'text-align': 'center', 'font-weight': 'bold'}).set_table_styles([dict(selector='th', props=[('text-align', 'center'), ('font-weight', 'bold')])])

# Streamlit Page Configuration
st.set_page_config(
    page_title="SmartRoute Planner", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Bold UI
st.markdown("""
    <style>
    /* Make absolutely everything bold */
    * {
        font-weight: 800 !important;
    }
    
    /* Highlighting specific headers */
    .sidebar-header {
        font-size: 1.5rem !important;
        color: #ffffff !important; 
        margin-bottom: 0.5rem;
        border-bottom: 3px solid rgba(255, 255, 255, 0.3) !important;
        padding-bottom: 0.5rem;
    }
    
    /* Bold Sidebar Background (Dark Charcoal) */
    [data-testid="stSidebar"] {
        background-color: #36454F !important;
        background-image: linear-gradient(135deg, #36454F, #1f2933) !important;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    .section-header {
        font-size: 2.2rem !important;
        letter-spacing: 1px;
    }
    
    /* Highlight gradient text for main title */
    .title-highlight {
        background: -webkit-linear-gradient(45deg, #0284c7, #4338ca);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        margin-bottom: 0px;
    }
    
    /* Styling Streamlit Metrics (cards) */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        color: #0284c7 !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.2rem !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: #1e3a8a !important; /* Dark Blue */
        color: white !important; /* Light Text */
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem !important;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 58, 138, 0.6);
        background: #1e40af !important;
        color: white !important;
    }
    
    /* HTML Table Centering */
    .dataframe-container table {
        width: 100%;
        color: var(--text-color);
        border-collapse: collapse;
        margin-top: 10px;
    }
    .dataframe-container th, .dataframe-container td {
        text-align: center !important;
        font-weight: bold !important;
        padding: 12px;
        border: 1px solid var(--faded-text20, #ccc);
    }
    .dataframe-container th {
        background-color: var(--secondary-background-color);
        color: #0284c7;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE INIT -----------------
if 'df_edges' not in st.session_state:
    edges = []
    for u, neighbors in CITY_GRAPH.items():
        for v, w in neighbors.items():
            edges.append({"From Node": u, "To Node": v, "Distance (km)": w})
    if not edges:
        edges = [{"From Node": "", "To Node": "", "Distance (km)": float('nan')}]
    st.session_state.df_edges = pd.DataFrame(edges)

if 'df_heuristics' not in st.session_state:
    heuristics = [{"Location Node": k, "Estimated Distance to Goal (km)": v} for k, v in HEURISTICS.items()]
    if not heuristics:
        heuristics = [{"Location Node": "", "Estimated Distance to Goal (km)": float('nan')}]
    st.session_state.df_heuristics = pd.DataFrame(heuristics)
# --------------------------------------------------------

# App Header
st.markdown('<h1 class="title-highlight">Smart Delivery Route Planner</h1>', unsafe_allow_html=True)
st.markdown("""
<p style='font-size: 1.2rem; margin-bottom: 2rem;'>
A powerful AI visualization tool comparing Breadth-First Search (BFS), Uniform Cost Search (UCS), and A* Algorithms.
</p>
""", unsafe_allow_html=True)

# Sidebar for User Input
with st.sidebar:
    st.markdown('<div class="sidebar-header">App Mode</div>', unsafe_allow_html=True)
    app_mode = st.radio("Select functionality:", ["Route Planner", "Data Editor (Build Network)"])
    
    st.markdown("---")

# Parse session state data
custom_graph = {}
custom_heuristics = {}

if not st.session_state.df_edges.empty:
    for index, row in st.session_state.df_edges.iterrows():
        u, v, w = row['From Node'], row['To Node'], row['Distance (km)']
        if pd.notna(u) and str(u).strip() != "" and pd.notna(v) and str(v).strip() != "" and pd.notna(w):
            u_str, v_str = str(u).strip(), str(v).strip()
            if u_str not in custom_graph: custom_graph[u_str] = {}
            custom_graph[u_str][v_str] = float(w)
            if v_str not in custom_graph: custom_graph[v_str] = {}

if not st.session_state.df_heuristics.empty:
    for index, row in st.session_state.df_heuristics.iterrows():
        node, h = row.iloc[0], row.iloc[1]
        if pd.notna(node) and str(node).strip() != "" and pd.notna(h):
            custom_heuristics[str(node).strip()] = float(h)


# MODE 1: DATA EDITOR
if app_mode == "Data Editor (Build Network)":
    st.markdown("### Interactive Network Builder")
    st.markdown("Modify the network structure below. You can edit distances, add new paths, or create entirely new cities.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 1. Network Connections (Edges)")
        
        # CSV Upload for Edges
        uploaded_edges = st.file_uploader("Upload Edges CSV", type="csv", key="edge_uploader")
        if uploaded_edges is not None:
            try:
                new_df = pd.read_csv(uploaded_edges)
                if "From Node" in new_df.columns and "To Node" in new_df.columns and "Distance (km)" in new_df.columns:
                    st.session_state.df_edges = new_df
                    st.success("Edges CSV loaded successfully!")
                else:
                    st.error("CSV must contain exactly: 'From Node', 'To Node', and 'Distance (km)' columns.")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
                
        st.session_state.df_edges = st.data_editor(
            st.session_state.df_edges,
            num_rows="dynamic",
            width="stretch",
            hide_index=True,
            column_config={
                "Distance (km)": st.column_config.NumberColumn(
                    "Distance (km)",
                    format="%.1f km",
                    min_value=0.0
                )
            },
            key="edge_editor"
        )
        
    with col2:
        st.markdown("#### 2. Node Heuristics (Estimates)")
        
        # CSV Upload for Heuristics
        uploaded_heuristics = st.file_uploader("Upload Heuristics CSV", type="csv", key="heuristic_uploader")
        if uploaded_heuristics is not None:
            try:
                new_df = pd.read_csv(uploaded_heuristics)
                # Flexible check for heuristics column since its name can vary
                h_col = None
                for col in new_df.columns:
                    if 'km' in col.lower() or 'distance' in col.lower() or 'estimate' in col.lower():
                        h_col = col
                
                if "Location Node" in new_df.columns and h_col:
                    # Standardize the column name to exactly match the app's internal requirement
                    new_df = new_df[["Location Node", h_col]].copy()
                    new_df.rename(columns={h_col: "Estimated Distance to Goal (km)"}, inplace=True)
                    st.session_state.df_heuristics = new_df
                    st.success("Heuristics CSV loaded successfully!")
                else:
                    st.error("CSV must contain a 'Location Node' column and a distance column.")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
                
        st.session_state.df_heuristics = st.data_editor(
            st.session_state.df_heuristics,
            num_rows="dynamic",
            width="stretch",
            hide_index=True,
            column_config={
                "Estimated Distance to Goal (km)": st.column_config.NumberColumn(
                    "Estimated Distance to Goal (km)",
                    format="%.1f km",
                    min_value=0.0
                )
            },
            key="heuristic_editor"
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Save", type="primary"):
        st.success("✅ Your custom network has been saved! You can now switch back to 'Route Planner' mode.")

# MODE 2: ROUTE PLANNER
elif app_mode == "Route Planner":
    
    with st.sidebar:
        st.markdown('<div class="sidebar-header">Route Settings</div>', unsafe_allow_html=True)
        st.markdown("<p style='font-weight:500;'>Select your pickup and drop-off locations below.</p>", unsafe_allow_html=True)
        
        available_nodes = list(custom_graph.keys())
        
        if not available_nodes:
            st.error("Your custom network has no nodes. Go to Data Editor to add them.")
            start_node = None
            goal_node = None
            execute_search = False
        else:
            start_node = st.selectbox("Start Node (Pickup)", options=available_nodes, index=0)
            
            # Default to the last node if possible
            default_goal_index = len(available_nodes)-1 if len(available_nodes) > 0 else 0
            goal_node = st.selectbox("Goal Node (Drop-off)", options=available_nodes, index=default_goal_index)
            
            st.markdown("---")
            execute_search = st.button("FIND BEST ROUTE", width="stretch")

    if available_nodes and execute_search:
        if start_node not in custom_graph or goal_node not in custom_graph:
            st.error("Invalid node selected. Please select a valid node from the sidebar.")
        else:
            st.markdown(f"<h3>Optimal Route Analysis: <span style='color:#0284c7;'>`{start_node}`</span> -> <span style='color:#0284c7;'>`{goal_node}`</span></h3>", unsafe_allow_html=True)
            
            # Run algorithms using custom graph!
            bfs_path, bfs_cost, bfs_explored = bfs(custom_graph, start_node, goal_node)
            ucs_path, ucs_cost, ucs_explored = ucs(custom_graph, start_node, goal_node)
            astar_path, astar_cost, astar_explored = a_star(custom_graph, start_node, goal_node, custom_heuristics)
            
            if not bfs_path and not ucs_path and not astar_path:
                st.error("No valid path could be found between the selected nodes.")
            else:
                # Create a visually appealing metrics layout for the winning algorithm (A*)
                st.markdown("<h3 style='color: #059669; margin-top: 20px;'>AI Recommendation (A* Search)</h3>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(label="Shortest Path Found", value=" -> ".join(astar_path))
                with col2:
                    st.metric(label="Total Distance (Cost)", value=f"{astar_cost:.2f} km")
                with col3:
                    st.metric(label="Nodes Explored (Efficiency)", value=f"{astar_explored} nodes")
                    
                st.markdown("---")
                st.markdown("<h3>Algorithm Comparison Matrix</h3>", unsafe_allow_html=True)
                
                results = [
                    {
                        "Algorithm": "Breadth-First Search (BFS)",
                        "Path Found": " -> ".join(bfs_path) if bfs_path else "No Path",
                        "Total Cost": f"{bfs_cost:.2f}" if bfs_path else "N/A",
                        "Nodes Explored": bfs_explored
                    },
                    {
                        "Algorithm": "Uniform Cost Search (UCS)",
                        "Path Found": " -> ".join(ucs_path) if ucs_path else "No Path",
                        "Total Cost": f"{ucs_cost:.2f}" if ucs_path else "N/A",
                        "Nodes Explored": ucs_explored
                    },
                    {
                        "Algorithm": "A* Search (Optimal)",
                        "Path Found": " -> ".join(astar_path) if astar_path else "No Path",
                        "Total Cost": f"{astar_cost:.2f}" if astar_path else "N/A",
                        "Nodes Explored": astar_explored
                    }
                ]
                
                # Convert results to DataFrame and display as an interactive dataframe
                df_results = pd.DataFrame(results)
                
                # Render as raw HTML table to force perfect center alignment
                html_table = df_results.to_html(index=False, escape=False)
                st.markdown(f'<div class="dataframe-container">{html_table}</div><br>', unsafe_allow_html=True)
                
                st.success("Pathfinding successfully executed. Note how A* generally explores fewer nodes than BFS to find the same optimal path!")

    # Show Data Reference in Route Planner mode too
    st.markdown("---")
    st.markdown('<div class="section-header">CURRENT DATA REFERENCE</div>', unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom: 15px;'>Review the current graph data and heuristics below. You can change this data in the 'Data Editor' mode.</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["City Graph (Connections & Distances)", "Heuristics (Estimated Distances to Goal)"])
    
    with tab1:
        st.session_state.df_edges = st.data_editor(
            center_df(st.session_state.df_edges),
            num_rows="dynamic",
            width="stretch",
            hide_index=True,
            column_config={
                "Distance (km)": st.column_config.NumberColumn(
                    "Distance (km)",
                    format="%.1f km",
                    min_value=0.0
                )
            },
            key="route_planner_edge_editor"
        )
        
    with tab2:
        st.session_state.df_heuristics = st.data_editor(
            center_df(st.session_state.df_heuristics),
            num_rows="dynamic",
            width="stretch",
            hide_index=True,
            column_config={
                "Estimated Distance to Goal (km)": st.column_config.NumberColumn(
                    "Estimated Distance to Goal (km)",
                    format="%.1f km",
                    min_value=0.0
                )
            },
            key="route_planner_heuristic_editor"
        )
