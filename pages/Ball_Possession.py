import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np


st.set_page_config(page_title="Ball Possession", layout="wide")

st.markdown("<h1 style='text-align: center;'>🏀 Ball Possession Dashboard</h1>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    possession_df = pd.read_csv("player_possession_stats.csv")
    player_df = pd.read_csv("player_stats.csv")
    return possession_df, player_df

df, player_df = load_data()

# Merge to get progressive_carries from player_stats.csv
merged_df = df.merge(
    player_df[['name', 'progressive_carries','minutes']], 
    left_on='player', 
    right_on='name', 
    how='left'
)

st.write("---")

# VISUALIZATION 1: Carries Volume + Progressiveness
st.markdown("## 📊 Carries Volume vs Progressiveness")

# Filter players with meaningful carry data (at least 50 carries) and valid progressive carries data
filt_carries = merged_df[(merged_df['carries'] >= 50) & (merged_df['progressive_carries']>10)&(merged_df['minutes']>1000)]

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

fig1 = go.Figure()

# Add scatter points by position
for position in filt_carries['position'].unique():
    if pd.isna(position):
        continue
        
    pos_data = filt_carries[filt_carries['position'] == position]
    
    fig1.add_trace(go.Scatter(
        x=pos_data['carries'],
        y=pos_data['progressive_carries'],
        mode='markers+text',
        marker=dict(
            size=12,
            color=position_colors.get(position, '#ffffff'),
            opacity=0.7,
            line=dict(width=2, color='white')
        ),
        text=pos_data['player'],
        textposition="top center",
        textfont=dict(size=8, color='white'),
        name=position,
        customdata=np.column_stack((
            pos_data['team'].values if 'team' in pos_data.columns else ['Unknown'] * len(pos_data),
            pos_data['minutes'].values if 'minutes' in pos_data.columns else [0] * len(pos_data),
            (pos_data['progressive_carries'] / pos_data['carries'] * 100).round(1).values
        )),
        hovertemplate="""
        <b>%{text}</b><br>
        Team: %{customdata[0]}<br>
        Position: """ + position + """<br>
        Total Carries: %{x}<br>
        Progressive Carries: %{y}<br>
        Progressive Rate: %{customdata[2]}%<br>
        Minutes Played: %{customdata[1]}<br>
        <extra></extra>
        """
    ))

# Add trend line
if len(filt_carries) > 10:  # Only if we have enough data points
    z = np.polyfit(filt_carries['carries'], filt_carries['progressive_carries'], 1)
    p = np.poly1d(z)
    
    fig1.add_trace(go.Scatter(
        x=sorted(filt_carries['carries']),
        y=p(sorted(filt_carries['carries'])),
        mode='lines',
        name='Trend Line',
        line=dict(color='white', width=2, dash='dash'),
        showlegend=True
    ))

fig1.update_layout(
    plot_bgcolor='#0e1a26',
    paper_bgcolor='#0e1a26',
    font_color='white',
    title={
        'text': 'Ball Carries: Volume vs Progressive Impact',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'color': 'white', 'size': 18}
    },
    xaxis=dict(
        title='Total Carries (Volume)',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=False
    ),
    yaxis=dict(
        title='Progressive Carries (Effectiveness)',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=False
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

st.plotly_chart(fig1, use_container_width=True)

# Analysis for Visualization 1
st.markdown("""
### 🔍 Analysis: Volume vs Progressive Impact
This scatter plot reveals the relationship between **carry frequency** and **progressive effectiveness**:

- **High Volume + High Progression**: Players in the top-right are the ultimate ball carriers - frequent AND progressive
- **Volume Specialists**: High total carries but lower progressive carries - secure ball retention focus
- **Progressive Specialists**: Fewer total carries but high progressive rate - quality over quantity approach
- **Trend Line**: Shows the general relationship between volume and progression across the league

**Key Insights**:
- **Defenders (Blue)**: Often cluster in lower-left - fewer carries, more conservative
- **Midfielders (Green)**: Spread across the spectrum - varying tactical roles
- **Forwards (Pink)**: Often higher progression rate - direct play orientation

**Tactical Application**: Identify players who combine high carry volume with progressive impact for key playmaking roles.
""")

st.write("---")

# VISUALIZATION 2: Top Ball Carriers by Total Distance
st.markdown("## 🏃‍♂️ Top Ball Carriers by Total Distance")

# Filter players with meaningful distance data and get top 25
filt_distance = df[df['total_distance_carried'] > 0].nlargest(25, 'total_distance_carried')

fig2 = go.Figure()

for i, idx in enumerate(filt_distance.index):
    player_data = filt_distance.loc[idx]
    player_name = player_data['player']
    team = player_data['team'] if 'team' in player_data else "Unknown"
    position = player_data['position'] if 'position' in player_data else "Unknown"
    total_distance = player_data['total_distance_carried']
    carries = player_data['carries']
    minutes = player_data['minutes'] if 'minutes' in player_data else 0
    avg_distance_per_carry = total_distance / carries if carries > 0 else 0
    
    fig2.add_trace(go.Bar(
        y=[player_name],
        x=[total_distance],
        orientation='h',
        marker_color='#00ff66',
        name=player_name,
        customdata=np.column_stack([[carries], [minutes], [avg_distance_per_carry]]),
        hovertemplate=f"""
        Player: {player_name}<br>
        Team: {team}<br>
        Position: {position}<br>
        Total Distance: {total_distance:,.0f}m<br>
        Total Carries: {carries}<br>
        Minutes: {minutes}<br>
        Avg Distance/Carry: {avg_distance_per_carry:.1f}m<br>
        <extra></extra>
        """,
        showlegend=False
    ))

fig2.update_layout(
    plot_bgcolor='#0e1a26',
    paper_bgcolor='#0e1a26',
    font_color='white',
    title={
        'text': 'Top 25 Ball Carriers by Total Distance Covered',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'color': 'white', 'size': 18}
    },
    xaxis=dict(
        title='Total Distance Carried (meters)',
        gridcolor='rgba(255,255,255,0.3)',
        gridwidth=1,
        color='white',
        showgrid=True,
        zeroline=False
    ),
    yaxis=dict(
        title='',
        color='white',
        autorange='reversed'
    ),
    height=800
)

st.plotly_chart(fig2, use_container_width=True)

# Analysis for Visualization 2
st.markdown("""
### 🔍 Analysis: Distance Coverage Patterns
This chart reveals **who covers the most ground** with the ball and their carrying characteristics:

- **Volume vs Burst Carriers**: Compare total distance with average distance per carry to identify playing styles
- **Endurance Indicators**: High total distance suggests high work rate and ball involvement
- **Efficiency Metrics**: Distance per carry shows whether players take long runs or frequent short carries
- **Position Patterns**: Different positions typically show distinct distance coverage patterns

**Key Patterns**:
- **High Distance + Many Carries**: Workhorses who are constantly involved in ball progression
- **High Distance + Few Carries**: Explosive players who cover significant ground in fewer touches
- **Moderate Distance + Many Carries**: Possession-focused players with frequent but shorter carries

**Strategic Value**: Players with high total distance often serve as key transitional figures, linking defense and attack through ball carrying.
""")

# Summary section
st.write("---")
st.markdown("## 📈 Dashboard Summary")

# Calculate summary statistics
total_carries = merged_df['carries'].sum()
total_progressive = merged_df['progressive_carries'].sum()
avg_progressive_rate = (total_progressive / total_carries * 100) if total_carries > 0 else 0

# Top performers
top_volume_carrier = merged_df.loc[merged_df['carries'].idxmax()] if not merged_df.empty else None
top_progressive_carrier = merged_df.loc[merged_df['progressive_carries'].idxmax()] if not merged_df.empty else None
top_distance_carrier = df.loc[df['total_distance_carried'].idxmax()] if not df.empty else None

col1, col2, col3 = st.columns(3)

with col1:
    if top_volume_carrier is not None:
        st.markdown(f"**🔄 Most Total Carries:**  \n{top_volume_carrier['player']} ({int(top_volume_carrier['carries'])})")

with col2:
    if top_progressive_carrier is not None:
        st.markdown(f"**⬆️ Most Progressive Carries:**  \n{top_progressive_carrier['player']} ({int(top_progressive_carrier['progressive_carries'])})")

with col3:
    if top_distance_carrier is not None:
        st.markdown(f"**🏃‍♂️ Most Distance Covered:**  \n{top_distance_carrier['player']} ({int(top_distance_carrier['total_distance_carried'])}m)")


# Back to homepage button
st.write("---")
if st.button("🏠 Back to Homepage"):
    st.switch_page("app.py")