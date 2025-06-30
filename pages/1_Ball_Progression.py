import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st 


st.set_page_config(page_title="Ball Progression", layout="wide")

st.markdown("<h1 style='text-align: center;'>Ball Progression: Pass + Carry</h1>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("player_stats.csv")

df = load_data()

# Create placeholder for graph at top
graph_placeholder = st.empty()

# Create initial blank graph
def create_blank_graph():
    fig = go.Figure()
    
    fig.update_layout(
        plot_bgcolor='#0e1a26',
        paper_bgcolor='#0e1a26',
        font_color='white',
        title={
            'text': 'Ball Progression - Pass + Carry',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white', 'size': 16}
        },
        xaxis=dict(
            title='Progression via Pass (Season Total)',
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white'
        ),
        yaxis=dict(
            title='Progression via Carry (Season Total)',
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white'
        ),
        showlegend=False,
        width=800,
        height=500
    )
    
    return fig

# Display blank graph initially
with graph_placeholder.container():
    st.plotly_chart(create_blank_graph(), use_container_width=True)

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

    # Creating & Designing the Interactive Scatter Plot with Plotly
    colors = [
        "#ff2d96", "#faff00", "#00ffff", "#ff7300", "#00ff66",
        "#4ac8ff", "#c77dff", "#ff4d4d", "#1abc9c", "#f1c40f"
    ]
    
    # Create the plotly figure
    fig = go.Figure()
    
    # Add scatter points with hover information
    for i, idx in enumerate(filt.index):
        player_name = filt.loc[idx, "name"]
        team = filt.loc[idx, "team"] if "team" in filt.columns else "Unknown"
        position = filt.loc[idx, "position"]
        minutes = filt.loc[idx, "minutes"]
        
        fig.add_trace(go.Scatter(
            x=[x.iloc[i]],
            y=[y.iloc[i]],
            mode='markers+text',
            marker=dict(
                color=colors[i % len(colors)],
                size=8,
                line=dict(width=1, color='rgba(255,255,255,0.3)')
            ),
            text=player_name,
            textposition="top center",
            textfont=dict(
                size=16,
                color='white'
            ),
            name=player_name,
            hovertemplate=f"""
            <span style="color:{colors[i % len(colors)]}"></span>
            Team: {team}<br>
            Position: {position}<br>
            Minutes: {minutes}<br>
            Progressive Passes: {x.iloc[i]}<br>
            Progressive Carries: {y.iloc[i]}<br>
            <extra></extra>
            """,
            showlegend=False
        ))
    
    # Update layout to match matplotlib styling
    fig.update_layout(
        plot_bgcolor='#0e1a26',
        paper_bgcolor='#0e1a26',
        font_color='white',
        title={
            'text': 'Ball Progression - Pass + Carry',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white', 'size': 18}
        },
        xaxis=dict(
            title='Progression via Pass (Season Total)',
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='Progression via Carry (Season Total)',
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white',
            showgrid=True,
            zeroline=False
        ),
        hovermode='closest',
        width=800,
        height=500
    )
    
    # Add hover effects for text enlargement
    fig.update_traces(
        hoverlabel=dict(
            bgcolor="rgba(0,0,0,0.8)",
            bordercolor="white",
            font_size=12,
            font_color="white"
        )
    )

    # Update the graph placeholder with the new interactive graph
    with graph_placeholder.container():
        st.plotly_chart(fig, use_container_width=True)