"""
app.py - Minimalist, High-Focus Streamlit Family Tree Builder
"""
import streamlit as st
import streamlit.components.v1 as components
from sample_data import get_sample_family_tree
from visualizer import generate_family_tree_html

# Page setup: full wide layout, distraction-free
st.set_page_config(
    page_title="Kinship | Family Tree Builder",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom minimal styling: remove excessive margins and headers
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

if "tree" not in st.session_state:
    st.session_state.tree = get_sample_family_tree()

# Render the self-contained interactive canvas
tree_html = generate_family_tree_html(st.session_state.tree, height=840)
components.html(tree_html, height=860, scrolling=False)
