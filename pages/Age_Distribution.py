import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(page_title="Age Distribution", layout="wide")

st.markdown("<h1 style='text-align: center;'>📅 Age Distribution Dashboard</h1>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("player_stats.csv")

df = load_data()

st.write("---")

# VISUALIZATION 1: Minutes by Birth Year and Team
st.markdown("## 🏟️ Minutes Played by Birth Year and Team")

# Group data by birth year and team
filt_team = df.groupby(['born', 'team'])['minutes'].sum().reset_index()

fig1 = px.density_heatmap(
    data_frame=filt_team,
    x='born',
    y='team',
    z='minutes',
    nbinsx=20,
    color_continuous_scale=['#90EE90', '#006400'],
    title='Minutes Played Distribution Across Teams and Birth Years'
)

fig1.update_layout(
    plot_bgcolor='#0e1a26',
    paper_bgcolor='#0e1a26',
    font_color='white',
    title={
        'text': 'Minutes Played Distribution Across Teams and Birth Years',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'color': 'white', 'size': 18}
    },
    xaxis=dict(
        title='Birth Year',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=False
    ),
    yaxis=dict(
        title='Team',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=False
    ),
    coloraxis_colorbar=dict(
        title=dict(text="Minutes Played", font=dict(color='white')),
        tickfont=dict(color='white'),
        bgcolor='rgba(0,0,0,0.5)',
        bordercolor='white',
        borderwidth=1
    ),
    height=600
)

# Add hover template for better interactivity
fig1.update_traces(
    hovertemplate="""
    <b>Team:</b> %{y}<br>
    <b>Birth Year:</b> %{x}<br>
    <b>Total Minutes:</b> %{z:,.0f}<br>
    <extra></extra>
    """
)

st.plotly_chart(fig1, use_container_width=True)

# Analysis for Visualization 1
st.markdown("""
### 🔍 Analysis: Team Age Composition
This heatmap reveals how different teams distribute playing time across age groups:

- **Young Teams**: Teams with darker green in recent birth years (1998-2002) prioritize youth development
- **Experienced Teams**: Concentration in earlier birth years (1988-1995) indicates reliance on veteran players
- **Balanced Squads**: Even distribution across multiple birth years shows good age balance and squad depth
- **Strategic Insights**: Teams heavily investing in specific age brackets reveal their long-term planning approach

**Key Patterns**: Look for teams with concentrated dark areas - these indicate heavy reliance on specific age groups, which could signal either a successful generation or potential future squad planning challenges.
""")

st.write("---")

# VISUALIZATION 2: Minutes by Birth Year and Position
st.markdown("## ⚽ Minutes Played by Birth Year and Position")

# Group data by birth year and position
filt_position = df.groupby(['born', 'position'])['minutes'].sum().reset_index()

fig2 = px.density_heatmap(
    data_frame=filt_position,
    x='born',
    y='position',
    z='minutes',
    nbinsx=20,
    color_continuous_scale=['#90EE90', '#006400'],
    title='Minutes Played Distribution Across Positions and Birth Years'
)

fig2.update_layout(
    plot_bgcolor='#0e1a26',
    paper_bgcolor='#0e1a26',
    font_color='white',
    title={
        'text': 'Minutes Played Distribution Across Positions and Birth Years',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'color': 'white', 'size': 18}
    },
    xaxis=dict(
        title='Birth Year',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=False
    ),
    yaxis=dict(
        title='Position',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=False
    ),
    coloraxis_colorbar=dict(
        title=dict(text="Minutes Played", font=dict(color='white')),
        tickfont=dict(color='white'),
        bgcolor='rgba(0,0,0,0.5)',
        bordercolor='white',
        borderwidth=1
    ),
    height=600
)

# Add hover template for better interactivity
fig2.update_traces(
    hovertemplate="""
    <b>Position:</b> %{y}<br>
    <b>Birth Year:</b> %{x}<br>
    <b>Total Minutes:</b> %{z:,.0f}<br>
    <extra></extra>
    """
)

st.plotly_chart(fig2, use_container_width=True)

# Analysis for Visualization 2
st.markdown("""
### 🔍 Analysis: Positional Age Trends
This heatmap shows how playing time is distributed across positions and age groups:

- **Goalkeeper Patterns**: Typically shows concentration in older age groups (1985-1992) due to the position's longevity requirements
- **Defender Age Profile**: Often peaks in mid-career years (1990-1996) when experience and physicality intersect optimally
- **Midfielder Distribution**: Usually shows the broadest age spread, as the position requires both energy (young) and wisdom (experienced)
- **Forward Evolution**: May show shifts between age groups indicating tactical evolution in the striker role

**Tactical Insights**: Dark green concentrations reveal where the Premier League's positional demands align with player development curves. Gaps in certain position-age combinations might indicate market opportunities or developmental challenges.
""")

# Summary section
st.write("---")
st.markdown("## 📈 Dashboard Summary")

# Calculate some summary statistics
total_players = len(df)
avg_birth_year = df['born'].mean()
current_year = 2024
avg_age = current_year - avg_birth_year

youngest_players = df.nlargest(5, 'born')[['name', 'team', 'born', 'position', 'minutes']]
oldest_players = df.nsmallest(5, 'born')[['name', 'team', 'born', 'position', 'minutes']]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Players Analyzed", total_players)
    st.metric("Average Age", f"{avg_age:.1f} years")

with col2:
    st.markdown("**🔴 Youngest Players (Most Minutes)**")
    st.dataframe(youngest_players, hide_index=True, use_container_width=True)

with col3:
    st.markdown("**🟢 Most Experienced Players (Most Minutes)**")
    st.dataframe(oldest_players, hide_index=True, use_container_width=True)

st.write("---")

# Back to homepage button
st.write("---")
if st.button("🏠 Back to Homepage"):
    st.switch_page("app.py")