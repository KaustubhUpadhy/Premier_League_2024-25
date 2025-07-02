import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from urllib.parse import parse_qs

st.set_page_config(page_title="Team Analysis", layout="wide")

# Get team parameter from URL (if available)
try:
    query_params = st.query_params
    selected_team = query_params.get('team', 'Liverpool').replace('_', ' ')
except:
    selected_team = 'Liverpool'

st.markdown(f"<h1 style='text-align: center;'>{selected_team} - Team Analysis</h1>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("player_stats.csv")
    except:
        return pd.DataFrame()

@st.cache_data
def load_standings():
    try:
        return pd.read_csv("standings.csv")
    except:
        return pd.DataFrame()

df = load_data()
standings_df = load_standings()

if df.empty:
    st.error("Player stats data not found. Please ensure 'player_stats.csv' exists.")
    st.stop()

# Team selector (fallback if URL parameter doesn't work)
if 'team' in df.columns:
    available_teams = sorted(df['team'].unique())
    if selected_team not in available_teams:
        selected_team = available_teams[0]
    
    selected_team = st.selectbox("Select Team", available_teams, 
                                index=available_teams.index(selected_team) if selected_team in available_teams else 0)

    # Filter data for selected team
    team_data = df[df['team'] == selected_team].copy()
    
    if team_data.empty:
        st.warning(f"No data found for {selected_team}")
        st.stop()
    
    # Team Overview Section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_players = len(team_data)
        st.metric("Total Players", total_players)
    
    with col2:
        if 'goals' in team_data.columns:
            total_goals = team_data['goals'].sum()
            st.metric("Team Goals", int(total_goals))
    
    with col3:
        if 'assists' in team_data.columns:
            total_assists = team_data['assists'].sum()
            st.metric("Team Assists", int(total_assists))
    
    with col4:
        if 'minutes' in team_data.columns:
            avg_minutes = team_data['minutes'].mean()
            st.metric("Avg Minutes/Player", f"{avg_minutes:.0f}")
    
    st.write("---")
    
    # Team Position Analysis
    if 'position' in team_data.columns:
        st.markdown("### 📊 Squad Composition")
        
        # Position distribution
        position_counts = team_data['position'].value_counts()
        
        fig = go.Figure(data=[
            go.Bar(
                x=position_counts.index,
                y=position_counts.values,
                marker_color='#37003c',
                text=position_counts.values,
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title=f"{selected_team} - Players by Position",
            xaxis_title="Position",
            yaxis_title="Number of Players",
            plot_bgcolor='white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Players Section
    st.write("---")
    st.markdown("### 🌟 Top Performers")
    
    # Top scorers
    if 'goals' in team_data.columns:
        top_scorers = team_data.nlargest(5, 'goals')[['name', 'goals', 'position']]
        if not top_scorers.empty:
            st.markdown("**🥅 Top Scorers:**")
            st.dataframe(top_scorers, hide_index=True, use_container_width=True)
    
    # Top assisters
    if 'assists' in team_data.columns:
        top_assisters = team_data.nlargest(5, 'assists')[['name', 'assists', 'position']]
        if not top_assisters.empty:
            st.markdown("**🎯 Top Assisters:**")
            st.dataframe(top_assisters, hide_index=True, use_container_width=True)
    
    # Most minutes played
    if 'minutes' in team_data.columns:
        most_minutes = team_data.nlargest(5, 'minutes')[['name', 'minutes', 'position']]
        if not most_minutes.empty:
            st.markdown("**⏱️ Most Minutes Played:**")
            st.dataframe(most_minutes, hide_index=True, use_container_width=True)
    
    st.write("---")
    
    # Full Squad Table
    st.markdown("### 👥 Full Squad")
    
    # Select relevant columns for display
    display_cols = ['name', 'position']
    if 'goals' in team_data.columns:
        display_cols.append('goals')
    if 'assists' in team_data.columns:
        display_cols.append('assists')
    if 'minutes' in team_data.columns:
        display_cols.append('minutes')
    
    squad_display = team_data[display_cols].sort_values('minutes', ascending=False) if 'minutes' in display_cols else team_data[display_cols]
    
    st.dataframe(squad_display, hide_index=True, use_container_width=True)

else:
    st.error("Team information not found in the dataset. Please check your data structure.")

# Back to homepage button
st.write("---")
if st.button("🏠 Back to Homepage"):
    st.switch_page("app.py")