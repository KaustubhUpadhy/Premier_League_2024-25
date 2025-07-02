import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Premier League 2024/25", layout="wide")

st.markdown("<h1 style='text-align: center;'>Premier League 2024/25 Season Analysis</h1>", unsafe_allow_html=True)

# Load standings data
@st.cache_data
def load_standings():
    return pd.read_csv("standings.csv")

# Image encoding helper
def get_base64_img(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Load and display Premier League table
st.markdown("## 📊 Premier League Table 2024/25")

df_standings = load_standings()
table_data = df_standings.iloc[:, :9]  # Get first 9 columns as specified

# Create the interactive table
st.markdown("""
<style>
.team-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 14px;
    background-color: white;
}

.team-table th {
    background-color: #37003c;
    color: white;
    font-weight: bold;
    padding: 12px 8px;
    text-align: center;
    border: 1px solid #ddd;
}

.team-table td {
    padding: 10px 8px;
    text-align: center;
    border: 1px solid #ddd;
    vertical-align: middle;
}

.team-table tr:nth-child(even) {
    background-color: #f8f9fa;
}

.team-table tr:hover {
    background-color: #e3f2fd;
    cursor: pointer;
}

.team-name {
    text-align: left;
    font-weight: 500;
}

.position {
    font-weight: bold;
    color: #37003c;
    min-width: 30px;
}

.qualification-zone {
    border-left: 4px solid #00ff00;
}

.europa-zone {
    border-left: 4px solid #ff8c00;
}

.relegation-zone {
    border-left: 4px solid #ff0000;
}
</style>
""", unsafe_allow_html=True)

# Generate table HTML
table_html = """
<table class="team-table">
    <thead>
        <tr>
            <th>Pos</th>
            <th>Team</th>
            <th>W</th>
            <th>L</th>
            <th>D</th>
            <th>GF</th>
            <th>GA</th>
            <th>Pts</th>
            <th>Last 5</th>
        </tr>
    </thead>
    <tbody>
"""

for index, row in table_data.iterrows():
    # Using actual column names from your CSV
    pos = row['rank']
    team_name = row['team']
    wins = row['win']
    losses = row['loss']
    draws = row['draw']
    goals_for = row['goals']
    goals_against = row['conceded']
    points = row['points']
    last5 = row['last5']
    
    # Determine row class for qualification zones
    row_class = ""
    if pos <= 4:
        row_class = "qualification-zone"
    elif pos <= 7:
        row_class = "europa-zone" 
    elif pos >= 18:
        row_class = "relegation-zone"
    
    table_html += f"""
        <tr class="{row_class}" onclick="window.open('pages/Team_Analysis.py?team={team_name.replace(' ', '_')}', '_blank')">
            <td class="position">{pos}</td>
            <td class="team-name">{team_name}</td>
            <td>{wins}</td>
            <td>{losses}</td>
            <td>{draws}</td>
            <td>{goals_for}</td>
            <td>{goals_against}</td>
            <td><strong>{points}</strong></td>
            <td>{last5}</td>
        </tr>
    """

table_html += """
    </tbody>
</table>
"""

st.markdown(table_html, unsafe_allow_html=True)

# Add legend for table colors
st.markdown("""
<div style='display: flex; justify-content: center; gap: 20px; margin: 20px 0; font-size: 12px;'>
    <div><span style='color: #00ff00; font-size: 16px;'>█</span> Champions League</div>
    <div><span style='color: #ff8c00; font-size: 16px;'>█</span> Europa League</div>
    <div><span style='color: #ff0000; font-size: 16px;'>█</span> Relegation</div>
</div>
""", unsafe_allow_html=True)

st.write("---")

# Dashboard Cards Section
st.markdown("## 🎯 Analysis Dashboards")

# Base64 images for dashboard cards
img1 = get_base64_img("images/ball_prog.png")
img2 = get_base64_img("images/goalscoring.png")
img3 = get_base64_img("images/team_analysis.png")  # Add team analysis image

# Create three columns for the cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style='
        border-radius:12px;
        box-shadow:0 4px 12px rgba(0,0,0,0.15);
        overflow:hidden;
        transition:0.3s ease;
        width:100%;
        height:330px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    '>
        <img src='data:image/png;base64,{img1}' style='width:100%; height:250px; object-fit:cover;'/>
        <div style='padding:10px; background-color:#f8f8f8; text-align:center;'>
            <h4>Ball Progression Dashboard</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding-top:10px;'>", unsafe_allow_html=True)
    st.page_link("pages/Ball_Progression.py", label="⚽ Open Dashboard", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='
        border-radius:12px;
        box-shadow:0 4px 12px rgba(0,0,0,0.15);
        overflow:hidden;
        transition:0.3s ease;
        width:100%;
        height:330px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    '>
        <img src='data:image/png;base64,{img2}' style='width:100%; height:250px; object-fit:cover;'/>
        <div style='padding:10px; background-color:#f8f8f8; text-align:center;'>
            <h4>Goalscoring Analysis</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding-top:10px;'>", unsafe_allow_html=True)
    st.page_link("pages/Goalscoring_Analysis.py", label="🎯 Open Dashboard", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='
        border-radius:12px;
        box-shadow:0 4px 12px rgba(0,0,0,0.15);
        overflow:hidden;
        transition:0.3s ease;
        width:100%;
        height:330px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    '>
        <img src='data:image/png;base64,{img3}' style='width:100%; height:250px; object-fit:cover;'/>
        <div style='padding:10px; background-color:#f8f8f8; text-align:center;'>
            <h4>Team Analysis</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding-top:10px;'>", unsafe_allow_html=True)
    st.page_link("pages/Team_Analysis.py", label="🏆 Open Dashboard", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)