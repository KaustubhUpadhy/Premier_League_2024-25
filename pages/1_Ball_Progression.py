import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st 


st.set_page_config(page_title="Ball Progression", layout="wide")

st.title("Ball Progression: Pass + Carry")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("player_stats.csv")

df = load_data()

# Create placeholder for graph at top
graph_placeholder = st.empty()

# Create initial blank graph
def create_blank_graph():
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#0e1a26")
    ax.set_facecolor("#0e1a26")
    
    for spine in ax.spines.values():
        spine.set_color("white")
    ax.tick_params(colors="white")
    
    ax.set_xlabel("Progression via Pass (Season Total)", color="white")
    ax.set_ylabel("Progression via Carry (Season Total)", color="white")
    ax.set_title("Ball Progression - Pass + Carry", color="white")
    ax.grid(True, linestyle="--", alpha=0.3)
    
    return fig

# Display blank graph initially
with graph_placeholder.container():
    st.pyplot(create_blank_graph())

# Add some spacing
st.write("")
st.write("")

# Create bottom section with sliders and button
col1, col2 = st.columns(2)

with col1:
    mins = st.slider("Minimum Minutes Played", 0, 3000, 500, step=50)

with col2:
    min_prog_pass = st.slider("Minimum Progressive Passes", 0, 200, 30, step=5)

# Center the button
col_left, col_center, col_right = st.columns([1, 1, 1])

with col_center:
    generate_button = st.button(
        "Generate Graph", 
        type="primary",
        use_container_width=True
    )

# Core Logic
if generate_button:
    defenders = [
        "DF",
        "DF,MF",
        "MF,DF",
        "DF,FW",
    ]

    # Assigning the Filter and axis's
    filt = df.loc[
        df["position"].isin(defenders)
        & (df["minutes"] >= mins)
        & (df["progressive_passes"] >= min_prog_pass)
    ]

    x = filt["progressive_passes"]
    y = filt["progressive_carries"]

    # Creating & Designing the Scatter Plot
    colors = [
        "#ff2d96",
        "#faff00",
        "#00ffff",
        "#ff7300",
        "#00ff66",
        "#4ac8ff",
        "#c77dff",
        "#ff4d4d",
        "#1abc9c",
        "#f1c40f",
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#0e1a26")
    ax.set_facecolor("#0e1a26")

    for i, (x_val, y_val) in enumerate(zip(x, y)):
        ax.scatter(x_val, y_val, color=colors[i % len(colors)])

    for spine in ax.spines.values():
        spine.set_color("white")
    ax.tick_params(colors="white")
    
    # To add Player names to the Label Points
    for i, idx in enumerate(filt.index):
        player_name = filt.loc[idx, "name"]
        ax.annotate(player_name, (x.iloc[i], y.iloc[i]), fontsize=8, color="silver")

    ax.set_xlabel("Progression via Pass (Season Total)", color="white")
    ax.set_ylabel("Progression via Carry (Season Total)", color="white")
    ax.set_title("Ball Progression - Pass + Carry", color="white")
    ax.grid(True, linestyle="--", alpha=0.3)

    # Update the graph placeholder with the new graph
    with graph_placeholder.container():
        st.pyplot(fig)