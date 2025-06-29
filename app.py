import streamlit as st
import base64

st.set_page_config(page_title="Premier League 2024/25", layout="wide")

st.markdown("<h1 style='text-align: center;'>Premier League 2024/25 Season Analysis</h1>", unsafe_allow_html=True)
st.write("---")

# Helper to convert image to base64 for inline HTML
def get_base64_img(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img1 = get_base64_img("images/ball_prog.png")
img2 = get_base64_img("images/ball_prog_per90.png")

# Card HTML with real <a href> tags (Streamlit recognizes /pages/file_name.py routes as /1_Ball_Progression etc.)
st.markdown(f"""
<style>
.card-container {{
    display: flex;
    justify-content: center;
    gap: 40px;
    margin-top: 40px;
}}
.card {{
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    overflow: hidden;
    cursor: pointer;
    width: 300px;
    text-decoration: none;
    color: inherit;
}}
.card:hover {{
    transform: scale(1.05);
    box-shadow: 0 8px 16px rgba(0,0,0,0.25);
}}
.card img {{
    width: 100%;
    height: 200px;
    object-fit: cover;
}}
.card-title {{
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    padding: 10px;
    background-color: #f8f8f8;
}}
</style>

<div class="card-container">
    <a href="/1_Ball_Progression" class="card" target="_self">
        <img src="data:image/png;base64,{img1}" />
        <div class="card-title">Ball Progression</div>
    </a>
    <a href="/2_Ball_Progression_per_90" class="card" target="_self">
        <img src="data:image/png;base64,{img2}" />
        <div class="card-title">Ball Progression Per 90</div>
    </a>
</div>
""", unsafe_allow_html=True)

