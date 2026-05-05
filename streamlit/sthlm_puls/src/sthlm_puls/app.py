import streamlit as st

pages = [
    st.Page("pages/home.py", title="Home"),
    st.Page("pages/events.py", title="Events"),
    st.Page("pages/raw_data.py", title="Events_raw"),
]

pg = st.navigation(pages)

pg.run()