import streamlit as st
from sthlm_puls.utils.constants import MARKDOWN_PATH


def dashboard_layout():
    st.markdown("# Events dashboard")
    st.markdown(read_textfile(MARKDOWN_PATH / "intro_events.md"))
    st.dataframe(get_events_df().head())

    st.markdown("**Number of different music events during May**")

    genres = [
        "Rock",
        "Blues",
        "Reggae",
        "Hip-Hop/Rap",
        "Folk",
        "Dance/Electronic",
        "R&B",
        "Alternative",
        "Latin",
        "World",
        "Classical",
        "Miscellaneous"
    ]

    cols = st.columns(len(genres))

    for column, genre in zip(cols, genres):