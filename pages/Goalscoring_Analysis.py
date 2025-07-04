import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np


st.set_page_config(page_title="Goalscoring Analysis", layout="wide")

st.markdown("<h1 style='text-align: center;'>Goalscoring Analysis </h1>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("player_stats.csv")

df = load_data()

# Create calculated columns
df["Goal_Involvements"] = df['goals'] + df['assists']
df["Goal_Involvements_per"] = (df['goals'] + df['assists']) / (df['minutes'] / 90)
df["recv_per"] = df['received_progressive_passes'] / (df['minutes'] / 90)

# Analysis selection
st.write("")
analysis_type = st.selectbox(
    "Select Analysis Type",
    ["Goals vs Expected Goals", "Goal Involvements per 90", "Progressive Pass Recipients"],
    index=0
)

st.write("---")

# Colors for consistency
colors = ['#ff2d96', '#faff00', '#00ffff', '#ff7300', '#00ff66',
          '#4ac8ff', '#c77dff', '#ff4d4d', '#1abc9c', '#f1c40f']

# Analysis 1: Goals vs Expected Goals (Scatter Plot)
if analysis_type == "Goals vs Expected Goals":
    st.markdown("### Premier League 2024-25: Goals vs Expected Goals Comparison ")
    stat_choice = st.selectbox("Choose how many Goal Scorers (Sorted by Top):", [10,20,30,40,50,"All"])
    # Filter top 30 scorers
    if stat_choice==int:
        top_scorers = df.sort_values(by='goals', ascending=False).head(stat_choice)
    elif stat_choice=="All":
        top_scorers = df.sort_values(by='goals', ascending=False)
    else:
        top_scorers = df.sort_values(by='goals', ascending=False).head(25)
    fig = go.Figure()
    
    # Add scatter points
    for i, idx in enumerate(top_scorers.index):
        player_data = top_scorers.loc[idx]
        player_name = player_data['name']
        team = player_data['team'] if 'team' in player_data else "Unknown"
        position = player_data['position'] if 'position' in player_data else "Unknown"
        minutes = player_data['minutes']
        goals = player_data['goals']
        xg = player_data['expected_goals']
        
        # Determine if overperforming or underperforming
        performance = "Overperforming" if goals > xg else "Underperforming" if goals < xg else "On Target"
        
        fig.add_trace(go.Scatter(
            x=[xg],
            y=[goals],
            mode='markers+text',
            marker=dict(
                color=colors[i % len(colors)],
                size=16,
                line=dict(width=1, color='rgba(255,255,255,0.3)')
            ),
            text=player_name,
            textposition="top center",
            textfont=dict(size=16, color='silver'),
            name=player_name,
            hovertemplate=f"""
            Player: {player_name}<br>
            Team: {team}<br>
            Position: {position}<br>
            Minutes: {minutes}<br>
            Goals: {goals}<br>
            Expected Goals: {xg:.2f}<br>
            Performance: {performance}<br>
            <extra></extra>
            """,
            showlegend=False
        ))
    
    # Add diagonal line for expected = actual
    min_val = min(df['expected_goals'].min(), df['goals'].min())
    max_val = max(df['expected_goals'].max(), df['goals'].max())
    
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        line=dict(color='#00ff00', width=2),
        name='Expected = Actual',
        showlegend=True
    ))
    
    # Add performance zone annotations
    fig.add_annotation(
        x=max_val * 0.5, y=max_val * 0.2,
        text="Underperforming",
        showarrow=False,
        font=dict(size=24, color='#ff2d96'),
        opacity=0.8
    )
    
    fig.add_annotation(
        x=max_val * 0.1, y=max_val * 0.9,
        text="Overperforming",
        showarrow=False,
        font=dict(size=24, color='#ff2d96'),
        opacity=0.8
    )
    
    fig.update_layout(
        plot_bgcolor='#0e1a26',
        paper_bgcolor='#0e1a26',
        font_color='white',
        title={
            'text': 'Goals vs Expected Goals Comparison',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white', 'size': 24}
        },
        xaxis=dict(
            title='Expected Goals (xG)',
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='Goals Scored',
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white',
            showgrid=True,
            zeroline=False
        ),
        hovermode='closest',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Analysis 2: Goal Involvements per 90 (Horizontal Bar Chart)
elif analysis_type == "Goal Involvements per 90":
    st.markdown("### Top 20 Players by Goal Involvement per 90 Minutes")
    
    # Filter top 20 by goal involvements
    filt = df.sort_values(by='Goal_Involvements', ascending=False).head(20)
    
    fig = go.Figure()
    
    for i, idx in enumerate(filt.index):
        player_data = filt.loc[idx]
        player_name = player_data['name']
        team = player_data['team'] if 'team' in player_data else "Unknown"
        position = player_data['position'] if 'position' in player_data else "Unknown"
        minutes = player_data['minutes']
        goals = player_data['goals']
        assists = player_data['assists']
        goal_inv_per90 = player_data['Goal_Involvements_per']
        
        fig.add_trace(go.Bar(
            y=[player_name],
            x=[goal_inv_per90],
            orientation='h',
            marker_color='#ff2d96',
            name=player_name,
            hovertemplate=f"""
            Player: {player_name}<br>
            Team: {team}<br>
            Position: {position}<br>
            Minutes: {minutes}<br>
            Goals: {goals}<br>
            Assists: {assists}<br>
            Goal Involvements per 90: {goal_inv_per90:.2f}<br>
            <extra></extra>
            """,
            showlegend=False
        ))
    
    fig.update_layout(
        plot_bgcolor='#0e1a26',
        paper_bgcolor='#0e1a26',
        font_color='white',
        title={
            'text': 'Top 20 Players by Goal Involvement per 90 Minutes',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white', 'size': 18}
        },
        xaxis=dict(
            title='Goal Involvement per 90',
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='',
            color='white',
            autorange='reversed'  # This inverts the y-axis like plt.gca().invert_yaxis()
        ),
        height=800
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Analysis 3: Progressive Pass Recipients (Horizontal Bar Chart)
elif analysis_type == "Progressive Pass Recipients":
    st.markdown("### Top 20 Recipients of Progressive Passes per 90")
    
    # Filter top 20 by received progressive passes
    filt = df.sort_values(by='received_progressive_passes', ascending=False).head(20)
    
    fig = go.Figure()
    
    for i, idx in enumerate(filt.index):
        player_data = filt.loc[idx]
        player_name = player_data['name']
        team = player_data['team'] if 'team' in player_data else "Unknown"
        position = player_data['position'] if 'position' in player_data else "Unknown"
        minutes = player_data['minutes']
        recv_prog_passes = player_data['received_progressive_passes']
        recv_per90 = player_data['recv_per']
        
        fig.add_trace(go.Bar(
            y=[player_name],
            x=[recv_per90],
            orientation='h',
            marker_color='#00ff66',
            name=player_name,
            hovertemplate=f"""
            Player: {player_name}<br>
            Team: {team}<br>
            Position: {position}<br>
            Minutes: {minutes}<br>
            Progressive Passes Received: {recv_prog_passes}<br>
            Received per 90: {recv_per90:.2f}<br>
            <extra></extra>
            """,
            showlegend=False
        ))
    
    fig.update_layout(
        plot_bgcolor='#0e1a26',
        paper_bgcolor='#0e1a26',
        font_color='white',
        title={
            'text': 'Top 20 Recipients of Progressive Passes per 90',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': 'white', 'size': 18}
        },
        xaxis=dict(
            title='Received Progressive Passes per 90',
            gridcolor='rgba(255,255,255,0.3)',
            gridwidth=1,
            color='white',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='',
            color='white',
            autorange='reversed'  # This inverts the y-axis
        ),
        height=800
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Add some insights at the bottom
st.write("---")
st.markdown("### 📊 Analysis Insights")

if analysis_type == "Goals vs Expected Goals":
    st.info("""
    **Understanding the Comparison:**
    - Players above the green line are **overperforming** their expected goals
    - Players below the line are **underperforming** their expected goals
    - The diagonal line represents perfect efficiency (Goals = Expected Goals)
    """)
elif analysis_type == "Goal Involvements per 90":
    st.info("""
    **Understanding Goal Involvements:**
    - Combines goals and assists to show overall attacking contribution
    - Normalized per 90 minutes for fair comparison across different playing times
    - Higher values indicate more consistent attacking output
    """)
else:
    st.info("""
    **Understanding Progressive Pass Reception:**
    - Shows players who receive the most progressive passes
    - Indicates players who are frequently found in advanced positions
    - Key metric for understanding attacking movement and positioning
    """)