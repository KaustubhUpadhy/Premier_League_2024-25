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
def create_blank_graph(view_type="Season Total"):
    fig = go.Figure()
    
    x_title = f'Progression via Pass ({view_type})'
    y_title = f'Progression via Carry ({view_type})'
    title_text = f'Ball Progression {view_type} - Pass + Carry'
    
    fig.update_layout(
        plot_bgcolor='#0e1a26',
        paper_bgcolor='#0e1a26',
        font_color='white',
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white', 'size': 16}
        },
        xaxis=dict(
            title=x_title,
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=y_title,
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white',
            showgrid=True,
            zeroline=False
        ),
        showlegend=False,
        width=800,
        height=500
    )
    
    return fig

# Add per 90 checkbox at the top
st.write("")
col_view1, col_view2, col_view3 = st.columns([1, 1, 1])
with col_view2:
    per_90_mode = st.checkbox("📊 Per 90 Stats", value=False)

# Display blank graph initially
view_type = "Per 90" if per_90_mode else "Season Total"
with graph_placeholder.container():
    st.plotly_chart(create_blank_graph(view_type), use_container_width=True)

# Add some spacing
st.write("")
st.write("")

# Create bottom section with sliders and button
col1, col2, col3 = st.columns(3)

with col1:
    mins = st.slider("Minimum Minutes Played", 0, 3000, 500, step=50)

with col2:
    min_prog_pass = st.slider("Minimum Progressive Passes", 0, 200, 30, step=5)

with col3:
    min_prog_carry = st.slider("Minimum Progressive Carries", 0, 200, 20, step=5)

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

    # Assigning the Filter with all three parameters
    filt = df.loc[
        df["position"].isin(defenders)
        & (df["minutes"] >= mins)
        & (df["progressive_passes"] >= min_prog_pass)
        & (df["progressive_carries"] >= min_prog_carry)
    ]

    # Determine x and y values based on checkbox state
    if per_90_mode:
        # Calculate per 90 values
        filt = filt.copy()  # Avoid SettingWithCopyWarning
        filt["progressive_passes_per90"] = (
            (filt["progressive_passes"] / filt["minutes"]) * 90
        ).round(2)
        filt["progressive_carries_per90"] = (
            (filt["progressive_carries"] / filt["minutes"]) * 90
        ).round(2)
        
        x = filt["progressive_passes_per90"]
        y = filt["progressive_carries_per90"]
        x_title = "Progression via Pass (Per 90)"
        y_title = "Progression via Carry (Per 90)"
        title_text = "Ball Progression Per 90 - Pass + Carry"
        value_suffix = " (Per 90)"
    else:
        x = filt["progressive_passes"]
        y = filt["progressive_carries"]
        x_title = "Progression via Pass (Season Total)"
        y_title = "Progression via Carry (Season Total)"
        title_text = "Ball Progression - Pass + Carry"
        value_suffix = ""

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
            Player Name: {player_name}<br>
            Team: {team}<br>
            Position: {position}<br>
            Minutes: {minutes}<br>
            Progressive Passes{value_suffix}: {x.iloc[i]}<br>
            Progressive Carries{value_suffix}: {y.iloc[i]}<br>
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
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white', 'size': 18}
        },
        xaxis=dict(
            title=x_title,
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=y_title,
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white',
            showgrid=True,
            zeroline=False
        ),
        hovermode='closest',
        width=800,
        height=800
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