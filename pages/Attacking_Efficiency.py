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
    possession_df = pd.read_csv("player_possession_stats.csv")
    player_df = pd.read_csv("player_stats.csv")
    return possession_df, player_df

df, player_df = load_data()

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
This chart reveals the **efficiency** of the most active dribblers in the Premier League.

- **Elite Dribblers**: Players with success rates above 50% demonstrate exceptional close control and decision-making
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
This bubble chart reveals the relationship between **dribbling frequency**, **success rate**, and **total output** based on top 50 players by Attempted Take ons:

- **Top-Right Quadrant**: Elite dribblers who attempt many take-ons AND succeed frequently - these are game-changers
- **Bubble Size**: Represents successful take-ons completed - larger bubbles show higher absolute contribution
- **Sweet Spot**: Players with 50+ attempts and 45%+ success rate represent the optimal balance of risk and reward

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
    x=-1.5, y=len(filt_mirror) + 1,
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

**Key Insight**: The most valuable attackers maximize their green bar while minimizing their red bar. Players heavily skewed to the right are safe but effective, while those with prominent red bars are exciting but potentially costly.
""")

st.write("---")

# VISUALIZATION 4: Dribbling vs Progression Efficiency
st.markdown("## 🎯 Dribbling vs Progression Efficiency")

# Filter players with at least 70 attempted take-ons, then get top 30
filtered_dribblers = df[df['attempted_take_ons'] >= 70]
top_dribblers = filtered_dribblers.sort_values(by='attempted_take_ons', ascending=False).head(30)

# Merge with player_stats.csv to get progressive_carries data
merged_data = top_dribblers.merge(
    player_df[['name', 'progressive_carries']], 
    left_on='player', 
    right_on='name', 
    how='left'
)

# Calculate progressive carry ratio using carries from possession stats and progressive_carries from player stats
merged_data['progressive_carry_ratio'] = merged_data['progressive_carries'] / merged_data['carries']

# Remove any rows with missing data
merged_data = merged_data.dropna(subset=['progressive_carry_ratio', 'take_on_success_rate'])

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

fig4 = go.Figure()

# Calculate reference lines (median values)
median_takeOn = merged_data['take_on_success_rate'].median()
median_progression = merged_data['progressive_carry_ratio'].median()

# Add scatter points by position
for position in merged_data['position'].unique():
    if pd.isna(position):
        continue
        
    pos_data = merged_data[merged_data['position'] == position]
    
    fig4.add_trace(go.Scatter(
        x=pos_data['take_on_success_rate'],
        y=pos_data['progressive_carry_ratio'],
        mode='markers+text',
        marker=dict(
            size=pos_data['carries'] / 10,  # Size based on total carries
            color=position_colors.get(position, '#ffffff'),
            opacity=0.7,
            line=dict(width=2, color='white')
        ),
        text=pos_data['player'],
        textposition="top center",
        textfont=dict(size=8, color='white'),
        name=position,
        customdata=np.column_stack((
            pos_data['team'] if 'team' in pos_data else 'Unknown',
            pos_data['carries'],
            pos_data['progressive_carries'],
            pos_data['attempted_take_ons'],
            pos_data['successful_take_ons']
        )),
        hovertemplate="""
        <b>%{text}</b><br>
        Team: %{customdata[0]}<br>
        Position: """ + position + """<br>
        Take-On Success Rate: %{x:.1%}<br>
        Progressive Carry Ratio: %{y:.1%}<br>
        Total Carries: %{customdata[1]}<br>
        Progressive Carries: %{customdata[2]}<br>
        Attempted Take-Ons: %{customdata[3]}<br>
        Successful Take-Ons: %{customdata[4]}<br>
        <extra></extra>
        """
    ))

# Add reference lines
fig4.add_hline(y=median_progression, line_dash="dash", line_color="white", 
               annotation_text=f"Median Progression Rate ({median_progression:.1%})",
               annotation_position="bottom right")

fig4.add_vline(x=median_takeOn, line_dash="dash", line_color="white",
               annotation_text=f"Median Take-On Rate ({median_takeOn:.1%})",
               annotation_position="top left")

# Add quadrant annotations
fig4.add_annotation(
    x=merged_data['take_on_success_rate'].max() * 0.9,
    y=merged_data['progressive_carry_ratio'].max() * 0.9,
    text="🔝🔜 ELITE<br>High Dribbling + High Progression",
    showarrow=False,
    font=dict(size=12, color='#00ff66'),
    bgcolor='rgba(0,255,102,0.1)',
    bordercolor='#00ff66',
    borderwidth=1
)

fig4.add_annotation(
    x=merged_data['take_on_success_rate'].min() * 1.1,
    y=merged_data['progressive_carry_ratio'].max() * 0.9,
    text="🔝⬅ TACTICAL<br>Low Dribbling + High Progression",
    showarrow=False,
    font=dict(size=12, color='#faff00'),
    bgcolor='rgba(255,255,0,0.1)',
    bordercolor='#faff00',
    borderwidth=1
)

fig4.add_annotation(
    x=merged_data['take_on_success_rate'].max() * 0.9,
    y=merged_data['progressive_carry_ratio'].min() * 1.1,
    text="⬇➡ SHOWY<br>High Dribbling + Low Progression",
    showarrow=False,
    font=dict(size=12, color='#ff7300'),
    bgcolor='rgba(255,115,0,0.1)',
    bordercolor='#ff7300',
    borderwidth=1
)

fig4.add_annotation(
    x=merged_data['take_on_success_rate'].min() * 1.1,
    y=merged_data['progressive_carry_ratio'].min() * 1.1,
    text="⬇⬅ LIMITED<br>Low Dribbling + Low Progression",
    showarrow=False,
    font=dict(size=12, color='#ff2d96'),
    bgcolor='rgba(255,45,150,0.1)',
    bordercolor='#ff2d96',
    borderwidth=1
)

fig4.update_layout(
    plot_bgcolor='#0e1a26',
    paper_bgcolor='#0e1a26',
    font_color='white',
    title={
        'text': 'Dribbling vs Progression Efficiency - Quadrant Analysis',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'color': 'white', 'size': 18}
    },
    xaxis=dict(
        title='Take-On Success Rate (1v1 Efficiency)',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=False,
        tickformat='.0%'
    ),
    yaxis=dict(
        title='Progressive Carry Ratio (Progression Efficiency)',
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

st.plotly_chart(fig4, use_container_width=True)

# Analysis for Visualization 4
st.markdown("""
### 🔍 Analysis: Dribbling vs Progression Efficiency Quadrants
This quadrant analysis reveals the **dual nature** of ball-carrying effectiveness:

- **🔝🔜 Top-Right (ELITE)**: Players who excel at both beating opponents AND progressing the ball - the complete package
- **🔝⬅ Top-Left (TACTICAL)**: Smart ball progressors who don't rely on 1v1 skills but consistently advance play
- **⬇➡ Bottom-Right (SHOWY)**: Skilled dribblers whose take-ons don't translate to meaningful progression
- **⬇⬅ Bottom-Left (LIMITED)**: Players struggling in both aspects - may need tactical or technical development

""")

# Summary section
st.write("---")
st.markdown("## 📈 Summary")

col1, col2, col3, col4 = st.columns(4)

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

with col4:
    st.info("""
    **Chart 4: Quadrant Analysis**
    Maps dribbling skill against progression effectiveness
    """)

# Back to homepage button
st.write("---")
if st.button("🏠 Back to Homepage"):
    st.switch_page("app.py")