from sthlm_puls.utils.helpers import get_events_df
import duckdb
import streamlit as st

df = get_events_df()

def