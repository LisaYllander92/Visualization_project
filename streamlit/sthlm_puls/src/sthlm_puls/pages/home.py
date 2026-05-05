import streamlit as st

from sthlm_puls.utils.constants import IMAGE_PATH, MARKDOWN_PATH
from sthlm_puls.utils.helpers import read_textfile

def home():
    st.markdown("# HOME")
    st.image(IMAGE_PATH / "sthlmpuls.png")
    st.markdown(read_textfile(MARKDOWN_PATH / "intro_events.md"))

if __name__ == "__main__":
    home()