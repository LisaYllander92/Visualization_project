import streamlit as st
from sthlm_puls.utils.helpers import get_events_df

def raw_data():
    st.markdown("# RAW DATA")
    st.dataframe(get_events_df())

if __name__ == "__main__":
    raw_data()