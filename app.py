import streamlit as st
import base64

st.set_page_config(page_title="Premier League 2024/25", layout="wide")

st.markdown("<h1 style='text-align: center;'>Premier League 2024/25 Season Analysis</h1>", unsafe_allow_html=True)
st.write("---")

# Image encoding helper
def get_base64_img(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Base64 image
img1 = get_base64_img("images/ball_prog.png")

# Center the single card
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
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