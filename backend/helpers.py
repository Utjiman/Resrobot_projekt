import base64

import streamlit as st


def load_css(file_path):
    """Laddar CSS från en extern fil och applicerar den i Streamlit."""
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def get_video_as_base64(video_path):
    """Converting a video to Base64 to embed it as HTML in Streamlit."""
    with open(video_path, "rb") as vid_file:
        return base64.b64encode(vid_file.read()).decode("utf-8")
