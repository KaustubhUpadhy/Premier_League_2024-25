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

# Add per 90 checkbox and position filters
st.write("")
col_view1, col_view2, col_view3 = st.columns([1, 1, 1])
with col_view2:
    per_90_mode = st.checkbox("📊 Per 90 Stats", value=False)

# Position filter checkboxes
st.write("")
st.markdown("**Select Positions to Include:**")
pos_col1, pos_col2, pos_col3 = st.columns(3)

with pos_col1:
    show_defenders = st.checkbox("🛡️ Defenders", value=True)

with pos_col2:
    show_midfielders = st.checkbox("⚽ Midfielders", value=False)

with pos_col3:
    show_forwards = st.checkbox("🎯 Forwards", value=False)

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
    # Position lists
    defenders = ["DF", "DF,MF", "MF,DF", "DF,FW"]
    midfielders = ["MF", "FW,MF", "DF,MF", "MF,DF", "MF,FW"]
    forwards = ["FW,MF", "FW", "FW,DF", "MF,FW", "DF,FW"]
    
    # Build selected positions list based on checkboxes
    selected_positions = []
    if show_defenders:
        selected_positions.extend(defenders)
    if show_midfielders:
        selected_positions.extend(midfielders)
    if show_forwards:
        selected_positions.extend(forwards)
    
    # Remove duplicates while preserving order
    selected_positions = list(dict.fromkeys(selected_positions))
    
    # Check if at least one position is selected
    if not selected_positions:
        st.error("Please select at least one position to display!")
        st.stop()

    # Assigning the Filter with all parameters including position selection
    filt = df.loc[
        df["position"].isin(selected_positions)
        & (df["minutes"] >= mins)
        & (df["progressive_passes"] >= min_prog_pass)
        & (df["progressive_carries"] >= min_prog_carry)
    ]
    
    # Check if filter returns any players
    if filt.empty:
        st.warning("No players match the selected criteria. Try adjusting your filters.")
        st.stop()

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