import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np


st.set_page_config(page_title="Attacking Efficiency", layout="wide")

st.markdown("<h1 style='text-align: center;'>⚔️ Attacking Efficiency Dashboard</h1>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("player_possession_stats.csv")

df = load_data()

# Calculate success rate and other metrics
df['take_on_success_rate'] = df['successful_take_ons'] / df['attempted_take_ons']
df['dispossessed_rate'] = df['takeons_tackled'] / df['attempted_take_ons']  # per 90 minutes

st.write("---")

# VISUALIZATION 1: Success Rate Bar Chart
st.markdown("## 📊 Top 20 Players by Take-On Success Rate")

# Filter top 20 by attempted take-ons
filt_success = df.sort_values(by='attempted_take_ons', ascending=False).head(20)

fig1 = go.Figure()

for i, idx in enumerate(filt_success.index):
    player_data = filt_success.loc[idx]
    player_name = player_data['player']
    team = player_data['team'] if 'team' in player_data else "Unknown"
    position = player_data['position'] if 'position' in player_data else "Unknown"
    success_rate = player_data['take_on_success_rate']
    attempted = player_data['attempted_take_ons']
    successful = player_data['successful_take_ons']
    
    fig1.add_trace(go.Bar(
        y=[player_name],
        x=[success_rate],
        orientation='h',
        marker_color='#ff2d96',
        name=player_name,
        hovertemplate=f"""
        Player: {player_name}<br>
        Team: {team}<br>
        Position: {position}<br>
        Success Rate: {success_rate:.2%}<br>
        Attempted Take-Ons: {attempted}<br>
        Successful Take-Ons: {successful}<br>
        <extra></extra>
        """,
        showlegend=False
    ))

fig1.update_layout(
    plot_bgcolor='#0e1a26',
    paper_bgcolor='#0e1a26',
    font_color='white',
    title={
        'text': 'Take-On Success Rate - Top 20 Most Active Dribblers',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'color': 'white', 'size': 18}
    },
    xaxis=dict(
        title='Success Rate (%)',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=False,
        tickformat='.0%'
    ),
    yaxis=dict(
        title='',
        color='white',
        autorange='reversed'
    ),
    height=700
)

st.plotly_chart(fig1, use_container_width=True)

# Analysis for Visualization 1
st.markdown("""
### 🔍 Analysis: Take-On Success Rates
This chart reveals the **efficiency** of the most active dribblers in the Premier League. Key insights:

- **Elite Dribblers**: Players with success rates above 60% demonstrate exceptional close control and decision-making
- **Volume vs Quality**: Some players attempt many take-ons but have lower success rates, indicating a more direct, risk-taking approach
- **Position Impact**: Wingers and attacking midfielders typically appear here, as they're expected to beat defenders in wide areas
- **Tactical Value**: High success rates suggest players who can consistently progress the ball and create numerical advantages

**What to Look For**: Players combining high attempt volumes with good success rates are particularly valuable for breaking down defensive structures.
""")

st.write("---")

# VISUALIZATION 2: Bubble Chart
st.markdown("## 🫧 Take-On Efficiency Bubble Chart")

# Use top 50 players for bubble chart to show more variety
filt_bubble = df.nlargest(50, 'attempted_take_ons')

# Create color mapping for positions
position_colors = {
    'FW': '#ff2d96',
    'MF': '#00ff66', 
    'DF': '#4ac8ff',
    'FW,MF': '#faff00',
    'MF,FW': '#ff7300',
    'DF,MF': '#c77dff',
    'MF,DF': '#ff4d4d'
}

fig2 = go.Figure()

for position in filt_bubble['position'].unique():
    if pd.isna(position):
        continue
        
    pos_data = filt_bubble[filt_bubble['position'] == position]
    
    fig2.add_trace(go.Scatter(
        x=pos_data['attempted_take_ons'],
        y=pos_data['take_on_success_rate'],
        mode='markers',
        marker=dict(
            size=pos_data['successful_take_ons'] * 2,  # Bubble size based on successful take-ons
            color=position_colors.get(position, '#ffffff'),
            opacity=0.7,
            line=dict(width=2, color='white')
        ),
        name=position,
        text=pos_data['player'],
        customdata=np.column_stack((
            pos_data['team'] if 'team' in pos_data else 'Unknown',
            pos_data['attempted_take_ons'],
            pos_data['successful_take_ons'],
            pos_data['takeons_tackled'] if 'takeons_tackled' in pos_data else 0
        )),
        hovertemplate="""
        <b>%{text}</b><br>
        Team: %{customdata[0]}<br>
        Position: """ + position + """<br>
        Attempted Take-Ons: %{x}<br>
        Success Rate: %{y:.1%}<br>
        Successful Take-Ons: %{customdata[2]}<br>
        Times Dispossessed: %{customdata[3]}<br>
        <extra></extra>
        """
    ))

fig2.update_layout(
    plot_bgcolor='#0e1a26',
    paper_bgcolor='#0e1a26',
    font_color='white',
    title={
        'text': 'Take-On Efficiency: Volume vs Success Rate',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'color': 'white', 'size': 18}
    },
    xaxis=dict(
        title='Attempted Take-Ons (Volume)',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=False
    ),
    yaxis=dict(
        title='Success Rate',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=False,
        tickformat='.0%'
    ),
    legend=dict(
        bgcolor='rgba(255,255,255,0.2)',
        bordercolor='white',
        borderwidth=2,
        font=dict(
            color='white',
            size=14,
            family='Arial Black'
        ),
        itemsizing='constant'
    ),
    height=600
)

st.plotly_chart(fig2, use_container_width=True)

# Analysis for Visualization 2
st.markdown("""
### 🔍 Analysis: Volume vs Efficiency Balance
This bubble chart reveals the relationship between **dribbling frequency**, **success rate**, and **total output**:

- **Top-Right Quadrant**: Elite dribblers who attempt many take-ons AND succeed frequently - these are game-changers
- **Bubble Size**: Represents successful take-ons completed - larger bubbles show higher absolute contribution
- **Position Clustering**: Forwards (pink) often cluster in high-volume areas, while defenders (blue) are more conservative
- **Sweet Spot**: Players with 40+ attempts and 55%+ success rate represent the optimal balance of risk and reward

**Tactical Insight**: The ideal attacking player appears in the top-right with a large bubble - high volume, high efficiency, high output.
""")

st.write("---")

# VISUALIZATION 3: Mirror Bar Chart
st.markdown("## ⚖️ Efficiency vs Risk Balance")

# Filter top 15 for cleaner mirror chart
filt_mirror = df.nlargest(20, 'attempted_take_ons')
filt_mirror = filt_mirror.sort_values('take_on_success_rate', ascending=True)

fig3 = go.Figure()

# Success rate bars (positive)
fig3.add_trace(go.Bar(
    y=filt_mirror['player'],
    x=filt_mirror['take_on_success_rate'],
    orientation='h',
    name='Success Rate',
    marker_color='#00ff66',
    customdata=np.column_stack((
        filt_mirror['team'] if 'team' in filt_mirror else 'Unknown',
        filt_mirror['attempted_take_ons'],
        filt_mirror['successful_take_ons']
    )),
    hovertemplate="""
    <b>%{y}</b><br>
    Team: %{customdata[0]}<br>
    Success Rate: %{x:.1%}<br>
    Attempted: %{customdata[1]}<br>
    Successful: %{customdata[2]}<br>
    <extra></extra>
    """
))

# Dispossessed rate bars (negative)
fig3.add_trace(go.Bar(
    y=filt_mirror['player'],
    x=-filt_mirror['dispossessed_rate'],  # Negative for mirror effect
    orientation='h',
    name='Dispossessed Rate (per 90)',
    marker_color='#ff2d96',
    customdata=np.column_stack((
        filt_mirror['team'] if 'team' in filt_mirror else 'Unknown',
        filt_mirror['dispossessed_rate'],
        filt_mirror['takeons_tackled'] if 'takeons_tackled' in filt_mirror else 0
    )),
    hovertemplate="""
    <b>%{y}</b><br>
    Team: %{customdata[0]}<br>
    Dispossessed Rate: %{customdata[1]:.1f} per 90min<br>
    Total Dispossessed: %{customdata[2]}<br>
    <extra></extra>
    """
))

fig3.update_layout(
    plot_bgcolor='#0e1a26',
    paper_bgcolor='#0e1a26',
    font_color='white',
    title={
        'text': 'Risk vs Reward: Success Rate vs Dispossession Rate',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'color': 'white', 'size': 18}
    },
    xaxis=dict(
        title='← Dispossessed Rate (per 90) | Success Rate →',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=True,
        zerolinecolor='white',
        zerolinewidth=2
    ),
    yaxis=dict(
        title='',
        color='white'
    ),
    legend=dict(
        bgcolor='rgba(255,255,255,0.2)',
        bordercolor='white',
        borderwidth=2,
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5,
        font=dict(
            color='white',
            size=14,
            family='Arial Black'
        ),
        itemsizing='constant'
    ),
    height=600,
    barmode='overlay'
)

# Add annotations
fig3.add_annotation(
    x=0.3, y=len(filt_mirror) + 1,
    text="🟢 EFFICIENT",
    showarrow=False,
    font=dict(size=14, color='#00ff66'),
    bgcolor='rgba(0,255,102,0.1)',
    bordercolor='#00ff66',
    borderwidth=1
)

fig3.add_annotation(
    x=-1, y=len(filt_mirror) + 1,
    text="🔴 RISKY",
    showarrow=False,
    font=dict(size=14, color='#ff2d96'),
    bgcolor='rgba(255,45,150,0.1)',
    bordercolor='#ff2d96',
    borderwidth=1
)

st.plotly_chart(fig3, use_container_width=True)

# Analysis for Visualization 3
st.markdown("""
### 🔍 Analysis: Risk-Reward Balance
This mirror chart shows the **trade-off** between attacking success and possession loss:

- **Right Side (Green)**: Success rate - how often players successfully complete take-ons
- **Left Side (Red)**: Dispossession rate - how often players lose the ball when attempting to dribble
- **Balanced Players**: Those with long green bars and short red bars offer the best risk-reward ratio
- **High-Risk Players**: Long red bars indicate players who frequently lose possession, which can disrupt team flow

**Key Insight**: The most valuable attackers maximize their green bar while minimizing their red bar. Players heavily skewed to the right are safe but effective, while those with prominent red bars are exciting but potentially costly.

""")

# Summary section
st.write("---")
st.markdown("## 📈 Dashboard Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **Chart 1: Success Rates**
    Identifies the most efficient dribblers among high-volume players
    """)

with col2:
    st.info("""
    **Chart 2: Bubble Analysis**  
    Shows the relationship between volume, efficiency, and total output
    """)

with col3:
    st.info("""
    **Chart 3: Risk vs Reward**
    Balances attacking success against possession loss risk
    """)

# Back to homepage button
st.write("---")
if st.button("🏠 Back to Homepage"):
    st.switch_page("app.py")