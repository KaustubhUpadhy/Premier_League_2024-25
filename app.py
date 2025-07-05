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

df_standings = load_standings()
table_data = df_standings.iloc[:, :9]  # Get first 9 columns as specified

# Load and display Premier League table
st.markdown("## 📊 Premier League Table 2024/25")

df_standings = load_standings()
table_data = df_standings.iloc[:, :9].copy()  # Get first 9 columns as specified

# Add qualification zone indicators
def get_zone_indicator(position):
    if position <= 4:
        return "🟢"  # Champions League
    elif position <= 7:
        return "🟠"  # Europa League
    elif position >= 18:
        return "🔴"  # Relegation
    else:
        return "⚪"  # Mid-table

# Prepare data for display
display_data = table_data.copy()
display_data['Zone'] = display_data['rank'].apply(get_zone_indicator)
display_data = display_data[['Zone', 'rank', 'team', 'win', 'loss', 'draw', 'goals', 'conceded', 'points', 'last5']]

# Rename columns for better display
display_data.columns = ['', 'Pos', 'Team', 'W', 'L', 'D', 'GF', 'GA', 'Pts', 'Last 5']

# Custom CSS for the dataframe
st.markdown("""
<style>
.stDataFrame {
    width: 100%;
}
.stDataFrame > div {
    width: 100%;
}
.stDataFrame table {
    width: 100% !important;
}
.stDataFrame th {
    background-color: #37003c !important;
    color: white !important;
    font-weight: bold !important;
    text-align: center !important;
    padding: 12px 8px !important;
}
.stDataFrame td {
    text-align: center !important;
    padding: 8px !important;
}
.stDataFrame tbody tr:hover {
    background-color: #e3f2fd !important;
    cursor: pointer !important;
}
</style>
""", unsafe_allow_html=True)

# Display the table
st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True,
    column_config={
        "": st.column_config.TextColumn(
            "",
            width="small",
        ),
        "Pos": st.column_config.NumberColumn(
            "Pos",
            width="small",
        ),
        "Team": st.column_config.TextColumn(
            "Team",
            width="medium",
        ),
        "W": st.column_config.NumberColumn(
            "W",
            width="small",
        ),
        "L": st.column_config.NumberColumn(
            "L", 
            width="small",
        ),
        "D": st.column_config.NumberColumn(
            "D",
            width="small",
        ),
        "GF": st.column_config.NumberColumn(
            "GF",
            width="small",
        ),
        "GA": st.column_config.NumberColumn(
            "GA",
            width="small",
        ),
        "Pts": st.column_config.NumberColumn(
            "Pts",
            width="small",
        ),
        "Last 5": st.column_config.TextColumn(
            "Last 5",
            width="medium",
        ),
    }
)

# Add legend and team selection
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style='display: flex; justify-content: start; gap: 20px; margin: 20px 0; font-size: 12px;'>
        <div><span style='color: #00ff00; font-size: 16px;'>🟢</span> Champions League</div>
        <div><span style='color: #ff8c00; font-size: 16px;'>🟠</span> Europa League</div>
        <div><span style='color: #ff0000; font-size: 16px;'>🔴</span> Relegation</div>
        <div><span style='color: #ffffff; font-size: 16px;'>⚪</span> Mid-table</div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# Dashboard Cards Section
st.markdown("## 🎯 Analysis Dashboards")

# Base64 images for dashboard cards
img1 = get_base64_img("images/ball_prog.png")
img2 = get_base64_img("images/goalscoring.png")
img3 = get_base64_img("images/team_analysis.png")
img4 = get_base64_img("images/attacking_efficiency.png")
img5 = get_base64_img("images/age_distribution.png")
img6 = get_base64_img("images/ball_possession.png")  # Add ball possession image

# Create two rows of cards
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
        <img src='data:image/png;base64,{img3}' style='width:100%; height:250px; object-fit:cover;'/>
        <div style='padding:10px; background-color:#f8f8f8; text-align:center;'>
            <h4>Team Analysis</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding-top:10px;'>", unsafe_allow_html=True)
    st.page_link("pages/Team_Analysis.py", label="🏆 Open Dashboard", icon="➡️")
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
        <img src='data:image/png;base64,{img1}' style='width:100%; height:250px; object-fit:cover;'/>
        <div style='padding:10px; background-color:#f8f8f8; text-align:center;'>
            <h4>Ball Progression</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding-top:10px;'>", unsafe_allow_html=True)
    st.page_link("pages/Ball_Progression.py", label="⚽ Open Dashboard", icon="➡️")
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
        <img src='data:image/png;base64,{img2}' style='width:100%; height:250px; object-fit:cover;'/>
        <div style='padding:10px; background-color:#f8f8f8; text-align:center;'>
            <h4>Goalscoring Analysis</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding-top:10px;'>", unsafe_allow_html=True)
    st.page_link("pages/Goalscoring_Analysis.py", label="🎯 Open Dashboard", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)


# Second row
st.write("")
col4, col5, col6 = st.columns(3)

with col4:
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
        <img src='data:image/png;base64,{img4}' style='width:100%; height:250px; object-fit:cover;'/>
        <div style='padding:10px; background-color:#f8f8f8; text-align:center;'>
            <h4>Attacking Efficiency</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding-top:10px;'>", unsafe_allow_html=True)
    st.page_link("pages/Attacking_Efficiency.py", label="⚔️ Open Dashboard", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)

with col5:
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
        <img src='data:image/png;base64,{img5}' style='width:100%; height:250px; object-fit:cover;'/>
        <div style='padding:10px; background-color:#f8f8f8; text-align:center;'>
            <h4>Age Distribution</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding-top:10px;'>", unsafe_allow_html=True)
    st.page_link("pages/Age_Distribution.py", label="📅 Open Dashboard", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)

with col6:
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
        <img src='data:image/png;base64,{img6}' style='width:100%; height:250px; object-fit:cover;'/>
        <div style='padding:10px; background-color:#f8f8f8; text-align:center;'>
            <h4>Ball Possession</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding-top:10px;'>", unsafe_allow_html=True)
    st.page_link("pages/Ball_Possession.py", label="⚽ Open Dashboard", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)

    # Dataset Attribution Section
st.write("---")
st.markdown("## 📊 Dataset Information")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: rgba(255,255,255,0.05); border-radius: 10px; border: 1px solid rgba(255,255,255,0.2);'>
        <h4 style='color: white; margin-bottom: 15px;'>📈 Data Source</h4>
        <p style='color: white; margin-bottom: 15px;'>This analysis is powered by comprehensive Premier League 2024/25 season data</p>
        <a href='https://www.kaggle.com/datasets/flynn28/2025-premier-league-stats-matches-salaries' target='_blank' style='background-color: #20a5ba; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;'>
            🔗 View Dataset on Kaggle
        </a>
        <p style='color: #ccc; font-size: 12px; margin-top: 15px;'>Dataset includes player stats, team stats, possession data, and match fixtures</p>
    </div>
    """, unsafe_allow_html=True)