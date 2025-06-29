import streamlit as st
import base64

st.set_page_config(page_title="Premier League 2024/25", layout="wide")

st.markdown("<h1 style='text-align: center;'>Premier League 2024/25 Season Analysis</h1>", unsafe_allow_html=True)
st.write("---")

# Base64 image encoder
def get_base64_img(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img1 = get_base64_img("images/ball_prog.png")
img2 = get_base64_img("images/ball_prog_per90.png")

# Layout using columns for reliable interaction
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style='border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.15); overflow:hidden; transition:0.3s ease;'>
        <img src='data:image/png;base64,{img1}' style='width:100%; height:200px; object-fit:cover;'/>
        <div style='padding:10px; background-color:#f8f8f8; text-align:center;'>
            <h4>Ball Progression</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Ball_Progression.py", label="⚽ Open Dashboard", icon="➡️")

with col2:
    st.markdown(f"""
    <div style='border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.15); overflow:hidden; transition:0.3s ease;'>
        <img src='data:image/png;base64,{img2}' style='width:100%; height:200px; object-fit:cover;'/>
        <div style='padding:10px; background-color:#f8f8f8; text-align:center;'>
            <h4>Ball Progression Per 90</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Ball_Progression_per_90.py", label="📊 Open Dashboard", icon="➡️")

